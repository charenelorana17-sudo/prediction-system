# How to Use Automatic Ingredient Deduction

## Quick Start

Once you log a sale (either manually or via CSV), ingredients are **automatically deducted** from your inventory. No extra steps needed!

## Manual Sales Entry

### Steps:
1. Go to **Sales Log** page
2. Fill in the form:
   - **Date**: Date of sale
   - **Bread Type**: Which bread you sold (e.g., "Pandesal")
   - **Produced**: Units produced
   - **Sold**: Units sold (THIS QUANTITY TRIGGERS AUTO-DEDUCTION)
   - **Price**: Price per unit
3. Click **"Add Record"**
4. You'll see a message like:
   ```
   ✓ Manual record saved successfully. 
   ⚠️ Flour (1st Class): Stock at 42 kg - Below reorder threshold of 50 kg
   ```

### What Happens Behind the Scenes:
- **100 units of Pandesal sold** 
- System calculates: 0.08 kg flour × 100 = 8 kg flour needed
- Your flour stock automatically reduced by 8 kg
- Deduction logged with timestamp
- If stock falls below threshold, you get a warning

## CSV Upload

### Steps:
1. Go to **Sales Log** page
2. Click **"Upload CSV"**
3. Select your CSV file with sales data
4. Click **"Upload"**
5. System processes all records and auto-deducts for each:
   ```
   ✓ 50 record(s) uploaded successfully. 
   ⚠️ Flour: Below threshold | ⚠️ Sugar: Below threshold
   ```

### CSV Format:
Required columns:
- `date` (YYYY-MM-DD)
- `bread_type` (e.g., "Pandesal", "Cheese Bread")
- `actual_qty_sold` (the quantity that triggers deduction)
- `products_produced`
- `price_per_product`

Example:
```
date,bread_type,products_produced,actual_qty_sold,price_per_product
2025-01-15,Pandesal,200,185,4.5
2025-01-15,Cheese Bread,150,140,6.0
2025-01-16,Ensaymada,100,95,7.5
```

## Monitoring Your Inventory

### Check Current Stock:
1. Go to **Ingredients** page
2. See all ingredients with current stock levels
3. **Color coding:**
   - 🟢 Green: In Stock (above threshold)
   - 🟡 Yellow: Below Threshold - time to reorder
   - 🔴 Red: Out of Stock or critically low

### View Deduction History:
1. Go to **Ingredients** page
2. Each ingredient shows: **Last Restock** date
3. Stock changes are logged automatically with timestamps

## Understanding the Warnings

### Low-Stock Warning Format:
```
⚠️ Flour (1st Class) (sack): Stock at 42 - Below reorder threshold of 50
```

Breaking it down:
- **⚠️** = Warning indicator
- **Flour (1st Class)** = Ingredient name
- **(sack)** = Unit of measurement
- **Stock at 42** = Current inventory level
- **reorder threshold of 50** = When you want to reorder

### What to Do:
1. **See a warning?** → Reorder that ingredient
2. Click **"Stock In"** button next to the ingredient
3. Enter the amount received
4. Click **"Update"**

## Recipes Used for Deduction

The system uses these ingredient requirements per bread unit:

### Pandesal
- Flour (1st Class): 0.08 kg
- Sugar: 0.005 kg
- Vegetable Oil: 0.003 kg
- Margarine: 0.002 kg
- Yeast: 0.001 kg
- Salt: 0.0005 kg
- Baking Powder: 0.0005 kg

### Cheese Bread
- Flour (1st Class): 0.1 kg (more than Pandesal!)
- Sugar: 0.007 kg
- Vegetable Oil: 0.004 kg
- Margarine: 0.003 kg
- Yeast: 0.0015 kg
- Salt: 0.0005 kg
- Baking Powder: 0.0008 kg

### Ensaymada
- Flour (1st Class): 0.12 kg
- Sugar: 0.015 kg
- Vegetable Oil: 0.005 kg
- Margarine: 0.008 kg
- Lard: 0.004 kg
- Yeast: 0.002 kg
- Salt: 0.0008 kg

### Mamon
- Flour (3rd Class): 0.06 kg
- Sugar: 0.04 kg
- Vegetable Oil: 0.025 kg
- Baking Powder: 0.005 kg
- Salt: 0.0005 kg

### Burger Buns
- Flour (1st Class): 0.15 kg
- Sugar: 0.01 kg
- Vegetable Oil: 0.005 kg
- Margarine: 0.004 kg
- Yeast: 0.002 kg
- Salt: 0.0008 kg
- Baking Powder: 0.001 kg

## Example: Daily Operations

### Morning (7 AM):
1. You check ingredients - all levels OK
2. You start production: 200 Pandesal, 150 Cheese Bread

### Mid-Day (12 PM):
1. You've sold 180 Pandesal
2. Go to Sales Log → Add Record
3. Bread Type: "Pandesal"
4. Sold: 180 units
5. Click "Add Record"
6. **System automatically:**
   - Deducts: 0.08 kg × 180 = 14.4 kg flour
   - Updates: Flour stock from 50 kg → 35.6 kg
   - Logs: Transaction showing "Auto-deduction: 180 units of Pandesal sold"

### Afternoon (3 PM):
1. You've sold 140 Cheese Bread
2. Add another record
3. **System automatically:**
   - Deducts: 0.1 kg × 140 = 14 kg flour
   - Updates: Flour stock from 35.6 kg → 21.6 kg
   - Warns: "⚠️ Flour (1st Class): Stock at 21.6 - Below reorder threshold of 50"

### End of Day:
1. Check Ingredients page
2. See Flour is low - **red status**
3. Call your supplier to reorder
4. When flour arrives, click "Stock In" to update inventory

## Troubleshooting

### Q: I logged a sale but inventory didn't change
**A:** 
- Check if the bread type is in the system recipes
- If using unmapped bread type, system skips deduction (shows warning)
- Make sure you entered "Sold" quantity (not "Produced")

### Q: I see a warning but don't know my reorder threshold
**A:**
- Go to Ingredients page
- Click the ingredient name to see settings
- Adjust "Reorder Threshold" if needed
- That's the minimum stock level that triggers warnings

### Q: How do I change the recipe quantities?
**A:**
- Contact your admin/developer
- Recipes are defined in the application settings
- Can be customized without affecting your data

### Q: Can I see the history of all deductions?
**A:**
- Not yet in the UI, but data is logged in the database
- Each deduction is recorded with timestamp and reason
- Contact admin if you need a detailed audit report

## Best Practices

1. **Log sales as soon as possible** - This keeps inventory accurate
2. **Set realistic reorder thresholds** - Based on your sales volume and supplier lead time
3. **Check inventory daily** - Monitor the Ingredients page every morning
4. **Act on warnings** - Reorder when you see yellow/red status
5. **Use consistent bread names** - Spelling matters ("Pandesal" not "pandesal" or "Pansdesal")

## Support

If something isn't working:
1. Check the Sales Log message - it shows what happened
2. Go to Ingredients page and verify stock levels updated
3. Review your recipe quantities - they should match your actual baking process
