# Alpha Test Guide

## Purpose
This guide helps you validate the core features of the bakery prediction system before wider testing.

## 1. Setup
1. Start XAMPP and ensure MySQL is running.
2. Open a terminal in `c:\xampp\htdocs\prediction_system`.
3. Activate the Python virtual environment:
   - `venv\Scripts\Activate.ps1`
4. Confirm the app starts without errors.

## 2. Login and Navigation
1. Open the app in the browser.
2. Log in with your user credentials.
3. Confirm the navigation links work:
   - Dashboard
   - Predict Demand
   - Sales Log
   - Production Log
   - Ingredients
   - Model Performance
   - About

## 3. Sales Log Testing
### Clear existing sales data
1. Go to `Sales Log`.
2. Click `Clear All Sales`.
3. Confirm the prompt.
4. Expect the table to be empty and a success message.

### Upload CSV data
1. Click `Upload CSV`.
2. Select a valid sales CSV file.
3. Verify the upload success message.
4. Confirm new rows appear in the table.

### Add manual records
1. In `Manual Entry`, fill out a sales record.
2. Save the record.
3. Verify the record appears and totals update.

### Edit and delete records
1. Open a saved row with `Edit`.
2. Change values and save.
3. Confirm the update is reflected in the table.
4. Delete one record and verify it is removed.

## 4. Ingredient Inventory and Expenses
### Ingredient stock adjustments
1. Open `Ingredients`.
2. Use the stock `+` or `-` controls to adjust an ingredient.
3. Confirm stock and status update correctly.

### Expense scope and saving
1. Use the expense scope selector to choose `Daily`, `Weekly`, or `Monthly`.
2. Enter values for ingredient expense categories.
3. Save the expenses.
4. Confirm totals update and the success message appears.

### Expense clearing
1. Use `Clear Scope` after saving.
2. Confirm only the selected period is cleared.

## 5. Predict Demand and Production Log
### Generate a forecast
1. Go to `Predict Demand`.
2. Select a bread type, date, temperature, and optional holiday/promotion.
3. Generate forecast.
4. Confirm forecast results display.

### Production log history
1. Open `Production Log`.
2. Use the history page if available.
3. Confirm saved forecast records are listed.

## 6. Dashboard and Model Performance
### Dashboard validation
1. Open `Dashboard`.
2. Confirm totals and charts render.
3. Check for readable labels and subtitles.

### Model metrics
1. Open `Model Performance`.
2. Verify model metrics are present.
3. If supported, retrain the model and confirm the action works.

## 7. About Page Review
1. Open `About`.
2. Confirm the full-width background image displays.
3. Verify the hero text is legible.

## 8. Bug Reporting Template
For any issue, capture:
- Action taken
- Expected behavior
- Actual behavior
- Screenshots or messages if available

Example:
- Action: Uploaded `sales.csv`
- Expected: 24 records imported
- Actual: 12 records imported, no error shown

## 9. Final Notes
- Always clear the sales log before a new upload cycle.
- Test first with small sample data, then larger datasets.
- Document any UI or data inconsistencies.
