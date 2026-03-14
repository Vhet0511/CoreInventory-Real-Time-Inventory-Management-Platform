# 📦 CoreInventory

> A modular, real-time Inventory Management System designed to digitize and streamline all stock-related operations within a business — replacing manual registers, Excel sheets, and scattered tracking methods with a centralized, easy-to-use application.

---

## 🎥 Demo Video

> **[Will be added soon]**

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Target Users](#target-users)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Tables](#database-tables)
- [HTML Pages](#html-pages)
- [Backend APIs](#backend-apis)
- [Inventory Flow](#inventory-flow)
- [Screenshots / Mockups](#screenshots--mockups)
- [Team](#team)

---

## 📖 About the Project

**CoreInventory** is a full-stack Inventory Management System (IMS) built to replace outdated stock tracking methods. It provides real-time visibility into stock levels, seamless movement tracking across warehouses, and automated updates triggered by receipts, deliveries, and adjustments.

Whether you're managing incoming goods from vendors, dispatching orders to customers, or moving stock between internal locations — CoreInventory handles it all in one place, with every action logged in a tamper-proof stock ledger.

---

## 👥 Target Users

| Role | Responsibility |
|------|---------------|
| **Inventory Manager** | Manages incoming & outgoing stock, reviews KPIs, configures warehouses |
| **Warehouse Staff** | Performs transfers, picking, shelving, counting, and adjustments |

---

## ✨ Features

### 🔐 Authentication
- User Sign Up / Login
- Redirects to Inventory Dashboard on successful login

### 📊 Dashboard
Real-time snapshot of inventory operations with the following KPIs:
- Total Products in Stock
- Low Stock / Out-of-Stock Items
- Pending Receipts
- Pending Deliveries
- Scheduled Internal Transfers

**Dynamic Filters:**
- By document type: Receipts / Delivery / Internal / Adjustments
- By status: Draft → Waiting → Ready → Done → Cancelled
- By warehouse or location
- By product category

### 📦 Product Management
Create and manage products with:
- Name, SKU / Code
- Category & Unit of Measure
- Initial stock (optional)
- Stock availability per location
- Reordering rules & low-stock alerts

### 🚚 Receipts (Incoming Goods)
- Create receipt from vendor
- Add supplier & product lines
- Input quantities received
- Validate → stock increases automatically

### 📤 Delivery Orders (Outgoing Goods)
- Pick → Pack → Validate workflow
- Stock decreases automatically on validation
- Linked to sales orders

### 🔄 Internal Transfers
- Move stock between warehouses, racks, or locations
- Total stock unchanged; location updated
- Every movement logged in the stock ledger

### 🛠 Stock Adjustments
- Select product & location
- Enter physically counted quantity
- System auto-updates and logs the adjustment

### ➕ Additional
- 🔔 Low stock alerts
- 🏭 Multi-warehouse support
- 🔍 SKU search & smart filters
- 📋 Full stock ledger / move history

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML,CSS, JS, Talwind CSS|
| **Backend** | Python (Django) |
| **Database** | SQL (PostgreSQL) |
| **Version Control** | Git & GitHub |
| **Design / Mockup** | Excalidraw |

---

## 🗂 Project Structure

```
CoreInventory-Real-Time-Inventory-Management-Platform/
│
├── 📁 backend/
│   └── main.py                  # Backend entry point (Python)
│
├── 📁 database/
│   └── schema.sql               # SQL table definitions & schema
│
├── 📁 docs/
│   └── documentation.md         # Project documentation
│
├── 📁 frontend/
│   ├── index.html               # Main HTML entry point
│   └── style.css                # Global stylesheet
│
├── .gitignore
└── README.md
```

> 🚧 Project is in early development — more files and folders will be added as features are built out.

---

## 🗃 Database Tables

> Tables are being designed and will be documented here as they are created.

---

### `users`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `products`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `warehouses`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `receipts`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `delivery_orders`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `internal_transfers`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `stock_adjustments`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

### `stock_ledger`
| Column | Type | Description |
|--------|------|-------------|
| [Will be added soon] | — | — |

---

## 🌐 HTML Pages

> Pages will be listed here as they are built.

| Page | Route | Description |
|------|-------|-------------|
| Login / Sign Up | [Will be added soon] | User authentication entry point |
| Dashboard | [Will be added soon] | KPIs and inventory overview |
| Products List | [Will be added soon] | Browse, search, filter products |
| Product Detail | [Will be added soon] | View/edit a specific product |
| Receipts | [Will be added soon] | Manage incoming goods |
| Delivery Orders | [Will be added soon] | Manage outgoing shipments |
| Internal Transfers | [Will be added soon] | Move stock between locations |
| Stock Adjustments | [Will be added soon] | Fix physical vs recorded mismatches |
| Move History | [Will be added soon] | Full stock ledger / audit trail |
| Warehouse Settings | [Will be added soon] | Configure warehouses and locations |
| My Profile | [Will be added soon] | User profile management |

---

## 🔌 Backend APIs

> APIs will be documented here as they are developed.

### 🔐 Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | [Will be added soon] | Register new user |
| POST | [Will be added soon] | Login |
| POST | [Will be added soon] | Send OTP for password reset |
| POST | [Will be added soon] | Verify OTP & reset password |

---

### 📦 Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | Get all products |
| POST | [Will be added soon] | Create a new product |
| PUT | [Will be added soon] | Update a product |
| DELETE | [Will be added soon] | Delete a product |

---

### 🚚 Receipts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | List all receipts |
| POST | [Will be added soon] | Create a new receipt |
| PUT | [Will be added soon] | Validate a receipt (updates stock) |

---

### 📤 Delivery Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | List all delivery orders |
| POST | [Will be added soon] | Create a delivery order |
| PUT | [Will be added soon] | Validate delivery (decreases stock) |

---

### 🔄 Internal Transfers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | List all internal transfers |
| POST | [Will be added soon] | Create a transfer |
| PUT | [Will be added soon] | Validate transfer (updates location) |

---

### 🛠 Stock Adjustments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | List all adjustments |
| POST | [Will be added soon] | Create & apply an adjustment |

---

### 📋 Stock Ledger / Move History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | Get full movement history |
| GET | [Will be added soon] | Filter by product / warehouse / date |

---

### 🏭 Warehouses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | [Will be added soon] | List all warehouses |
| POST | [Will be added soon] | Create a warehouse |
| PUT | [Will be added soon] | Update warehouse details |

---

## 🔁 Inventory Flow

```
Step 1 — Receive Goods from Vendor
  └─ Receive 100 kg Steel → Stock: +100

Step 2 — Move to Production Rack
  └─ Internal Transfer: Main Store → Production Rack
     (Total stock unchanged; location updated)

Step 3 — Deliver Finished Goods
  └─ Deliver 20 steel → Stock: −20

Step 4 — Adjust Damaged Items
  └─ 3 kg steel damaged → Stock: −3

All movements are logged in the Stock Ledger ✅
```

---

## 🖼 Screenshots / Mockups

**Excalidraw Mockup:** [https://link.excalidraw.com/l/65VNwvy7c4X/3ENvQFu9o8R](https://link.excalidraw.com/l/65VNwvy7c4X/3ENvQFu9o8R)

> App screenshots will be added here once the UI is built.

| Screen | Preview |
|--------|---------|
| Dashboard | [Will be added soon] |
| Products | [Will be added soon] |
| Receipts | [Will be added soon] |
| Delivery Orders | [Will be added soon] |

---

## 👨‍💻 Team

| Name | Role |
|------|------|
| Het Vyas |	Backend Development, API Architecture, and Version Control |
| Kinjalba Vaghela |	Database Design and Management |
| Pooja Adhiya |	Frontend Development and Interface Design |
| Shashank |	Frontend Development and Interface Design |

---

## 📄 License

[Will be added soon]

---

<p align="center">Built with ❤️ for CoreInventory</p>
