"""Test automatic ingredient deduction when sales are logged."""
import sys
import os
import unittest
from datetime import date

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app as main_app


class TestAutoIngredientDeduction(unittest.TestCase):
    """Test automatic ingredient stock reduction for sales."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Disable MySQL for testing
        os.environ['USE_MYSQL'] = '0'
        self.app = main_app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_bread_recipes_defined(self):
        """Test that bread recipes are defined for major bread types."""
        self.assertIn('Pandesal', main_app.BREAD_RECIPES)
        self.assertIn('Cheese Bread', main_app.BREAD_RECIPES)
        self.assertIn('Ensaymada', main_app.BREAD_RECIPES)
        self.assertIn('Mamon', main_app.BREAD_RECIPES)
    
    def test_pandesal_recipe_has_ingredients(self):
        """Test that Pandesal recipe includes flour and other basics."""
        recipe = main_app.BREAD_RECIPES['Pandesal']
        self.assertIn('Flour (1st Class)', recipe)
        self.assertIn('Sugar', recipe)
        self.assertIn('Vegetable Oil', recipe)
        self.assertIn('Yeast', recipe)
        self.assertGreater(recipe['Flour (1st Class)'], 0)
    
    def test_recipe_quantities_are_positive(self):
        """Test that all recipe quantities are positive numbers."""
        for bread_type, ingredients in main_app.BREAD_RECIPES.items():
            for ingredient_name, quantity in ingredients.items():
                self.assertGreater(quantity, 0, 
                    f"Invalid quantity for {ingredient_name} in {bread_type}: {quantity}")
    
    def test_ingredient_calculation_for_sale(self):
        """Test ingredient calculation for a sales quantity."""
        recipe = main_app.BREAD_RECIPES['Pandesal']
        quantity_sold = 100
        
        # Calculate expected consumption
        flour_needed = recipe['Flour (1st Class)'] * quantity_sold
        self.assertGreater(flour_needed, 0)
        self.assertEqual(flour_needed, 8.0)  # 0.08 * 100
    
    def test_multiple_bread_recipes(self):
        """Test that multiple bread types have recipes."""
        count = len(main_app.BREAD_RECIPES)
        self.assertGreaterEqual(count, 5, 
            f"Expected at least 5 bread recipes, but got {count}")
    
    def test_cheese_bread_has_extra_ingredients(self):
        """Test that Cheese Bread recipe is different from Pandesal."""
        pandesal_recipe = main_app.BREAD_RECIPES['Pandesal']
        cheese_bread_recipe = main_app.BREAD_RECIPES['Cheese Bread']
        
        # Cheese bread should need more flour
        pandesal_flour = pandesal_recipe.get('Flour (1st Class)', 0)
        cheese_flour = cheese_bread_recipe.get('Flour (1st Class)', 0)
        self.assertGreater(cheese_flour, pandesal_flour,
            "Cheese Bread should require more flour than Pandesal")


if __name__ == '__main__':
    unittest.main()
