-- Schema-only export for prediction_system
-- No data inserts included

CREATE DATABASE IF NOT EXISTS `prediction_system`;
USE `prediction_system`;

CREATE TABLE `ingredients` (

  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `current_stock` decimal(14,4) NOT NULL DEFAULT 0.0000,
  `unit` varchar(50) NOT NULL DEFAULT '',
  `reorder_threshold` decimal(14,4) NOT NULL DEFAULT 0.0000,
  `last_restock` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `ingredient_transactions` (

  `id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `change_amount` decimal(14,4) NOT NULL,
  `transaction_type` enum('in','out') NOT NULL,
  `note` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `inventory` (

  `id` int(11) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `reorder_threshold` int(11) NOT NULL DEFAULT 5,
  `unit` varchar(50) DEFAULT '',
  `last_restock` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `inventory_items` (

  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `unit` varchar(50) DEFAULT 'pcs',
  `current_stock` decimal(12,3) NOT NULL DEFAULT 0.000,
  `low_stock_threshold` decimal(12,3) NOT NULL DEFAULT 0.000,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `inventory_transactions` (

  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `transaction_date` datetime DEFAULT current_timestamp(),
  `transaction_type` enum('in','out') NOT NULL,
  `quantity` decimal(12,3) NOT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `note` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `model_performance` (

  `id` int(11) NOT NULL,
  `training_date` datetime DEFAULT current_timestamp(),
  `r2_score` decimal(5,4) NOT NULL,
  `mae` decimal(10,2) NOT NULL,
  `accuracy` int(11) NOT NULL,
  `training_count` int(11) NOT NULL,
  `test_count` int(11) NOT NULL,
  `model_version` int(11) DEFAULT 1,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `monthly_expenses` (

  `id` int(11) NOT NULL,
  `expense_month` date NOT NULL,
  `category` varchar(100) NOT NULL,
  `amount` decimal(12,2) NOT NULL DEFAULT 0.00,
  `note` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `scope_type` enum('daily','weekly','monthly') NOT NULL DEFAULT 'monthly',
  `period_key` varchar(20) NOT NULL DEFAULT 'monthly'

);

CREATE TABLE `predictions` (

  `id` int(11) NOT NULL,
  `bread_type` varchar(100) NOT NULL,
  `prediction_date` datetime DEFAULT current_timestamp(),
  `date_predicted` date NOT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  `is_holiday` tinyint(1) DEFAULT 0,
  `is_promotion` tinyint(1) DEFAULT 0,
  `predicted_demand` int(11) NOT NULL,
  `buffer` int(11) DEFAULT 0,
  `recommended_production` int(11) NOT NULL,
  `confidence` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `actual_production` int(11) NOT NULL DEFAULT 0,
  `sold` int(11) NOT NULL DEFAULT 0,
  `waste` int(11) NOT NULL DEFAULT 0

);

CREATE TABLE `production_plan` (

  `id` int(11) NOT NULL,
  `plan_date` datetime DEFAULT current_timestamp(),
  `bread_type` varchar(100) NOT NULL,
  `day_date` date NOT NULL,
  `planned_quantity` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `actual_quantity` int(11) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL

);

CREATE TABLE `raw_sales_uploads` (

  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `bread_type` varchar(200) DEFAULT NULL,
  `products_produced` int(11) DEFAULT 0,
  `actual_qty_sold` int(11) DEFAULT 0,
  `waste_returns` int(11) DEFAULT 0,
  `price_per_product` decimal(10,2) DEFAULT 0.00,
  `temperature` decimal(5,2) DEFAULT 30.00,
  `is_holiday` tinyint(1) DEFAULT 0,
  `is_promotion` tinyint(1) DEFAULT 0,
  `sacks_used` int(11) DEFAULT 0,
  `plates_used` int(11) DEFAULT 0,
  `expense_amount` decimal(10,2) DEFAULT 0.00,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `recipes` (

  `id` int(11) NOT NULL,
  `bread_type` varchar(100) NOT NULL,
  `ingredient_name` varchar(255) NOT NULL,
  `qty_per_unit` decimal(12,6) NOT NULL DEFAULT 0.000000,
  `unit` varchar(50) DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()

);

CREATE TABLE `sales_data` (

  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `bread_type` varchar(100) NOT NULL,
  `products_produced` int(11) NOT NULL DEFAULT 0,
  `actual_qty_sold` int(11) NOT NULL DEFAULT 0,
  `waste_returns` int(11) NOT NULL DEFAULT 0,
  `price_per_product` decimal(10,2) NOT NULL DEFAULT 0.00,
  `temperature` decimal(5,2) NOT NULL DEFAULT 30.00,
  `is_holiday` tinyint(1) NOT NULL DEFAULT 0,
  `is_promotion` tinyint(1) NOT NULL DEFAULT 0,
  `sacks_used` int(11) NOT NULL DEFAULT 0,
  `plates_used` int(11) NOT NULL DEFAULT 0,
  `expense_amount` decimal(10,2) NOT NULL DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `bad_waste` int(11) NOT NULL DEFAULT 0,
  `good_waste` int(11) NOT NULL DEFAULT 0

);

CREATE TABLE `users` (

  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(50) DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1

);
