#  Warehouse Order Fulfillment & Stock Management Engine
---

##  Overview
A **Python-based backend system** that processes warehouse inventory and customer orders.

It validates orders, updates stock, and generates fulfillment reports with proper logging and testing.

---

##  Features

- Product validation  
- Quantity & date validation  
- Full / Partial / Rejected fulfillment  
- Automatic stock updates  
- CSV report generation  
- Centralized logging (`logs/app.log`)  
- Unit testing with coverage  

---

##  Project Structure
# user-story-13

---

## 📁 Project Structure


user story 13/
│
├── data/
│ ├── products.csv
│ ├── warehouse_orders.csv
│
├── output/
│ ├── fulfillment_report.csv
│ ├── stock_remaining.csv
│
├── logs/
│ ├── app.log
│
├── src/
│ ├── processor.py
│ ├── validator.py
│ ├── logger.py
│
├── tests/
│ ├── test_processor.py
│
├── main.py
##  Input Files

###  products.csv
product_id,product_name,available_stock,price
P001,Laptop,20,50000
P002,Mobile,50,20000
P003,Headphones,100,1500

 ### warehouse_orders.csv
order_id,product_id,quantity,order_date
101,P001,5,2024-01-01
102,P002,10,2024-01-02

 ### Processing Rules
Product must exist
Quantity must be > 0
Date must be valid
If quantity ≤ stock → FULFILLED
If quantity > stock → PARTIAL
If stock = 0 → REJECTED

### Output
Generated in output/ folder:

 fulfillment_report.csv
order_id	product_id	requested_qty	fulfilled_qty	status	reason
 stock_remaining.csv
product_id	remaining_stock
 Logging
All logs are stored in:
logs/app.log

Includes:
Invalid product
Invalid quantity
Invalid date
Stock issues
Processing steps
