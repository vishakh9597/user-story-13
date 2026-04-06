import unittest
import pandas as pd
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from processor import process_orders


class TestWarehouseProcessor(unittest.TestCase):

    def setUp(self):
        # Sample products data (matches your CSV structure)
        self.products_df = pd.DataFrame({
            "product_id": ["P001", "P002"],
            "available_stock": [10, 5]
        })

    #  Invalid product
    def test_invalid_product_rejected(self):
        orders_df = pd.DataFrame({
            "order_id": [101],
            "product_id": ["P999"],
            "quantity": [2],
            "order_date": ["2024-01-01"]
        })

        report, _ = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[0]["status"], "REJECTED")
        self.assertEqual(report.iloc[0]["reason"], "INVALID_PRODUCT")

    #  Negative quantity
    def test_negative_quantity_rejected(self):
        orders_df = pd.DataFrame({
            "order_id": [102],
            "product_id": ["P001"],
            "quantity": [-5],
            "order_date": ["2024-01-01"]
        })

        report, _ = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[0]["status"], "REJECTED")
        self.assertEqual(report.iloc[0]["reason"], "INVALID_QUANTITY")

    #  Invalid date
    def test_invalid_date_rejected(self):
        orders_df = pd.DataFrame({
            "order_id": [103],
            "product_id": ["P001"],
            "quantity": [2],
            "order_date": ["invalid-date"]
        })

        report, _ = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[0]["status"], "REJECTED")
        self.assertEqual(report.iloc[0]["reason"], "INVALID_DATE")

    # Full fulfillment
    def test_full_fulfillment(self):
        orders_df = pd.DataFrame({
            "order_id": [104],
            "product_id": ["P001"],
            "quantity": [5],
            "order_date": ["2024-01-01"]
        })

        report, stock = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[0]["status"], "FULFILLED")
        self.assertEqual(report.iloc[0]["fulfilled_qty"], 5)

        remaining = stock.loc[stock["product_id"] == "P001", "remaining_stock"].values[0]
        self.assertEqual(remaining, 5)

    # Partial fulfillment
    def test_partial_fulfillment(self):
        orders_df = pd.DataFrame({
            "order_id": [105],
            "product_id": ["P002"],
            "quantity": [10],
            "order_date": ["2024-01-01"]
        })

        report, stock = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[0]["status"], "PARTIAL")
        self.assertEqual(report.iloc[0]["fulfilled_qty"], 5)

        remaining = stock.loc[stock["product_id"] == "P002", "remaining_stock"].values[0]
        self.assertEqual(remaining, 0)

    # Out of stock
    def test_out_of_stock(self):
        # First consume stock
        orders_df = pd.DataFrame({
            "order_id": [106, 107],
            "product_id": ["P001", "P001"],
            "quantity": [10, 1],
            "order_date": ["2024-01-01", "2024-01-02"]
        })

        report, _ = process_orders(self.products_df, orders_df)

        self.assertEqual(report.iloc[1]["status"], "REJECTED")
        self.assertEqual(report.iloc[1]["reason"], "OUT_OF_STOCK")

    #  Stock deduction consistency
    def test_stock_deduction(self):
        orders_df = pd.DataFrame({
            "order_id": [108],
            "product_id": ["P001"],
            "quantity": [3],
            "order_date": ["2024-01-01"]
        })

        _, stock = process_orders(self.products_df, orders_df)

        remaining = stock.loc[stock["product_id"] == "P001", "remaining_stock"].values[0]
        self.assertEqual(remaining, 7)


if __name__ == "__main__":
    unittest.main()