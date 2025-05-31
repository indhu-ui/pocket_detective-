import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ──────────── Configuration ────────────
# List of substrings to identify merchants
MERCHANTS = [
    "swiggy", "zomato", "amazon", "irctc",
    "flipkart", "bigbasket", "reliance", "myntra"
]

# List of known contact names
CONTACTS = ["rahul", "neha", "arjun", "sneha", "vikram"]

# ──────────── Helper Functions ────────────
def classify_transaction_row(row):
    """
    Given a DataFrame row with 'account_name', return one of:
    - "Merchant"   (if account_name contains a known merchant substring)
    - "Friend"     (if account_name matches a known contact)
    - "Stranger"   (otherwise)
    """
    name = str(row["account_name"]).lower()
    # Check merchant substrings
    for m in MERCHANTS:
        if m in name:
            return "Merchant"
    # Check friend/contact names
    for c in CONTACTS:
        if c in name:
            return "Friend"
    # Otherwise
    return "Stranger"

def format_timestamp(ts):
    """
    Convert ISO string "YYYY-MM-DDThh:mm:ss" → "DD Mon YYYY, hh:mm AM/PM"
    """
    # If it's already a datetime object, skip parsing
    if not isinstance(ts, str):
        ts = str(ts)
    try:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        # Fallback if timestamps include milliseconds or different format
        dt = pd.to_datetime(ts)
    return dt.strftime("%d %b %Y, %I:%M %p")


# ──────────── Streamlit App Starts Here ────────────
st.set_page_config(page_title="GPay Transaction Analyzer", layout="wide")
st.title("🧾 GPay Transaction Analyzer")

st.markdown(
    """
    **How to Use:**  
    1. Upload a CSV file containing your transactions.  
    2. The app will classify each row as `Merchant`, `Friend`, or `Stranger`.  
    3. View a pie chart of total spend per category.  
    4. Click a category to list its transactions.  
    5. Click an individual transaction to see detailed analysis.  
    6. Download the full analysis as a new CSV.
    """
)

# ──────────── Step 1: Upload CSV ────────────
uploaded_file = st.file_uploader(
    "Upload a CSV file with columns: `amount`, `account_name`, `timestamp`", 
    type=["csv"]
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"⚠️ Could not read the CSV file. Make sure it is a valid CSV. Error: {e}")
        st.stop()

    # Check required columns
    required_cols = {"amount", "account_name", "timestamp"}
    if not required_cols.issubset(df.columns):
        st.error(
            f"CSV must contain these columns exactly: `{', '.join(required_cols)}`. "
            f"Found: {', '.join(df.columns)}"
        )
        st.stop()

    # ──────────── Step 2: Classify & Format ────────────
    # Ensure correct types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["account_name"] = df["account_name"].astype(str)
    df["timestamp"] = df["timestamp"].astype(str)

    # Drop any rows with missing amount or account_name
    df = df.dropna(subset=["amount", "account_name", "timestamp"])
    df = df.reset_index(drop=True)

    # Classify each transaction
    df["type"] = df.apply(classify_transaction_row, axis=1)
    # Create a human-readable timestamp column
    df["formatted_timestamp"] = df["timestamp"].apply(format_timestamp)

    # ──────────── Step 3: Downloadable Analysis CSV ────────────
    analysis_df = df[["amount", "account_name", "type", "formatted_timestamp"]]
    csv_data = analysis_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Full Analysis as CSV",
        data=csv_data,
        file_name="transaction_analysis.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # ──────────── Step 4: Pie Chart of Total Spend by Category ────────────
    st.subheader("Spending by Category")
    category_totals = (
        df.groupby("type")["amount"]
          .sum()
          .reset_index()
          .sort_values(by="amount", ascending=False)
    )

    if category_totals.empty:
        st.warning("No transactions to display.")
        st.stop()

    fig = px.pie(
        category_totals,
        names="type",
        values="amount",
        title="Spending Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ──────────── Step 5: Drill-Down by Category ────────────
    chosen_category = st.selectbox(
        "Select a category to view its transactions:",
        category_totals["type"].tolist()
    )

    filtered = df[df["type"] == chosen_category].reset_index(drop=True)
    st.markdown(f"#### Transactions under: **{chosen_category}**")
    if filtered.empty:
        st.info("No transactions in this category.")
    else:
        # Build a list of display strings
        options = [
            f"₹{row['amount']}  →  {row['account_name']}  on  {row['formatted_timestamp']}"
            for _, row in filtered.iterrows()
        ]

        # Let user pick one transaction
        selected_label = st.radio("Choose a transaction:", options, index=0)

        # Find the corresponding row index
        idx = options.index(selected_label)
        txn = filtered.iloc[idx]

        # ──────────── Step 6: Show Detailed Analysis ────────────
        st.markdown("### 🧠 Transaction Analysis")
        st.markdown(f"- **Amount:** ₹{txn['amount']}")
        st.markdown(f"- **Sent To:** {txn['account_name']}")
        st.markdown(f"- **Type:** {txn['type']}")
        st.markdown(f"- **Date & Time:** {txn['formatted_timestamp']}")

else:
    st.info("🔎 Please upload a CSV file to begin analysis.")
