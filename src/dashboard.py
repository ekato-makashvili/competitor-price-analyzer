import streamlit as st
import pandas as pd
from src.database.models import get_connection

st.set_page_config(page_title="Price Analyzer", layout="wide")

st.title("📱 Price Intelligence Dashboard")

def load_data():
    try:
        conn = get_connection()
        query = "SELECT store_name, product_name, price, scraped_at FROM prices ORDER BY scraped_at DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

df = load_data()

if df is not None and not df.empty:
    st.metric("Total Products", len(df))
    st.dataframe(df, use_container_width=True)
else:
    st.info("Waiting for data... Ensure the scraper has finished its first run.")