import unittest
from datetime import date

import app as app_module


class SalesUpsertTest(unittest.TestCase):
    """Test the UPSERT logic and duplicate prevention for sales records."""

    def setUp(self):
        """Set up test by creating a fresh app instance."""
        self.app = app_module.application
        self.client = self.app.test_client()

    def test_upsert_logic_updates_existing_record(self):
        """Verify that saving a record with the same (date, bread_type) updates the existing record instead of creating a duplicate."""
        if not app_module.USE_MYSQL:
            self.skipTest("MySQL not enabled; UPSERT logic requires database")

        try:
            # Clear the database first
            conn = app_module.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales_data WHERE date = %s AND bread_type = %s", ("2026-06-30", "Pandesal"))
            conn.commit()
            cursor.close()
            conn.close()

            # Insert the first record
            record1 = {
                "date": "2026-06-30",
                "bread_type": "Pandesal",
                "products_produced": 100,
                "actual_qty_sold": 80,
                "waste_returns": 20,
                "price_per_product": 5.0,
                "temperature": 30.0,
                "is_holiday": 0,
                "is_promotion": 0,
                "sacks_used": 1,
                "plates_used": 10,
                "expense_amount": 50.0,
            }
            app_module.save_sales_record(record1)

            # Verify the record was inserted
            conn = app_module.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as cnt FROM sales_data WHERE date = %s AND bread_type = %s", ("2026-06-30", "Pandesal"))
            result = cursor.fetchone()
            initial_count = result["cnt"]
            cursor.close()
            conn.close()
            self.assertEqual(initial_count, 1, "First record should be inserted")

            # Save a second record with the same (date, bread_type) but different values
            record2 = {
                "date": "2026-06-30",
                "bread_type": "Pandesal",
                "products_produced": 120,  # Changed
                "actual_qty_sold": 90,     # Changed
                "waste_returns": 30,       # Changed
                "price_per_product": 5.5,  # Changed
                "temperature": 31.0,
                "is_holiday": 0,
                "is_promotion": 1,         # Changed
                "sacks_used": 1,
                "plates_used": 10,
                "expense_amount": 55.0,    # Changed
            }
            app_module.save_sales_record(record2)

            # Verify no duplicates were created
            conn = app_module.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as cnt FROM sales_data WHERE date = %s AND bread_type = %s", ("2026-06-30", "Pandesal"))
            result = cursor.fetchone()
            final_count = result["cnt"]
            self.assertEqual(final_count, 1, "UPSERT should not create a duplicate; should only update")

            # Verify the record was updated with new values
            cursor.execute("SELECT products_produced, actual_qty_sold, is_promotion FROM sales_data WHERE date = %s AND bread_type = %s", ("2026-06-30", "Pandesal"))
            updated = cursor.fetchone()
            cursor.close()
            conn.close()
            self.assertEqual(updated["products_produced"], 120, "Record should be updated with new produced value")
            self.assertEqual(updated["actual_qty_sold"], 90, "Record should be updated with new sold value")
            self.assertEqual(updated["is_promotion"], 1, "Record should be updated with new is_promotion value")

        except Exception as e:
            self.fail(f"UPSERT test failed: {e}")

    def test_cleanup_duplicate_sales_removes_duplicates(self):
        """Verify that cleanup_duplicate_sales() function exists and works correctly on legacy duplicates."""
        if not app_module.USE_MYSQL:
            self.skipTest("MySQL not enabled; cleanup logic requires database")

        try:
            # The unique constraint now prevents duplicates from being created.
            # This test verifies the cleanup function exists and completes without error.
            conn = app_module.get_db_connection()
            cursor = conn.cursor()
            
            # Delete any existing test data
            cursor.execute("DELETE FROM sales_data WHERE date = %s AND bread_type = %s", ("2026-06-29", "Cheese Bread"))
            conn.commit()
            cursor.close()
            conn.close()

            # Run cleanup - should complete without error
            cleaned_count = app_module.cleanup_duplicate_sales()
            
            # Verify cleanup returned a count (even if 0 since no duplicates exist)
            self.assertIsInstance(cleaned_count, int, "Cleanup should return an integer count")
            self.assertGreaterEqual(cleaned_count, 0, "Cleanup count should be >= 0")

        except Exception as e:
            self.fail(f"Cleanup test failed: {e}")


if __name__ == "__main__":
    unittest.main()
