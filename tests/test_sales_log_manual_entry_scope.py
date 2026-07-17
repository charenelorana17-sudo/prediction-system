from datetime import date

from app import build_batch_entry_records


def test_build_batch_entry_records_respects_selected_date_scope():
    rows = build_batch_entry_records(
        start_date=date(2026, 6, 2),
        scope_days=3,
        bread_inputs=[
            {"bread_type": "Pandesal", "produced": 10, "sold": 7, "price": 4.5},
            {"bread_type": "Cheese Bread", "produced": 4, "sold": 3, "price": 5.5},
        ],
    )

    assert len(rows) == 6
    assert rows[0]["date"] == "2026-06-02"
    assert rows[0]["bread_type"] == "Pandesal"
    assert rows[1]["date"] == "2026-06-02"
    assert rows[1]["bread_type"] == "Cheese Bread"
    assert rows[2]["date"] == "2026-06-03"
    assert rows[2]["bread_type"] == "Pandesal"
    assert rows[5]["date"] == "2026-06-04"
    assert rows[5]["bread_type"] == "Cheese Bread"
