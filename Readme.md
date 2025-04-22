# Customer Ticket Resolver

A robust ticket management system designed to handle customer issues efficiently. This project features a FastAPI backend for processing ticket submissions, category classification, and resolution approvals, paired with a React frontend for a dynamic user interface. It supports ticket submission, category confirmation by agents, resolution approval, and similarity-based ticket suggestions.

## Features
- Submit new customer tickets with issue descriptions.
- Automatically classify tickets into categories (e.g., Billing, Network).
- Allow agents to confirm or edit predicted categories.
- Provide draft resolutions and enable agent approval of final responses.
- Display similar past tickets based on issue descriptions.
- Persistent storage using SQLite with session-based state management.
## Screenshots
# Home Page
![image](https://github.com/user-attachments/assets/981e1ef8-281b-431c-8989-cc082c0a0101)
# Page with Predicted Category and Draft Message
![image](https://github.com/user-attachments/assets/778d36ac-060b-4dd1-8f0c-9b4ae4675f00)
# Page with Similar tickets
![image](https://github.com/user-attachments/assets/d9962af4-11c2-4d0a-b6ac-9285eeebf4e0)
# Page After Agent Approves
![image](https://github.com/user-attachments/assets/d1c9afcf-83dd-45f1-a622-faea63aee2ff)


## Technologies Used
- **Backend:** FastAPI, SQLAlchemy, SQLite, Pydantic
- **Frontend:** React, Axios
- **Other Tools:** Python, Node.js, npm, Git
  

## Prerequisites
- **Python 3.10+** for the backend
- **Node.js 14+** and **npm** for the frontend
- Git for version control
- A code editor (e.g., VS Code) with SQLite extensions.



