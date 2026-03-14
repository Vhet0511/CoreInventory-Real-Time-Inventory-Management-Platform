# Database Schema Documentation

**Database:** PostgreSQL 18.3  
**Schema:** `public`  
**Dumped on:** 2026-03-14  

---

## Overview

This database supports a **Warehouse Management System (WMS)**. It handles user authentication, product cataloguing, warehouse and location management, inventory tracking, stock movements (receipts, deliveries, transfers), and audit logging via a stock ledger.

---

## Table of Contents

1. [users](#1-users)
2. [password_reset_otp](#2-password_reset_otp)
3. [product_categories](#3-product_categories)
4. [units_of_measure](#4-units_of_measure)
5. [products](#5-products)
6. [warehouses](#6-warehouses)
7. [locations](#7-locations)
8. [inventory_stock](#8-inventory_stock)
9. [stock_ledger](#9-stock_ledger)
10. [receipts](#10-receipts)
11. [receipt_items](#11-receipt_items)
12. [deliveries](#12-deliveries)
13. [delivery_items](#13-delivery_items)
14. [transfers](#14-transfers)
15. [transfer_items](#15-transfer_items)
16. [stock_adjustments](#16-stock_adjustments)
17. [Entity Relationship Summary](#entity-relationship-summary)
18. [Foreign Key Constraints](#foreign-key-constraints)

---

## Tables

### 1. `users`

Stores all system users including warehouse managers and operators.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique user identifier |
| `name` | `varchar(100)` | | Full name of the user |
| `email` | `varchar(150)` | UNIQUE | User's email address (used for login) |
| `password_hash` | `text` | | Hashed password string |
| `role` | `varchar(50)` | | Role of the user (e.g., admin, manager, operator) |
| `created_at` | `timestamp` | | Account creation timestamp |

---

### 2. `password_reset_otp`

Manages OTP (one-time password) codes used for password reset flows.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique OTP record identifier |
| `user_id` | `integer` | FK → `users.id` (CASCADE DELETE), NOT NULL | The user requesting the reset |
| `otp_code` | `varchar(6)` | NOT NULL | The 6-character OTP code |
| `created_at` | `timestamp` | | When the OTP was generated |
| `expires_at` | `timestamp` | | When the OTP expires |

> OTP records are automatically deleted when the associated user is deleted.

---

### 3. `product_categories`

Lookup table for grouping products into categories.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique category identifier |
| `name` | `varchar(100)` | | Category name |
| `description` | `text` | | Optional description of the category |

---

### 4. `units_of_measure`

Lookup table for product measurement units (e.g., kg, litre, piece).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique unit identifier |
| `name` | `varchar(50)` | | Full unit name (e.g., "Kilogram") |
| `symbol` | `varchar(10)` | | Short symbol (e.g., "kg") |

---

### 5. `products`

Master catalogue of all products tracked in the system.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique product identifier |
| `name` | `varchar(150)` | | Product name |
| `sku` | `varchar(100)` | UNIQUE | Stock Keeping Unit — unique product code |
| `category_id` | `integer` | FK → `product_categories.id` (RESTRICT), NOT NULL | Product's category |
| `unit_id` | `integer` | FK → `units_of_measure.id` (RESTRICT), NOT NULL | Measurement unit for this product |
| `reorder_level` | `integer` | | Minimum stock quantity before reordering is triggered |
| `created_at` | `timestamp` | | Record creation timestamp |

> Deleting a category or unit that is still in use by a product is prevented (`RESTRICT`).

---

### 6. `warehouses`

Represents physical warehouse locations in the system.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique warehouse identifier |
| `name` | `varchar(150)` | | Warehouse name |
| `address` | `text` | | Physical address of the warehouse |
| `manager_id` | `integer` | FK → `users.id` (SET NULL), NOT NULL | Assigned manager user |
| `created_at` | `timestamp` | | Record creation timestamp |

> If a manager user is deleted, the `manager_id` is set to `NULL` rather than deleting the warehouse.

---

### 7. `locations`

Represents specific zones or bins within a warehouse (e.g., Aisle A, Rack 3).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique location identifier |
| `warehouse_id` | `integer` | FK → `warehouses.id` (RESTRICT), NOT NULL | The parent warehouse |
| `name` | `varchar(100)` | | Location name/label |
| `type` | `varchar(50)` | | Location type (e.g., rack, bin, aisle) |

---

### 8. `inventory_stock`

Tracks the current quantity of each product at each warehouse location.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique stock record identifier |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The product being tracked |
| `location_id` | `integer` | FK → `locations.id`, NOT NULL | The location storing the product |
| `quantity` | `numeric(10,2)` | | Current stock quantity |
| `updated_at` | `timestamp` | | Last time this stock level was updated |

---

### 9. `stock_ledger`

Append-only audit log of every stock movement — provides a full history of all inventory changes.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique ledger entry identifier |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The product involved |
| `location_id` | `integer` | FK → `locations.id`, NOT NULL | The location affected |
| `change_qty` | `numeric(10,2)` | | Quantity change (positive = in, negative = out) |
| `operation_type` | `varchar(50)` | | Type of operation (e.g., receipt, delivery, transfer, adjustment) |
| `reference_id` | `integer` | | ID of the source transaction (receipt, delivery, etc.) |
| `created_at` | `timestamp` | | When this ledger entry was created |

---

### 10. `receipts`

Header record for inbound stock deliveries from suppliers.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique receipt identifier |
| `supplier_name` | `varchar(150)` | | Name of the supplier |
| `warehouse_id` | `integer` | FK → `warehouses.id`, NOT NULL | Destination warehouse |
| `status` | `varchar(50)` | | Receipt status (e.g., pending, completed) |
| `created_by` | `integer` | FK → `users.id`, NOT NULL | User who created the receipt |
| `created_at` | `timestamp` | | Record creation timestamp |

---

### 11. `receipt_items`

Line items for each receipt — records which products were received and in what quantities.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique receipt item identifier |
| `receipt_id` | `integer` | FK → `receipts.id` (CASCADE DELETE), NOT NULL | Parent receipt |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The received product |
| `location_id` | `integer` | FK → `locations.id`, NOT NULL | Location where product was placed |
| `quantity` | `numeric(10,2)` | | Quantity received |

> Receipt items are automatically deleted if the parent receipt is deleted.

---

### 12. `deliveries`

Header record for outbound stock dispatches to customers.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique delivery identifier |
| `customer_name` | `varchar(150)` | | Name of the customer |
| `warehouse_id` | `integer` | FK → `warehouses.id`, NOT NULL | Source warehouse |
| `status` | `varchar(50)` | | Delivery status (e.g., pending, dispatched) |
| `created_at` | `timestamp` | | Record creation timestamp |

---

### 13. `delivery_items`

Line items for each delivery — records which products were dispatched and in what quantities.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique delivery item identifier |
| `delivery_id` | `integer` | FK → `deliveries.id` (CASCADE DELETE), NOT NULL | Parent delivery |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The dispatched product |
| `location_id` | `integer` | FK → `locations.id`, NOT NULL | Location from which product was taken |
| `quantity` | `numeric(10,2)` | | Quantity dispatched |

> Delivery items are automatically deleted if the parent delivery is deleted.

---

### 14. `transfers`

Header record for internal stock transfers between two locations (within or across warehouses).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique transfer identifier |
| `from_location` | `integer` | FK → `locations.id`, NOT NULL | Source location |
| `to_location` | `integer` | FK → `locations.id`, NOT NULL | Destination location |
| `status` | `varchar(50)` | DEFAULT `'pending'` | Transfer status (e.g., pending, completed) |
| `created_by` | `integer` | FK → `users.id`, NOT NULL | User who initiated the transfer |
| `created_at` | `timestamp` | DEFAULT `CURRENT_TIMESTAMP` | Record creation timestamp |

> **Constraint:** `check_locations_distinct` ensures `from_location ≠ to_location` — a transfer must be between two different locations.

---

### 15. `transfer_items`

Line items for each transfer — records which products were moved and in what quantities.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique transfer item identifier |
| `transfer_id` | `integer` | FK → `transfers.id` (CASCADE DELETE), NOT NULL | Parent transfer |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The product being moved |
| `quantity` | `numeric(10,2)` | | Quantity being transferred |

> Transfer items are automatically deleted if the parent transfer is deleted.

---

### 16. `stock_adjustments`

Records manual corrections to inventory (e.g., due to damage, counting errors, shrinkage).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | PK, NOT NULL, auto-increment | Unique adjustment identifier |
| `product_id` | `integer` | FK → `products.id`, NOT NULL | The product being adjusted |
| `location_id` | `integer` | FK → `locations.id`, NOT NULL | Location of the adjustment |
| `adjustment_qty` | `numeric(10,2)` | NOT NULL | Quantity change (positive or negative) |
| `reason` | `text` | | Reason/note for the adjustment |
| `created_by` | `integer` | FK → `users.id`, NOT NULL | User who made the adjustment |
| `created_at` | `timestamp` | DEFAULT `CURRENT_TIMESTAMP` | When the adjustment was recorded |

---

## Entity Relationship Summary

```
users
 ├── password_reset_otp      (1 user → many OTPs)
 ├── warehouses (manager)    (1 user → many warehouses as manager)
 ├── receipts (created_by)   (1 user → many receipts)
 ├── transfers (created_by)  (1 user → many transfers)
 └── stock_adjustments       (1 user → many adjustments)

product_categories
 └── products                (1 category → many products)

units_of_measure
 └── products                (1 unit → many products)

products
 ├── inventory_stock         (1 product → many stock records)
 ├── stock_ledger            (1 product → many ledger entries)
 ├── receipt_items           (1 product → many receipt lines)
 ├── delivery_items          (1 product → many delivery lines)
 ├── transfer_items          (1 product → many transfer lines)
 └── stock_adjustments       (1 product → many adjustments)

warehouses
 ├── locations               (1 warehouse → many locations)
 ├── receipts                (1 warehouse → many receipts)
 └── deliveries              (1 warehouse → many deliveries)

locations
 ├── inventory_stock         (1 location → many stock records)
 ├── stock_ledger            (1 location → many ledger entries)
 ├── receipt_items           (1 location → many receipt lines)
 ├── delivery_items          (1 location → many delivery lines)
 ├── transfers (from/to)     (1 location → many transfers as source/destination)
 └── stock_adjustments       (1 location → many adjustments)

receipts
 └── receipt_items           (1 receipt → many items, CASCADE DELETE)

deliveries
 └── delivery_items          (1 delivery → many items, CASCADE DELETE)

transfers
 └── transfer_items          (1 transfer → many items, CASCADE DELETE)
```

---

## Foreign Key Constraints

| Constraint Name | Table | Column | References | On Delete |
|---|---|---|---|---|
| `fk_otp_user` | `password_reset_otp` | `user_id` | `users.id` | CASCADE |
| `fk_product_category` | `products` | `category_id` | `product_categories.id` | RESTRICT |
| `fk_product_unit` | `products` | `unit_id` | `units_of_measure.id` | RESTRICT |
| `fk_warehouses_manager` | `warehouses` | `manager_id` | `users.id` | SET NULL |
| `fk_deliveries_warehouse` | `locations` | `warehouse_id` | `warehouses.id` | RESTRICT |
| `fk_product` | `inventory_stock` | `product_id` | `products.id` | — |
| `fk_location` | `inventory_stock` | `location_id` | `locations.id` | — |
| `fk_product` | `stock_ledger` | `product_id` | `products.id` | — |
| `fk_location` | `stock_ledger` | `location_id` | `locations.id` | — |
| `fk_user` | `receipts` | `created_by` | `users.id` | — |
| `fk_warehouse` | `receipts` | `warehouse_id` | `warehouses.id` | — |
| `fk_receipt` | `receipt_items` | `receipt_id` | `receipts.id` | CASCADE |
| `fk_product` | `receipt_items` | `product_id` | `products.id` | — |
| `fk_location` | `receipt_items` | `location_id` | `locations.id` | — |
| `fk_warehouse` | `deliveries` | `warehouse_id` | `warehouses.id` | — |
| `fk_delivery` | `delivery_items` | `delivery_id` | `deliveries.id` | CASCADE |
| `fk_delivery_product` | `delivery_items` | `product_id` | `products.id` | — |
| `fk_delivery_location` | `delivery_items` | `location_id` | `locations.id` | — |
| `fk_transfer_from` | `transfers` | `from_location` | `locations.id` | — |
| `fk_transfer_to` | `transfers` | `to_location` | `locations.id` | — |
| `fk_transfer_user` | `transfers` | `created_by` | `users.id` | — |
| `fk_transfer_header` | `transfer_items` | `transfer_id` | `transfers.id` | CASCADE |
| `fk_transfer_product` | `transfer_items` | `product_id` | `products.id` | — |
| `fk_adj_product` | `stock_adjustments` | `product_id` | `products.id` | — |
| `fk_adj_location` | `stock_adjustments` | `location_id` | `locations.id` | — |
| `fk_adj_user` | `stock_adjustments` | `created_by` | `users.id` | — |

---

*Documentation generated from `schema.sql` — PostgreSQL 18.3 dump dated 2026-03-14.*