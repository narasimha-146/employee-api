# Employee Management API (FastAPI + MongoDB)

A simple Employee Management API built with **FastAPI** and **MongoDB Atlas**.  
Supports full CRUD operations, querying, aggregation, and secure JWT-protected routes.  

---

## 🚀 Features
- **CRUD**:
  - Create Employee
  - Get Employee by ID
  - Update Employee (partial updates supported)
  - Delete Employee
- **Queries**:
  - List employees by department
  - Search employees by skill
  - Calculate average salary per department
- **Advanced Features**:
  - Pagination for employee listing
  - MongoDB JSON Schema validation
  - JWT authentication for protected routes
- **Interactive Docs**: Swagger UI (`/docs`) and ReDoc (`/redoc`)

---

## 🛠️ Tech Stack
- **FastAPI** – web framework
- **Motor (async MongoDB driver)** – database connection
- **MongoDB Atlas** – cloud database
- **Uvicorn** – ASGI server
- **python-dotenv** – load environment variables
- **PyJWT** – JWT authentication

---

## 📂 Project Structure


employee_api/
│── app/
│ ├── init.py
│ ├── main.py # FastAPI app entry
│ ├── database.py # MongoDB connection
│ ├── models.py # Pydantic models
│ ├── crud.py # CRUD + queries/aggregations
│ └── routes/
│ └── employees.py # Employee API routes
│
├── requirements.txt
├── .env # MongoDB URI + configs (not committed!)
├── app/test_mongo.py # Optional: safe local MongoDB test
└── README.md


---

## ⚙️ Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/employee-api.git
cd employee-api
```
2. Create Virtual Environment
python -m venv venv
# Activate it:
# Windows (PowerShell)
.\venv\Scripts\Activate
# macOS/Linux
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt


5. Run the Server

Local development:

uvicorn app.main:app --reload --port 8000


Render deployment (automatic $PORT):

uvicorn app.main:app --host 0.0.0.0 --port $PORT

📖 API Endpoints
Employees
Method	Endpoint	Description
POST	/employees/	Create a new employee
GET	/employees/{employee_id}	Get employee by ID
PUT	/employees/{employee_id}	Update employee (partial allowed)
DELETE	/employees/{employee_id}	Delete employee
Queries
Method	Endpoint	Description
GET	/employees/?department=Engineering	List employees by department, newest first
GET	/employees/search/?skill=Python	List employees by skill
GET	/employees/average-salary	Average salary per department
🧪 Example (cURL)

Create employee

curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "E001",
    "name": "Alice",
    "department": "Engineering",
    "salary": 80000,
    "joining_date": "2023-02-10",
    "skills": ["Python", "FastAPI"]
  }'


Get by ID

curl http://127.0.0.1:8000/employees/E001


Average salary per department

curl http://127.0.0.1:8000/employees/average-salary

📚 API Docs

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🚀 API Demo (Swagger UI)

Here’s a quick demo of the Employee API in action:

🌍 Live Demo [assests/swagger-demo.gif]

The API is deployed on Render:
👉 https://employee-api-wl86.onrender.com/docs#/



## 📂 Project Structure
