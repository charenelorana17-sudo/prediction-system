import io

from app import app


def test_sales_log_accepts_upload_excel_action_for_excel_file():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["logged_in"] = True

    payload = {
        "action": "upload_excel",
        "file": (io.BytesIO(b"date,bread_type,Products_Produced,Actual_Qty_Sold,Waste_Returns,Price_Per_Product,Expense_Amount\n2026-06-01,Pandesal,10,8,1,4.5,5.0\n"), "upload.csv"),
    }

    response = client.post("/sales-log", data=payload, content_type="multipart/form-data", follow_redirects=False)

    assert response.status_code in (200, 302)
    assert b"uploaded successfully" in response.data.lower()
