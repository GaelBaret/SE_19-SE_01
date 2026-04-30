# 🚀 Full-Stack Blog Project

A professional, decoupled full-stack application featuring a **Node.js API** and a **Python (Flask) Frontend**, fully deployed on Render with a cloud-hosted MongoDB database.

## 🌟 Project Overview
This project is built using a modern microservices architecture. Instead of one giant application, it is split into two specialized services:
1. **The Backend (Node.js):** Handles data and communication with MongoDB Atlas.
2. **The Frontend (Python/Flask):** Fetches data from the API and displays it to users.

## 🛠️ Tech Stack
* **Backend:** Node.js, Express, Mongoose, MongoDB Atlas
* **Frontend:** Python, Flask, Gunicorn, Requests library
* **Hosting:** Render (Cloud Services)

## 🌐 System Architecture
1. **Client** visits the Python Frontend URL.
2. **Frontend** calls the **Node.js API** using the `API_URL` environment variable.
3. **Node.js API** talks to **MongoDB Atlas**.
4. Data flows back and is rendered on the page.

## ⚙️ Deployment Notes
* **Network Security:** Whitelisted `0.0.0.0/0` in MongoDB Atlas for Render connectivity.
* **Environment Variables:** Used `API_URL` on Render to connect the services securely.
* **SSL:** Configured Python `requests` to handle HTTPS communication.

---
*Created by Gael Baret - 2026*
