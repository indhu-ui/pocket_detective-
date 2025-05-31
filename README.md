# 🕵️‍♂️ Pocket Detective

**Pocket Detective** is a powerful Streamlit web app that helps you analyze and categorize your personal transaction history from any **digital wallet** or **UPI-based app** (e.g., PhonePe, Paytm, GPay, etc.).

Upload your CSV, and Pocket Detective will turn your payment data into visual summaries and interactive insights—so you can track where your money is going and uncover spending patterns instantly.

---

## 📌 Features

- 🔄 **Upload CSV**: Accepts a transaction file with columns `amount`, `account_name`, and `timestamp`.
- 🧠 **Smart Categorization**: Classifies each transaction as:
  - `Merchant`: Known businesses like Swiggy, Amazon, etc.
  - `Friend`: Personal contacts (you can customize the list)
  - `Stranger`: Unknown or uncategorized recipients
- 📊 **Pie Chart Visualization**: See how your total spending is distributed by category.
- 📋 **Category Drill-Down**: Click on any pie slice to view a full table of related transactions.
- 🔍 **Transaction Details**: Select a single transaction to reveal date, time, type, and recipient.
- 📥 **Export Analysis**: Download the processed data as a CSV for offline use or reporting.

---

## 📂 CSV Format

Ensure your file is in CSV format with the following headers:

```csv
amount,account_name,timestamp
499,Swiggy,2025-05-27T20:34:00
1200,Rahul,2025-05-25T10:22:00
...
