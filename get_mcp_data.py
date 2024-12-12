# app.py

import streamlit as st
from datetime import datetime
import pandas as pd
from eptr2 import EPTR2

def fetch_mcp_data(input_date: str, username: str, password: str):
    """
    Fetch MCP data for the given date using EPTR2 credentials.

    Args:
        input_date (str): Date in YYYY-MM-DD format.
        username (str): EPTR2 username.
        password (str): EPTR2 password.

    Returns:
        pd.DataFrame or None: DataFrame containing MCP data or None if failed.
    """
    try:
        # Create EPTR2 object using username and password
        eptr = EPTR2(username=username, password=password)
    except Exception as e:
        st.error(f"Failed to create EPTR2 object: {e}")
        return None

    # Fetch data (Market Clearing Price) for the given date
    try:
        result = eptr.call(
            "mcp",
            start_date=input_date,
            end_date=input_date,
            postprocess=True
        )
        st.success("Data fetched successfully.")
    except Exception as e:
        st.error(f"Error while fetching data: {e}")
        return None

    # Process the result
    if isinstance(result, pd.DataFrame):
        df = result
        if not df.empty:
            st.write(f"**DataFrame Shape:** {df.shape}")
            st.dataframe(df)
            return df
        else:
            st.warning("The DataFrame is empty. No data to display.")
            return None
    elif isinstance(result, list) and len(result) > 0:
        df = pd.DataFrame(result)
        st.write(f"**DataFrame Shape:** {df.shape}")
        st.dataframe(df)
        return df
    else:
        st.warning("No data returned or result is not a valid list or DataFrame.")
        return None

def main():
    st.title("EPİAŞ Market Clearing Price (PTF) Data Fetcher")

    st.markdown("""
    This application fetches Market Clearing Price (PTF) data from EPİAŞ for a specified date.
    """)

    # Date input
    input_date = st.date_input("Select Date", datetime.today())
    input_date_str = input_date.strftime("%Y-%m-%d")

    # Button to fetch data
    if st.button("Fetch Data"):
        # Retrieve credentials from Streamlit secrets
        try:
            username = st.secrets["eptr_credentials"]["EPTR_USERNAME"]
            password = st.secrets["eptr_credentials"]["EPTR_PASSWORD"]
        except KeyError:
            st.error("EPTR2 credentials not found in Streamlit secrets.")
            return

        # Fetch data
        df = fetch_mcp_data(input_date_str, username, password)

        # Optionally, you can display additional information or visualizations here
        # For example:
        # if df is not None:
        #     st.line_chart(df['price_column'])  # Replace 'price_column' with actual column name

if __name__ == "__main__":
    main()
