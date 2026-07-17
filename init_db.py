#!/usr/bin/env python3
"""
Database initialization script for the prediction system.
Run this once to set up all required tables.
"""

import os
import sys
import mysql.connector

# Configuration (matches app.py)
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "prediction_system")

def create_database():
    """Create the database and tables"""
    try:
        # Connect without specifying database
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database
        print(f"Creating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
        
        # Connect to the database
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Create sales_data table
        print("Creating sales_data table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                bread_type VARCHAR(100) NOT NULL,
                products_produced INT NOT NULL DEFAULT 0,
                actual_qty_sold INT NOT NULL DEFAULT 0,
                waste_returns INT NOT NULL DEFAULT 0,
                price_per_product DECIMAL(10,2) NOT NULL DEFAULT 0.0,
                temperature DECIMAL(5,2) NOT NULL DEFAULT 30.0,
                is_holiday TINYINT(1) NOT NULL DEFAULT 0,
                is_promotion TINYINT(1) NOT NULL DEFAULT 0,
                sacks_used INT NOT NULL DEFAULT 0,
                plates_used INT NOT NULL DEFAULT 0,
                expense_amount DECIMAL(10,2) NOT NULL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_date (date),
                INDEX idx_bread_type (bread_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        
        # Create users table for login
        print("Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active TINYINT(1) DEFAULT 1,
                INDEX idx_username (username)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        
        # Create model_performance table
        print("Creating model_performance table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_performance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                training_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                r2_score DECIMAL(5,4) NOT NULL,
                mae DECIMAL(10,2) NOT NULL,
                accuracy INT NOT NULL,
                training_count INT NOT NULL,
                test_count INT NOT NULL,
                model_version INT DEFAULT 1,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_training_date (training_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()

        # Create monthly_expenses table
        print("Creating monthly_expenses table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scope_type ENUM('daily','weekly','monthly') NOT NULL DEFAULT 'monthly',
                period_key VARCHAR(20) NOT NULL,
                expense_month DATE NULL,
                category VARCHAR(100) NOT NULL,
                amount DECIMAL(12,2) NOT NULL DEFAULT 0.0,
                note VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_expense_scope (scope_type, period_key),
                INDEX idx_expense_month (expense_month),
                INDEX idx_category (category),
                UNIQUE KEY unique_scope_category (scope_type, period_key, category)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        
        # Create predictions table
        print("Creating predictions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bread_type VARCHAR(100) NOT NULL,
                prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_predicted DATE NOT NULL,
                temperature DECIMAL(5,2),
                is_holiday TINYINT(1) DEFAULT 0,
                is_promotion TINYINT(1) DEFAULT 0,
                predicted_demand INT NOT NULL,
                buffer INT DEFAULT 0,
                recommended_production INT NOT NULL,
                confidence INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_bread_type (bread_type),
                INDEX idx_date_predicted (date_predicted),
                INDEX idx_prediction_date (prediction_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        
        # Create production_plan table
        print("Creating production_plan table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS production_plan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                plan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                bread_type VARCHAR(100) NOT NULL,
                day_date DATE NOT NULL,
                planned_quantity INT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_plan_date (plan_date),
                INDEX idx_bread_type (bread_type),
                INDEX idx_day_date (day_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        
        # Insert default admin user
        print("Inserting default admin user...")
        cursor.execute("""
            INSERT IGNORE INTO users (username, password_hash, role) VALUES (%s, %s, %s)
        """, ('admin', '', 'admin'))
        conn.commit()
        
        # Insert sample monthly expenses
        print("Inserting sample monthly expenses...")
        sample_expenses = [
            ('2026-04-01', 'Ingredients', 2500.00, 'Flour, sugar, eggs, and other baking ingredients'),
            ('2026-04-01', 'Utilities', 800.00, 'Electricity and water bills'),
            ('2026-04-01', 'Rent', 1200.00, 'Monthly shop rent'),
            ('2026-04-01', 'Equipment', 300.00, 'Equipment maintenance and supplies'),
            ('2026-04-01', 'Marketing', 150.00, 'Advertising and promotions'),
            ('2026-04-01', 'Insurance', 200.00, 'Business insurance'),
            ('2026-04-01', 'Transportation', 100.00, 'Delivery and transportation costs'),
            ('2026-04-01', 'Other', 50.00, 'Other small expenses')
        ]
        cursor.executemany("""
            INSERT IGNORE INTO monthly_expenses (expense_month, category, amount, note) 
            VALUES (%s, %s, %s, %s)
        """, sample_expenses)
        conn.commit()
        
        print("\n✓ Database initialized successfully!")
        print(f"Database: {DB_NAME}")
        print(f"Host: {DB_HOST}:{DB_PORT}")
        print("\nTables created:")
        print("  - sales_data")
        print("  - users")
        print("  - model_performance")
        print("  - monthly_expenses")
        print("  - predictions")
        print("  - production_plan")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"✗ Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
