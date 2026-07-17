# Quick Start: Automatic Ingredient Deduction

## The Problem You Had
❌ You logged sales in your system, but ingredients had to be manually reduced from inventory
❌ This meant duplicate work and easy to forget
❌ Your ingredient stock didn't match actual production/sales

## The Solution We Built
✅ Now when you log a sale, ingredients automatically deduct from inventory
✅ No extra steps - it happens in the background
✅ You get warnings when stock gets low
✅ Everything is logged for your records

## How to Use It (3 Steps)

### Step 1: Log a Sale
Go to **Sales Log** page and add a record:
- Date: 2025-01-15
- Bread Type: **Pandesal**
- Produced: 200
- **Sold: 100** ← This number triggers ingredient deduction
- Price: 4.5
- Click **"Add Record"**

### Step 2: See the Magic
You'll see a message like:
```
✓ Manual record saved successfully.
⚠️ Flour (1st Class): Stock at 42 - Below reorder threshold of 50
```

### Step 3: Check Your Inventory
Go to **Ingredients** page - you'll see flour stock decreased from 50 to 42!

---

## What Happened Behind the Scenes

When you logged 100 Pandesal sold:

```
System looked up: "How much flour in 1 Pandesal?"
Answer from recipe: 0.08 kg

Calculated: 0.08 kg × 100 units = 8 kg flour needed

Updated database: Flour stock = 50 kg → 42 kg

Logged action: "Auto-deduction: 100 units of Pandesal sold" 
               with timestamp: 2025-01-15 14:32:50

Checked threshold: Is 42 < 50 (reorder threshold)? YES!
Added warning: "Below reorder threshold of 50"
```

---

## For Bulk Uploads

If you upload a CSV with 50 sales records, the system:
1. Processes each record
2. **Automatically deducts ingredients for each sale**
3. Shows you all warnings at once

Example result:
```
✓ 50 record(s) uploaded successfully.
⚠️ Flour: Below threshold | ⚠️ Sugar: Below threshold | ⚠️ Oil: Below threshold
```

---

## What Gets Tracked

Every automatic deduction is logged in your database with:
- **What**: Ingredient name (e.g., "Flour (1st Class)")
- **How much**: Amount deducted (e.g., 8 kg)
- **Why**: Reason (e.g., "100 units of Pandesal sold")
- **When**: Exact timestamp

You can review this history anytime (contact admin for detailed reports).

---

## Supported Bread Types with Recipes

These breads already have their recipes configured:
- ✅ Pandesal
- ✅ Cheese Bread
- ✅ Ensaymada
- ✅ Mamon
- ✅ Burger Buns
- ❌ Other types (recipes can be added)

If you try to log a sale for a bread without a recipe:
```
⚠️ No recipe found for [Bread Name]. Skipping ingredient deduction.
```
(Sale is still saved, just no auto-deduction)

---

## Understanding Your Warnings

### Yellow Alert (Below Threshold)
```
⚠️ Flour (1st Class): Stock at 42 - Below reorder threshold of 50
```
**What it means**: You still have stock, but it's below your reorder level
**What to do**: Reorder from your supplier (click "Stock In" when it arrives)

### Red Alert (Out of Stock)
```
⚠️ Flour (1st Class): Stock at 0 - Below reorder threshold of 50
```
**What it means**: You're completely out
**What to do**: URGENT - Reorder immediately!

---

## Real Example: A Day in Your Bakery

**8:00 AM** - Ingredients look good
- Flour: 50 kg ✓
- Sugar: 20 kg ✓
- Oil: 10 liters ✓

**12:00 PM** - You sold 100 Pandesal
- You go to Sales Log → Add Record
- Bread Type: Pandesal, Sold: 100
- Click "Add Record"
- System automatically deducts 8 kg flour

**12:01 PM** - You see the message
- ✓ Record saved successfully
- ⚠️ Flour: Stock at 42 - Below reorder threshold
- Flour is now 42 kg (was 50 kg)

**2:00 PM** - You sold 140 Cheese Bread
- Add another record
- Bread Type: Cheese Bread, Sold: 140
- System automatically deducts 14 kg flour (0.1 kg × 140)
- Flour is now 28 kg

**3:00 PM** - Check Ingredients page
- Flour: 28 kg (RED - below 50) → Call supplier!
- Sugar: 20 kg (GREEN - still OK)
- Oil: 10 L (GREEN - still OK)

**3:30 PM** - Flour arrives
- Click "Stock In" for Flour
- Enter: +50 kg received
- Flour now: 28 + 50 = 78 kg (back to GREEN)

---

## FAQ

**Q: Will this affect my existing sales data?**
A: No! This only auto-deducts going forward when you log NEW sales.

**Q: Can I turn it off?**
A: Currently no, but the deduction logic can be disabled by removing the function call. Contact admin if needed.

**Q: What if a recipe is wrong?**
A: You'll see the effects (inventory wrong). Contact admin to adjust recipes in app.py.

**Q: Does it work with my inventory manual adjustments?**
A: Yes! Manual +/- buttons still work, plus this automatic system on top.

**Q: What if I need different recipes for different seasons?**
A: Currently recipes are fixed. This could be added as a future enhancement.

---

## Troubleshooting

### Ingredients didn't decrease
1. Check if you entered the **Sold** quantity (not Produced)
2. Check if the bread type has a recipe (see list above)
3. Check Ingredients page to see if it actually decreased
4. If still wrong, contact admin

### I see a warning but not sure what to do
1. **Yellow** = Reorder soon
2. **Red** = Reorder NOW
3. Use "Stock In" button to add new inventory when it arrives

### I want to add recipes for more bread types
Contact your admin/developer to add new recipes to the system

---

## The Bottom Line

**Before**: Manual logging → Manually remember to reduce ingredients → Easy to forget/make mistakes

**Now**: Log sale → Ingredients automatically reduce → You get notified of low stock → Simple!

That's it! Start logging your sales and watch your inventory stay accurate automatically. 🎉
