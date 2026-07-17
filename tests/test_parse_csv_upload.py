import io

import pandas as pd

from app import parse_csv_upload


class DummyFile:
    def __init__(self, content, filename="upload.csv"):
        self.stream = io.BytesIO(content.encode("utf-8"))
        self.filename = filename


def test_parse_csv_upload_aggregates_duplicates():
    csv = """date,bread_type,Products_Produced,Actual_Qty_Sold,Waste_Returns,Price_Per_Product,Expense_Amount
2026-06-01,Pandesal,100,60,10,10.0,50
2026-06-01,Pandesal,80,40,5,12.0,30
2026-06-01,Cheese Bread,50,30,3,20.0,20
"""

    dummy = DummyFile(csv, filename="test.csv")
    records = parse_csv_upload(dummy)

    # Expect two aggregated records: Pandesal and Cheese Bread
    assert isinstance(records, list)
    assert len(records) == 2

    by_key = {(r["date"], r["bread_type"]): r for r in records}

    p = by_key.get(("2026-06-01", "Pandesal"))
    assert p is not None
    assert p["products_produced"] == 180
    assert p["actual_qty_sold"] == 100
    assert p["waste_returns"] == 15
    assert round(p["expense_amount"], 2) == 80.0
    # Weighted price: (60*10 + 40*12) / 100 = 10.8
    assert float(p["price_per_product"]) == 10.8

    c = by_key.get(("2026-06-01", "Cheese Bread"))
    assert c is not None
    assert c["products_produced"] == 50
    assert c["actual_qty_sold"] == 30
    assert c["price_per_product"] == 20.0


def test_parse_excel_upload_xlsx_file():
    df = pd.DataFrame([
        {
            "date": "2026-06-02",
            "bread_type": "Cheese Bread",
            "Products_Produced": 40,
            "Actual_Qty_Sold": 20,
            "Waste_Returns": 2,
            "Price_Per_Product": 18.0,
            "Expense_Amount": 15.0,
        }
    ])
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)

    class ExcelDummyFile(DummyFile):
        def __init__(self, bytes_content, filename="upload.xlsx"):
            self.stream = io.BytesIO(bytes_content)
            self.filename = filename

    dummy = ExcelDummyFile(buffer.read())
    records = parse_csv_upload(dummy)

    assert isinstance(records, list)
    assert len(records) == 1
    record = records[0]
    assert record["date"] == "2026-06-02"
    assert record["bread_type"] == "Cheese Bread"
    assert record["products_produced"] == 40
    assert record["actual_qty_sold"] == 20
    assert record["waste_returns"] == 2
    assert float(record["price_per_product"]) == 18.0
    assert float(record["expense_amount"]) == 15.0
