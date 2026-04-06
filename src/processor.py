import pandas as pd
from validator import validate_order   
from logger import log_info, log_error


def process_orders(products_df, orders_df):
    products_df.columns = products_df.columns.str.strip().str.lower()
    orders_df.columns = orders_df.columns.str.strip().str.lower()

    required_product_cols = {"product_id", "available_stock"}
    required_order_cols = {"order_id", "product_id", "quantity", "order_date"}

    if not required_product_cols.issubset(products_df.columns):
        raise ValueError("Products file missing required columns")

    if not required_order_cols.issubset(orders_df.columns):
        raise ValueError("Orders file missing required columns")

    # Stock dictionary
    stock = {}
    for _, row in products_df.iterrows():
        try:
            stock[row["product_id"]] = int(row["available_stock"])
        except Exception:
            log_error(f"Invalid stock data: {row}")

    results = []

    for _, row in orders_df.iterrows():
        order_id = row.get("order_id")
        log_info(f"Processing order_id={order_id}")

        is_valid, error_type = validate_order(row, products_df)

        if not is_valid:
            results.append({
                "order_id": order_id,
                "product_id": row.get("product_id"),
                "requested_qty": row.get("quantity"),
                "fulfilled_qty": 0,
                "status": "REJECTED",
                "reason": error_type
            })
            continue

        product_id = row["product_id"]
        qty = int(row["quantity"])
        available = stock.get(product_id, 0)

        if available == 0:
            status = "REJECTED"
            fulfilled = 0
            reason = "OUT_OF_STOCK"
            log_error(f"Order {order_id} rejected")

        elif qty <= available:
            status = "FULFILLED"
            fulfilled = qty
            stock[product_id] -= qty
            reason = None
            log_info(f"Order {order_id} fulfilled")

        else:
            status = "PARTIAL"
            fulfilled = available
            stock[product_id] = 0
            reason = "INSUFFICIENT_STOCK"
            log_error(f"Order {order_id} partial")

        results.append({
            "order_id": order_id,
            "product_id": product_id,
            "requested_qty": qty,
            "fulfilled_qty": fulfilled,
            "status": status,
            "reason": reason
        })

    report_df = pd.DataFrame(results)

    stock_df = pd.DataFrame([
        {"product_id": pid, "remaining_stock": qty}
        for pid, qty in stock.items()
    ])

    return report_df, stock_df