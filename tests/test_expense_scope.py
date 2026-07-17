from app import get_expense_scope_context


def test_expense_scope_context_builds_daily_weekly_and_monthly_periods():
    daily = get_expense_scope_context("daily", selected_date="2026-06-15")
    assert daily["scope_type"] == "daily"
    assert daily["period_key"] == "2026-06-15"
    assert daily["expense_date"].strftime("%Y-%m-%d") == "2026-06-15"

    weekly = get_expense_scope_context("weekly", selected_week="2026-W25")
    assert weekly["scope_type"] == "weekly"
    assert weekly["period_key"] == "2026-W25"
    assert weekly["expense_week"] == 25

    monthly = get_expense_scope_context("monthly", selected_month="2026-06")
    assert monthly["scope_type"] == "monthly"
    assert monthly["period_key"] == "2026-06"
    assert monthly["expense_month"].strftime("%Y-%m") == "2026-06"
