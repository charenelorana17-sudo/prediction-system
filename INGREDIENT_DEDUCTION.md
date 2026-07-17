# Automatic Ingredient Deduction System

## Overview

The automatic ingredient deduction system automatically reduces ingredient inventory when sales are logged. This ensures your ingredient stock stays synchronized with actual sales without manual intervention.

## How It Works

### 1. **Bread-to-Recipe Mapping**

Each bread type has a defined recipe showing how much of each ingredient is needed per unit produced:

```python
BREAD_RECIPES = {
    'Pandesal': {
        'Flour (1st Class)': 0.08,      # kg per unit
        'Sugar': 0.005,
        'Vegetable Oil': 0.003,
        'Margarine': 0.002,
        'Yeast': 0.001,
        'Salt': 0.0005,
        'Baking Powder': 0.0005,
    },
    'Cheese Bread': {
        'Flour (1st Class)': 0.1,
        'Sugar': 0.007,
        # ... more ingredients
    },
    # ... more bread types
}
```

### 2. **Automatic Deduction on Sale**

When you log a sale, the system:

1. **Identifies the recipe** for that bread type
2. **Calculates total consumption**: quantity_per_unit × units_sold
3. **Updates ingredient stock**: Reduces `current_stock` in the database
4. **Logs transaction**: Records the deduction in `ingredient_transactions` table
5. **Checks thresholds**: Alerts if stock falls below reorder threshold

### 3. **Workflow**

```
User logs sale (100 units of Pandesal)
        ↓
save_sales_record() saves to database
        ↓
reduce_ingredients_for_sale() called
        ↓
For each ingredient in recipe:
   - Calculate: 0.08 kg (per unit) × 100 = 8 kg flour needed
   - Deduct from inventory
   - Log transaction
   - Check if below reorder threshold
        ↓
Display warnings for low-stock items
```

## Implementation Details

### Function: `reduce_ingredients_for_sale()`

```python
def reduce_ingredients_for_sale(bread_type, quantity_sold):
    """
    Automatically deduct ingredients from inventory when a sale is logged.
    
    Args:
        bread_type: The type of bread sold (e.g., 'Pandesal')
        quantity_sold: The quantity of units sold
    
    Returns:
        {'success': bool, 'warnings': [list of low-stock warnings]}
    """
```

**Called in:**
- `/sales_log` route when manually adding a record
- `/sales_log` route when uploading CSV files

### Database Tables Used

1. **ingredients** - Updated with new `current_stock`
2. **ingredient_transactions** - Records the deduction with reason
3. **sales_data** - Unchanged (normal sales logging)

## Features

### ✅ Automatic Stock Reduction
- Ingredients automatically deduct based on sales quantities
- Works with both manual entry and CSV uploads

### ✅ Transaction Logging
- Every deduction is recorded in `ingredient_transactions`
- Reason stored: "Auto-deduction: X units of [bread_type] sold"
- Timestamp recorded automatically

### ✅ Low-Stock Alerts
- System checks if stock falls below reorder threshold
- Warnings displayed in the UI message
- Format: `⚠️ Ingredient (unit): Stock at X - Below reorder threshold of Y`

### ✅ Configurable Recipes
- Easily adjust ingredient quantities per bread type
- Add new bread types with their recipes
- Quantities in standard units (kg, containers, etc.)

## Configuration

### Adding/Modifying Recipes

Edit `BREAD_RECIPES` dictionary in `app.py`:

```python
BREAD_RECIPES = {
    'Your Bread Name': {
        'Flour (1st Class)': 0.10,          # kg per unit
        'Sugar': 0.008,
        'Vegetable Oil': 0.004,
        'Margarine': 0.003,
        'Yeast': 0.002,
        'Salt': 0.0008,
    },
}
```

### Supported Ingredients

The system works with the standard ingredient list:
- Flour (1st Class)
- Flour (3rd Class)
- Sugar
- Vegetable Oil
- Margarine
- Lard
- Butter Milk
- Yeast
- Salt
- Baking Powder
- Anti-Amag
- Amoniaco

## Example Scenarios

### Scenario 1: Manual Sale Entry
1. User navigates to Sales Log
2. Enters: Date, Bread Type (Pandesal), Sold (100 units)
3. Clicks "Add Record"
4. System:
   - Saves sale record
   - Calculates: 0.08 kg × 100 = 8 kg flour needed
   - Reduces flour stock by 8 kg
   - Logs transaction with timestamp
   - Checks thresholds
   - Shows: "Manual record saved successfully. ⚠️ Flour (1st Class): Stock at 42 kg - Below reorder threshold of 50 kg"

### Scenario 2: CSV Upload
1. User uploads CSV with 50 sales records
2. System processes each record and deducts ingredients automatically
3. If any records cause low-stock warnings, they're displayed collectively

## Monitoring & Feedback

### User Feedback Messages

**Success:** 
```
Manual record saved successfully.
```

**With Warnings:**
```
Manual record saved successfully. ⚠️ Flour (1st Class): Stock at 42 kg - Below reorder threshold
```

**Batch Upload:**
```
50 record(s) uploaded successfully. ⚠️ Flour: Below threshold | ⚠️ Sugar: Below threshold
```

### Ingredient Transactions Table

View all automatic deductions:
- Date/Time of deduction
- Ingredient affected
- Amount deducted
- Reason ("Auto-deduction: X units of Pandesal sold")

## Technical Notes

- **Database Requirement**: MySQL connection required (not available in memory-only mode)
- **Transaction Safety**: Uses MySQL transaction commits to ensure data consistency
- **Error Handling**: If ingredient not found or DB error occurs, warning logged but sale still recorded
- **Performance**: Minimal overhead - one query per ingredient in recipe

## Testing

Run tests to verify the system:

```bash
python -m unittest tests.test_auto_ingredient_deduction -v
```

**Test Coverage:**
- Recipe definitions exist for all major bread types
- Recipes contain realistic ingredient quantities
- Ingredient calculations are correct
- Recipe quantities are positive numbers

## Future Enhancements

Possible improvements to consider:
1. **Bulk Recipe Editor** - UI to manage recipes without code changes
2. **Historical Stock Levels** - Track inventory changes over time
3. **Automated Reordering** - Alert system for reorder management
4. **Recipe Variants** - Different recipes based on season/promotion
5. **Ingredient Waste Tracking** - Separate tracking for waste vs. sales
