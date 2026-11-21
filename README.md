# Python MVC Clean Architecture Template

A lightweight, zero-dependency (pure Python) MVC server architecture with automatic route registration and hot-reloading.

---

## 🏗️ Architecture Overview

When you want to add a new API endpoint, you only need to touch **3 files**:

```
Client Request
      ⬇
1. Route (api/*_routes.py)       -> Maps URL to a Controller function (Auto-scanned by core/router.py)
      ⬇
2. Controller (controllers/*.py) -> Receives payload, validates, calls Service, formats response
      ⬇
3. Service (services/*.py)       -> Contains pure business logic (MT5, calculations, database, etc.)
```

---

## 📁 Directory Structure

```text
Quant_Algo_Backend/
├── api/
│   ├── __init__.py
│   └── demo_routes.py         <-- 1. Route definitions (mapped to controllers)
├── controllers/
│   ├── __init__.py
│   └── demo_controller.py     <-- 2. Request/Response controller
├── services/
│   ├── __init__.py
│   └── demo_service.py        <-- 3. Business logic / algorithms
├── core/
│   ├── __init__.py
│   └── router.py              <-- Auto route discovery mechanism
├── app.py                     <-- HTTP Server & routing engine (Pure Python)
├── watcher.py                 <-- Auto-reloader for development
├── requirements.txt           <-- (Optional) watchdog for auto-reload
└── README.md
```

---

## 🚀 How to Run

### Standard Mode:
```bash
python app.py
```

### Development Mode (Auto-reload on file change):
```bash
pip install -r requirements.txt
python watcher.py
```

---

## 🧪 Demo Endpoints

* **GET `http://127.0.0.1:5000/`** -> Server status & available route list
* **GET `http://127.0.0.1:5000/api/demo`** -> Demo GET endpoint
* **POST `http://127.0.0.1:5000/api/demo/order`** -> Demo POST endpoint
  ```json
  {
    "symbol": "EURUSD",
    "action": "BUY",
    "volume": 0.05
  }
  ```
