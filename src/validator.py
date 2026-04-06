import pandas as pd
from logger import log_error  


def validate_order(row, products_df):
    product_id = row.get("product_id")
    qty = row.get("quantity")
    date = row.get("order_date")

    if product_id not in products_df["product_id"].values:
        log_error(f"Invalid product_id: {product_id}")
        return False, "INVALID_PRODUCT"

    if not isinstance(qty, (int, float)) or qty <= 0:
        log_error(f"Invalid quantity: {qty}")
        return False, "INVALID_QUANTITY"

    try:
        pd.to_datetime(date)
    except Exception:
        log_error(f"Invalid date: {date}")
        return False, "INVALID_DATE"

    return True, None