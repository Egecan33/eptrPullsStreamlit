import json
import argparse
import pandas as pd
from eptr2 import EPTR2
from datetime import datetime


def main(input_date: str):
    # Load credentials from JSON file
    try:
        with open("eptr_credentials.json", "r") as f:
            creds = json.load(f)
    except FileNotFoundError:
        print(
            "Error: eptr_credentials.json file not found. Please ensure it exists in the current directory."
        )
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding eptr_credentials.json: {e}")
        return

    username = creds.get("EPTR_USERNAME")
    password = creds.get("EPTR_PASSWORD")

    if not username or not password:
        print("Error: Username or password not found in eptr_credentials.json.")
        return

    # Create EPTR2 object using username and password
    try:
        eptr = EPTR2(username=username, password=password)
    except Exception as e:
        print(f"Error creating EPTR2 object: {e}")
        return

    # Fetch data (Market Clearing Price) for the given date
    # Using the same date for start and end to get that single day's data
    try:
        result = eptr.call(
            "mcp", start_date=input_date, end_date=input_date, postprocess=True
        )
        print("Data fetched successfully.")
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return

    # Debugging: Print the type of result
    print(f"Type of result: {type(result)}")

    # Convert result to a DataFrame and display
    if isinstance(result, pd.DataFrame):
        df = result
        if not df.empty:
            print(f"DataFrame created with shape: {df.shape}")
            print(df.head())  # Display first few rows

            # If you'd like to save to CSV, uncomment the lines below
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = f"./PTF_{timestamp}.csv"
            try:
                df.to_csv(csv_path, index=False)
                print(f"Data saved to CSV file: {csv_path}")
            except Exception as e:
                print(f"Error saving data to CSV: {e}")
        else:
            print("The DataFrame is empty. No data to display or save.")
    elif isinstance(result, list) and len(result) > 0:
        df = pd.DataFrame(result)
        print(f"DataFrame created with shape: {df.shape}")
        print(df.head())  # Display first few rows

        # If you'd like to save to CSV, uncomment the lines below
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"./PTF_{timestamp}.csv"
        try:
            df.to_csv(csv_path, index=False)
            print(f"Data saved to CSV file: {csv_path}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
    else:
        print("No data returned or result is not a valid list or DataFrame.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch MCP data for a given date.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    args = parser.parse_args()
    main(args.date)
