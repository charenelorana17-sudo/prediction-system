import unittest

from app import deduplicate_sales_rows


class SalesDeduplicationTest(unittest.TestCase):
    def test_deduplicate_sales_rows_removes_exact_duplicates(self):
        rows = [
            {
                "date": "2026-03-26",
                "bread_type": "Pandesal",
                "products_produced": 100,
                "actual_qty_sold": 90,
                "waste_returns": 10,
                "price_per_product": 2.0,
                "temperature": 30.0,
                "is_holiday": 0,
                "is_promotion": 0,
                "sacks_used": 0,
                "plates_used": 0,
                "expense_amount": 0.0,
            },
            {
                "date": "2026-03-26",
                "bread_type": "Pandesal",
                "products_produced": 100,
                "actual_qty_sold": 90,
                "waste_returns": 10,
                "price_per_product": 2.0,
                "temperature": 30.0,
                "is_holiday": 0,
                "is_promotion": 0,
                "sacks_used": 0,
                "plates_used": 0,
                "expense_amount": 0.0,
            },
            {
                "date": "2026-03-27",
                "bread_type": "Ensaymada",
                "products_produced": 120,
                "actual_qty_sold": 110,
                "waste_returns": 10,
                "price_per_product": 4.5,
                "temperature": 31.0,
                "is_holiday": 0,
                "is_promotion": 1,
                "sacks_used": 1,
                "plates_used": 1,
                "expense_amount": 5.0,
            },
        ]

        deduped = deduplicate_sales_rows(rows)

        self.assertEqual(len(deduped), 2)
        self.assertEqual(deduped[0]["date"], "2026-03-26")
        self.assertEqual(deduped[1]["bread_type"], "Ensaymada")


if __name__ == "__main__":
    unittest.main()
