🎓 Campus Placement Portal API [Placement Portal](https://placement-portal-4fe6.onrender.com)

📖 The Problem

Institutes require efficient systems to manage campus recruitment activities involving companies and students. Currently, many institutes rely on fragmented spreadsheets, email threads, or manual coordination. This creates massive administrative bottlenecks and makes it difficult to securely manage company approvals, coordinate placement drives, handle student registrations, and track application statuses.
💡 The Solution

This monolithic full-stack application digitizes and automates the entire recruitment lifecycle. It provides a secure, role-based platform where administrators can vet companies, employers can post job drives, and students can apply to opportunities seamlessly through a unified dashboard.

🛠️ Technical Architecture

    Frontend: Vue.js (compiled for monolith delivery)

    Backend: Python / Flask

    API Structure: Flask-RESTful (Class-Based Views)

    Database: PostgreSQL (Hosted on Neon)

    ORM & Migrations: Flask-SQLAlchemy & Flask-Migrate

    Background Tasks & Caching: Celery & Redis (Hosted on Upstash)

    Authentication: Flask-Security with PBKDF2-SHA512 hashing

    Deployment: Render Web Services
