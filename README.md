# 🐳 BE-04: Containerize Your Stack

> **FlyRank AI Internship — Backend AI Engineering Track — Week 2**

A production-ready containerized stack: **FastAPI** app + **PostgreSQL 16** database, orchestrated with **Docker Compose**. Data survives full container restarts via a named Docker volume. Swapped the in-memory store from A2 → Postgres repository **without touching a single route**, proving clean layered architecture.

---

## 🎯 Assignment Goal

Run Postgres in Docker, connect the A2 service to it (swapping the in-memory store for a real repository), and start app + database together with **one command**.

---

## ⚡ Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ContainerizeStack.git
cd ContainerizeStack

# 2. Copy environment template
cp .env.example .env

# 3. Start everything with ONE command
docker compose up --build


App available at:

🌐 API root: http://localhost:8000
📖 Swagger UI: http://localhost:8000/docs
🗄️ Postgres: localhost:5432


🏗️ Architecture

┌─────────────────────────────────────────────────────┐
│              docker compose up                       │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌───────────────────┐          ┌───────────────────┐
│   flyrank_app     │          │    flyrank_db     │
│   (FastAPI)       │◄────────►│   (Postgres 16)   │
│   port 8000       │  SQLAlch │   port 5432       │
└───────────────────┘          └─────────┬─────────┘
                                         │
                                         ▼
                              ┌────────────────────┐
                              │  postgres_data     │
                              │  (named volume)    │
                              │  ← PERSISTENCE     │
                              └────────────────────┘


📁 Project Structure

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

🏆 Persistence Proof (Assignment Core Requirement)
The data must survive container destruction. Proven with the following live test:

# 1️⃣  Create an item
> curl.exe -X POST "http://localhost:8000/items?name=PersistenceProof"
{"created_at":"2026-07-12T21:25:40.406753","name":"PersistenceProof","id":1,"description":null}

# 2️⃣  Verify item is stored
> curl http://localhost:8000/items
StatusCode        : 200
Content           : [{"created_at":"2026-07-12T21:25:40.406753",
                     "name":"PersistenceProof","id":1,"description":null}]

# 3️⃣  DESTROY all containers
> docker compose down
[+] Running 3/3
 ✔ Container flyrank_app                  Removed    9.7s
 ✔ Container flyrank_db                   Removed    8.5s
 ✔ Network containerizestack_default      Removed    2.8s

# 4️⃣  START fresh containers (same volume)
> docker compose up -d
[+] Running 3/3
 ✔ Network containerizestack_default      Created    0.5s
 ✔ Container flyrank_db                   Healthy   14.8s
 ✔ Container flyrank_app                  Started   13.0s

# 5️⃣  Data STILL there ✅
> curl http://localhost:8000/items
StatusCode        : 200
Content           : [{"name":"PersistenceProof","id":1,
                     "created_at":"2026-07-12T21:25:40.406753","description":null}]

![alt text](persistence-proof-1.png)
