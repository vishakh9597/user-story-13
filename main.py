import pandas as pd
import sys
import os

# Allow imports from src
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from processor import process_orders


def main():
    try:
        # Create output folder if not exists
        os.makedirs("output", exist_ok=True)

        products_df = pd.read_csv("data/products.csv")
        orders_df = pd.read_csv("data/warehouse_orders.csv")

        report_df, stock_df = process_orders(products_df, orders_df)

        # Save into output folder
        report_df.to_csv("output/fulfillment_report.csv", index=False)
        stock_df.to_csv("output/stock_remaining.csv", index=False)

        print(" Processing completed successfully")

    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    main()