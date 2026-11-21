# Quant Algo Backend Server (Python MVC)

A lightweight, high-performance MVC backend server built in pure Python (Zero external web framework dependencies).

---

## 🔐 Default Superadmin Credentials

Upon first launch, the database (`quant_algo.db`) is automatically initialized and seeded with:

* **Username:** `admin`
* **Email:** `admin@quantalgo.com`
* **Password:** `admin123`
* **Role:** `superadmin`

---

## 📡 API Endpoints

### 1. Authentication Endpoints

#### 🔑 Login
* **POST `/api/auth/login`**
* **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
* **Success Response (200):**
  ```json
  {
    "success": true,
    "message": "Login successful",
    "data": {
      "token": "tok_9b2d35e1f0...",
      "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@quantalgo.com",
        "role": "superadmin",
        "created_at": "2026-11-21 08:40:00"
      }
    }
  }
  ```

#### 👤 Current Admin Profile
* **POST `/api/auth/me`**
* **Request Body:**
  ```json
  {
    "token": "tok_9b2d35e1f0..."
  }
  ```

#### 🚪 Logout
* **POST `/api/auth/logout`**
* **Request Body:**
  ```json
  {
    "token": "tok_9b2d35e1f0..."
  }
  ```

---

### 2. Admin CRUD Endpoints

#### 📋 List All Admins
* **GET `/api/admin/list`**
* Returns array of all admin accounts (passwords excluded).

#### 🔍 Get Single Admin
* **POST `/api/admin/get`**
* **Request Body:**
  ```json
  {
    "id": 1
  }
  ```

#### ➕ Create New Admin
* **POST `/api/admin/create`**
* **Request Body:**
  ```json
  {
    "username": "trader_john",
    "email": "john@quantalgo.com",
    "password": "SecurePassword123!",
    "role": "admin"
  }
  ```

#### ✏️ Update Admin
* **POST `/api/admin/update`**
* **Request Body:**
  ```json
  {
    "id": 2,
    "email": "john.updated@quantalgo.com",
    "role": "manager",
    "password": "NewPassword456!"
  }
  ```

#### ❌ Delete Admin
* **POST `/api/admin/delete`**
* **Request Body:**
  ```json
  {
    "id": 2
  }
  ```
*(Protection: You cannot delete the only remaining superadmin)*.

---

## 🏗️ Architecture Pattern (3-File Rule)

```text
Request ➔ api/*_routes.py ➔ controllers/*_controller.py ➔ services/*_service.py ➔ core/database.py
```

* **`core/router.py`**: Auto-scans all `api/*_routes.py` files on startup.
* **`core/database.py`**: SQLite connection & schema manager.
* **`services/`**: Business logic & DB queries.
* **`controllers/`**: Request validation, status codes, and JSON response formatting.
* **`api/`**: Route definition mapping URLs to controllers.

---

## 🚀 Running the Server

```bash
# Direct run:
python app.py

# With auto-reload on file change:
pip install -r requirements.txt
python watcher.py
```
