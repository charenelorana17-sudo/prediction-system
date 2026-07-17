import importlib
import os


def test_ingredients_expenses_save_without_mysql(monkeypatch):
    os.environ["USE_MYSQL"] = "0"
    import app as app_module

    importlib.reload(app_module)
    app_module.MONTHLY_EXPENSES.clear()
    app_module.app.config["TESTING"] = True

    client = app_module.app.test_client()
    with client.session_transaction() as session:
        session["logged_in"] = True

    response = client.post(
        "/ingredients",
        data={
            "action": "save_expenses",
            "scope_type": "monthly",
            "selected_month": "2026-07",
            "amount_Flour (1st Class)": "123.45",
            "unit_Flour (1st Class)": "test note",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    expenses = app_module.fetch_monthly_expenses("2026-07", scope_type="monthly", period_key="2026-07")
    assert expenses["Flour (1st Class)"]["amount"] == 123.45
    assert expenses["Flour (1st Class)"]["note"] == "test note"


def test_ingredients_expenses_clear_scope_without_mysql(monkeypatch):
    os.environ["USE_MYSQL"] = "0"
    import app as app_module

    importlib.reload(app_module)
    app_module.MONTHLY_EXPENSES.clear()
    app_module.app.config["TESTING"] = True

    client = app_module.app.test_client()
    with client.session_transaction() as session:
        session["logged_in"] = True

    response = client.post(
        "/ingredients",
        data={
            "action": "save_expenses",
            "scope_type": "monthly",
            "selected_month": "2026-07",
            "amount_Flour (1st Class)": "456.78",
            "unit_Flour (1st Class)": "kg",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    expenses = app_module.fetch_monthly_expenses("2026-07", scope_type="monthly", period_key="2026-07")
    assert expenses["Flour (1st Class)"]["amount"] == 456.78
    assert expenses["Flour (1st Class)"]["note"] == "kg"

    response = client.post(
        "/ingredients",
        data={
            "action": "clear_expenses",
            "scope_type": "monthly",
            "selected_month": "2026-07",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    expenses = app_module.fetch_monthly_expenses("2026-07", scope_type="monthly", period_key="2026-07")
    assert expenses == {}


def test_ensure_monthly_expenses_schema_adds_scope_columns(monkeypatch):
    os.environ["USE_MYSQL"] = "1"
    import app as app_module

    importlib.reload(app_module)

    class FakeCursor:
        def __init__(self):
            self.queries = []

        def execute(self, query, params=None):
            self.queries.append((query, params))
            if query.strip().upper().startswith("SHOW COLUMNS"):
                return None
            return None

        def fetchall(self):
            return [("id",), ("category",), ("amount",), ("note",)]

        def close(self):
            return None

    class FakeConnection:
        def __init__(self):
            self.cursor_obj = FakeCursor()

        def cursor(self):
            return self.cursor_obj

        def commit(self):
            return None

        def close(self):
            return None

    fake_conn = FakeConnection()
    monkeypatch.setattr(app_module, "get_db_connection", lambda: fake_conn)

    app_module.ensure_monthly_expenses_table_schema()

    executed_queries = [query for query, _params in fake_conn.cursor_obj.queries]
    assert any("scope_type" in query for query in executed_queries)
    assert any("period_key" in query for query in executed_queries)
