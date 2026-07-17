import app as app_module


def test_sales_log_summary_uses_full_dataset_when_filter_is_active(monkeypatch):
    app_module.app.config["TESTING"] = True
    app_module.SALES_DATA = [
        {
            "date": "2024-01-01",
            "bread_type": "Pandesal",
            "products_produced": 10,
            "actual_qty_sold": 5,
            "waste_returns": 1,
            "price_per_product": 10.0,
            "temperature": 30.0,
            "is_holiday": 0,
            "is_promotion": 0,
            "sacks_used": 0,
            "plates_used": 0,
            "expense_amount": 0.0,
        },
        {
            "date": "2024-01-02",
            "bread_type": "Cheese Bread",
            "products_produced": 20,
            "actual_qty_sold": 8,
            "waste_returns": 2,
            "price_per_product": 15.0,
            "temperature": 30.0,
            "is_holiday": 0,
            "is_promotion": 0,
            "sacks_used": 0,
            "plates_used": 0,
            "expense_amount": 0.0,
        },
    ]

    monkeypatch.setattr(app_module, "fetch_all_expenses_total", lambda: 0)
    monkeypatch.setattr(app_module, "fetch_monthly_expense_total", lambda month: 0)
    monkeypatch.setattr(app_module, "fetch_monthly_expenses", lambda month: [])
    monkeypatch.setattr(app_module, "retrain_model_async", lambda sales: None)
    app_module.WEEKLY_PLAN = []

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["logged_in"] = True

    response = client.get("/prediction_system/sales-log?filter_date=2024-01-02&history_period=daily")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "₱170.00" in html
    assert "Dataset" in html and "2" in html
