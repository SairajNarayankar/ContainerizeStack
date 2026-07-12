# 🐳 BE-04: Containerize Your Stack

> **FlyRank AI Internship — Backend AI Engineering Track — Week 2**

A production-ready containerized stack using:

- **FastAPI** (application service)
- **PostgreSQL 16** (database service)
- **Docker Compose** (orchestration)

This project replaces the in-memory repository with a PostgreSQL-backed implementation and runs the full stack with a **single command**. Persistent data is stored in a named Docker volume, so it survives container restarts and recreation.

---

## 🎯 Assignment Goal

Run PostgreSQL in Docker, connect the A2 service to it, and start both the app and database together using one command.

---

## ⚡ Quickstart

```bash
# 1) Clone the repository
git clone https://github.com/YOUR_USERNAME/ContainerizeStack.git
cd ContainerizeStack

# 2) Copy environment template
cp .env.example .env

# 3) Start the complete stack
docker compose up --build
```

### Service Endpoints

- 🌐 API Root: `http://localhost:8000`
- 📖 Swagger UI: `http://localhost:8000/docs`
- 🗄️ PostgreSQL: `localhost:5432`

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────┐
│               docker compose up                     │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌───────────────────┐          ┌───────────────────┐
│    flyrank_app    │          │    flyrank_db     │
│     (FastAPI)     │◄────────►│   (Postgres 16)   │
│    port 8000      │  SQLAlch │    port 5432      │
└───────────────────┘          └─────────┬─────────┘
                                         │
                                         ▼
                              ┌────────────────────┐
                              │   postgres_data    │
                              │   (named volume)   │
                              │   ← PERSISTENCE    │
                              └────────────────────┘
```

---

## 📁 Project Structure

```text
ContainerizeStack/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── models.py               # SQLAlchemy models
│   ├── database.py             # DB engine + session
│   ├── routes.py               # API routes (UNCHANGED from A2)
│   └── repositories/
│       ├── memory_repo.py      # Old A2 in-memory store
│       └── postgres_repo.py    # NEW Postgres implementation
├── sql/
│   └── init.sql                # Table creation on first boot
├── .env                        # 🔒 gitignored (real secrets)
├── .env.example                # ✅ committed (template)
├── .gitignore
├── Dockerfile                  # App image
├── docker-compose.yml          # Full stack orchestration
├── requirements.txt
└── README.md
```

---

## 🏆 Persistence Proof (Core Requirement)

The assignment requires that data remains available after containers are removed and recreated. The following test demonstrates persistence using the named Docker volume.

```bash
# 1) Create an item
curl.exe -X POST "http://localhost:8000/items?name=PersistenceProof"
{"created_at":"2026-07-12T21:25:40.406753","name":"PersistenceProof","id":1,"description":null}

# 2) Verify the item is stored
curl http://localhost:8000/items
StatusCode        : 200
Content           : [{"created_at":"2026-07-12T21:25:40.406753",
                     "name":"PersistenceProof","id":1,"description":null}]

# 3) Destroy all containers
docker compose down
[+] Running 3/3
 ✔ Container flyrank_app                  Removed    9.7s
 ✔ Container flyrank_db                   Removed    8.5s
 ✔ Network containerizestack_default      Removed    2.8s

# 4) Start fresh containers (same volume)
docker compose up -d
[+] Running 3/3
 ✔ Network containerizestack_default      Created    0.5s
 ✔ Container flyrank_db                   Healthy   14.8s
 ✔ Container flyrank_app                  Started   13.0s

# 5) Data is still present ✅
curl http://localhost:8000/items
StatusCode        : 200
Content           : [{"name":"PersistenceProof","id":1,
                     "created_at":"2026-07-12T21:25:40.406753","description":null}]
```

![Persistence proof screenshot](persistence-proof-1.png)
