import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Finance Dashboard", layout="wide")

st.title("💰 Personal Finance Dashboard")

file = st.file_uploader("Upload File", type=["csv", "xlsx"])

if file:

    # Load file
    if file.name.endswith("csv"):
        df = pd.read_csv(file, header=1)
    else:
        df = pd.read_excel(file, header=1)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Force rename
    df.columns = ['date', 'type', 'category', 'amount']

    # 🔥 REMOVE BAD ROWS (IMPORTANT)
    df = df[df['date'] != 'Column1']   # remove fake row
    df = df.dropna(subset=['date'])    # remove empty rows

    # Clean amount
    df['amount'] = df['amount'].astype(str).replace('[₹, ]', '', regex=True)

    # 🔥 REMOVE NON-NUMERIC VALUES
    df = df[df['amount'].str.replace('.', '', regex=False).str.isnumeric()]

    df['amount'] = df['amount'].astype(float)

    # Convert date
    df['date'] = pd.to_datetime(df['date'])


    # KPIs
    income = df[df['type'] == 'Income']['amount'].sum()
    expense = df[df['type'] == 'Expense']['amount'].sum()
    savings = income - expense

    col1, col2, col3 = st.columns(3)

    col1.metric("Income", f"₹{income}")
    col2.metric("Expense", f"₹{expense}")
    col3.metric("Savings", f"₹{savings}")

    # PIE CHART
    st.subheader("Expense by Category")

    expense_df = df[df['type'] == 'Expense']
    fig1 = px.pie(expense_df, names='category', values='amount')
    st.plotly_chart(fig1)

    # LINE CHART
    st.subheader("Monthly Savings")

    df['month'] = df['date'].dt.to_period('M').astype(str)

    monthly = df.groupby(['month', 'type'])['amount'].sum().unstack().fillna(0)
    monthly['Savings'] = monthly.get('Income', 0) - monthly.get('Expense', 0)

    fig2 = px.line(monthly, x=monthly.index, y='Savings', markers=True)
    st.plotly_chart(fig2)

    # TABLE
    st.dataframe(df)

    
    st.write(df.columns)


else:
    st.write("Upload your file to start")
