# Advanced Complaint Management System (ACMS)

A complete, modern, and stylish web-based Complaint Management System built using **Python Flask, HTML5, CSS3, and SQLite**. This project is designed specifically for 1st-year CSE students for their Python Lab Mini Project and College Submission.

---

## 🚀 Quick Setup Instructions

### 1. Install Python
Ensure you have Python installed on your system. You can download it from [python.org](https://python.org).

### 2. Install Flask
Open your terminal or command prompt and run the following command:
```bash
pip install flask
```

### 3. Project Structure
Ensure your files are organized as follows:
```
AdvancedComplaintManagement/
├── app.py
├── complaints.db (auto-generated)
├── static/
│   ├── style.css
│   └── uploads/ (auto-generated)
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── register.html
│   ├── user_login.html
│   ├── admin_login.html
│   ├── user_dashboard.html
│   └── admin_dashboard.html
└── README.md
```

### 4. Run the Application
Navigate to the project folder and run:
```bash
python app.py
```
Open your browser and visit: `http://127.0.0.1:5000`

---

## 📝 Project Details

### 💡 Main Project Idea
The **Advanced Complaint Management System** is a secure platform that bridges the gap between users and administrators. It allows users to register, login, and submit grievances with optional image attachments. Admins can view all complaints, track their status (Pending, In Progress, Resolved), and manage them efficiently.

### 🛠️ Technology Stack
- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3 (Modern Glassmorphism Design)
- **Database:** SQLite3
- **Icons:** FontAwesome

---

## 📊 Algorithm
1. **Start** the application.
2. **Database Initialization:** Create `users`, `admin`, and `complaints` tables if they don't exist.
3. **User Module:**
   - User registers with name, ID, email, and password.
   - User logs in (Session created).
   - User submits a complaint with title, description, category, and optional image.
   - Data is stored in the SQLite database.
4. **Admin Module:**
   - Admin logs in with default credentials (`admin` / `admin123`).
   - Admin views all complaints in a modern table.
   - Admin updates the status of a complaint.
   - Admin deletes invalid or resolved complaints.
5. **Logout:** Clear session and redirect to home.
6. **Stop**.

---

## 📈 Flowchart (Text Format)
```text
[Start]
   |
[Home Page] --(Choose)--> [User Register] --> [Success] --|
   |                                                      |
   |---(Choose)--> [User Login] <-------------------------|
   |                 |
   |           [User Dashboard] --> [Submit Complaint] --> [Save to DB]
   |
   |---(Choose)--> [Admin Login]
                     |
               [Admin Dashboard] <--> [View/Update/Delete]
                     |
                  [Logout]
                     |
                   [End]
```

---

## 📂 File-by-File Explanation
- **`app.py`**: The heart of the project. Handles routing, database operations, session management, and file uploads.
- **`templates/layout.html`**: The base template containing the navigation bar and footer.
- **`templates/home.html`**: A beautiful landing page with a hero section.
- **`templates/register.html`**: User registration form with validation logic.
- **`templates/user_login.html`**: Secure login for registered users.
- **`templates/admin_login.html`**: Exclusive login for system administrators.
- **`templates/user_dashboard.html`**: Minimalist form for complaint submission.
- **`templates/admin_dashboard.html`**: Powerful management panel for admins.
- **`static/style.css`**: Contains all modern UI styles (Gradients, Glassmorphism, Responsive layout).

---

## 🗄️ Database Explanation (SQLite)
- **Table `users`**: Stores registration details.
- **Table `admin`**: Stores administrative credentials.
- **Table `complaints`**: Stores all submitted grievances including user info, timestamps, and file paths.

---

## ✅ Advantages
- **Modern UI:** Glassmorphism design looks professional.
- **Responsive:** Works on mobile, tablets, and desktops.
- **Lightweight:** Uses SQLite, so no heavy database installation is required.
- **Secure:** Uses Flask sessions to protect dashboards.

## ⚠️ Limitations
- Only allows specific image formats (PNG, JPG, JPEG).
- No password hashing (kept simple for beginners).
- Single admin support.

## 🔮 Future Enhancements
- Email notifications upon status update.
- User profile editing.
- Multi-admin support with roles.
- Advanced search and filter for admins.

---

## 🎓 Viva Questions & Answers
1. **Q: What is Flask?**
   - **A:** Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.
2. **Q: Why use SQLite?**
   - **A:** SQLite is serverless and zero-configuration. It's stored in a single file, making it perfect for small projects and lab submissions.
3. **Q: What are Flask Sessions?**
   - **A:** Sessions allow you to store information specific to a user from one request to the next.
4. **Q: How is the modern UI achieved?**
   - **A:** By using Vanilla CSS3 features like `backdrop-filter` for glassmorphism and `linear-gradient` for vibrant colors.

---

## 🛡️ Common Errors & Solutions
- **"ModuleNotFoundError: No module named 'flask'"**: Run `pip install flask`.
- **"IntegrityError: UNIQUE constraint failed"**: User ID already exists. Try a different ID.
- **Image not appearing**: Ensure the `static/uploads` folder exists and has permissions.

---

## 📝 University Answer Summary (10-15 Marks)
This project implements a **Complaint Management System** using the **MVC (Model-View-Controller)** pattern conceptually. The **Model** is SQLite, the **View** is HTML/CSS, and the **Controller** is Python Flask. It demonstrates CRUD (Create, Read, Update, Delete) operations, session management, and file handling—key concepts in web development and Python programming.
