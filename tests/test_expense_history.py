from app import build_expense_history_rows


def test_build_expense_history_rows_returns_latest_entries_first():
    entries = [
        {
            "scope_type": "monthly",
            "period_key": "2026-01",
            "category": "Flour (1st Class)",
            "amount": 150.0,
            "note": "Opening stock",
            "created_at": "2026-01-10T09:00:00",
        },
        {
            "scope_type": "weekly",
            "period_key": "2026-W02",
            "category": "Sugar",
            "amount": 75.5,
            "note": "Weekly purchase",
            "created_at": "2026-01-15T10:30:00",
        },
    ]

    rows = build_expense_history_rows(entries, limit=5)

    assert len(rows) == 2
    assert rows[0]["category"] == "Sugar"
    assert rows[0]["amount"] == 75.5
    assert rows[1]["category"] == "Flour (1st Class)"
