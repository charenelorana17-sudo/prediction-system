import unittest
from datetime import date

from app import app, build_production_log_rows


class ProductionLogHistoryTest(unittest.TestCase):
    def test_build_production_log_rows_links_predictions_to_sales_outcomes(self):
        prediction_rows = [
            {
                "bread_type": "Pandesal",
                "date_predicted": date(2026, 6, 1),
                "predicted_demand": 120,
                "recommended_production": 132,
                "confidence": 95,
            }
        ]
        sales_rows = [
            {
                "date": "2026-06-01",
                "bread_type": "Pandesal",
                "products_produced": 140,
                "actual_qty_sold": 125,
                "waste_returns": 15,
            }
        ]

        rows = build_production_log_rows(prediction_rows, sales_rows)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["bread_type"], "Pandesal")
        self.assertEqual(rows[0]["predicted_demand"], 120)
        self.assertEqual(rows[0]["recommended_production"], 132)
        self.assertEqual(rows[0]["actual_production"], 140)
        self.assertEqual(rows[0]["waste"], 15)
        self.assertEqual(rows[0]["confidence"], 95)

    def test_production_plan_page_renders_for_logged_in_user(self):
        client = app.test_client()

        with client.session_transaction() as sess:
            sess["logged_in"] = True

        response = client.get("/production-plan")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
