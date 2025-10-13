import db_utils
import sys
from pathlib import Path
from db_utils import *


def main():
    # Connect to the SQLite database
    conn = create_connection("../Database/ibotta.db")
    if not conn:
        print("Connection failed.")
        return

    csv_folder = Path("../CSV_data")

    # Map table names to their corresponding CSV files
    csv_tables = {
        "offer_rewards": "offer_rewards_168083.csv",
        "customer_offers": "customer_offers_296332.csv",
        "customer_offer_rewards": "customer_offer_rewards_144392.csv",
        "customer_offer_redemptions": "customer_offer_redemptions_31025.csv",
    }

    # Load each CSV into its corresponding table
    for table, file_name in csv_tables.items():
        csv_path = csv_folder / file_name
        if csv_path.exists():
            print(f"Loading {csv_path} into {table}...")
            loadcsv(conn, csv_path, table)
        else:
            print(f"File not found: {csv_path}")

    # Close the database connection
    conn.close()
    print("All tables have been loaded!")

#run main
if __name__ == '__main__':
    main()
