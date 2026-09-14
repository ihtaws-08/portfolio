
from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

# Used for admin login sessions
app.secret_key = "swathi_portfolio_secret"


# ==========================================
# MYSQL CONNECTION
# ==========================================

def get_db():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="swathi2008",
        database="portfolio_db"
    )


# ==========================================
# CREATE TABLES + INITIAL DATA
# ==========================================

def setup_database():

    db = get_db()
    cursor = db.cursor()

    # --------------------------------------
    # ADMIN TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)


    # --------------------------------------
    # PROFILE TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            title VARCHAR(200),
            bio TEXT,
            email VARCHAR(150),
            github VARCHAR(300)
        )
    """)


    # --------------------------------------
    # SKILLS TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)


    # --------------------------------------
    # PROJECTS TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            technologies VARCHAR(300),
            github VARCHAR(300)
        )
    """)


    # ======================================
    # DEFAULT ADMIN
    # ======================================

    cursor.execute("SELECT COUNT(*) FROM admin")

    admin_count = cursor.fetchone()[0]

    if admin_count == 0:

        cursor.execute("""
            INSERT INTO admin
            (username, password)
            VALUES (%s, %s)
        """, (
            "swathi",
            "1234"
        ))


    # ======================================
    # DEFAULT PROFILE
    # ======================================

    cursor.execute("SELECT COUNT(*) FROM profile")

    profile_count = cursor.fetchone()[0]

    if profile_count == 0:

        cursor.execute("""
            INSERT INTO profile
            (id, name, title, bio, email, github)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            1,
            "Swathi",
            "CS Student | Full-Stack Developer",
            "I am a first-year Computer Science Engineering student interested in programming, web development and building useful digital projects.",
            "pswathi232022@gmail.com",
            "https://github.com/ihtaws-08/project"
        ))


    # ======================================
    # DEFAULT SKILLS
    # ======================================

    cursor.execute("SELECT COUNT(*) FROM skills")

    skill_count = cursor.fetchone()[0]

    if skill_count == 0:

        skills = [
            ("Python",),
            ("SQL",),
            ("HTML/CSS",),
            ("MySQL",),
            ("Git/GitHub",)
        ]

        cursor.executemany("""
            INSERT INTO skills (name)
            VALUES (%s)
        """, skills)


    db.commit()

    cursor.close()
    db.close()


# ==========================================
# PUBLIC PORTFOLIO
# ==========================================

@app.route("/")
def home():

    db = get_db()

    cursor = db.cursor(dictionary=True)


    # Get profile

    cursor.execute("""
        SELECT *
        FROM profile
        WHERE id = 1
    """)

    profile = cursor.fetchone()


    # Get skills

    cursor.execute("""
        SELECT *
        FROM skills
        ORDER BY id
    """)

    skills = cursor.fetchall()


    # Get projects

    cursor.execute("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()


    cursor.close()
    db.close()


    return render_template(
        "portfolio.html",
        profile=profile,
        skills=skills,
        projects=projects
    )


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    # ------------------------------
    # LOGIN FORM SUBMITTED
    # ------------------------------

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]


        db = get_db()

        cursor = db.cursor(dictionary=True)


        cursor.execute("""
            SELECT *
            FROM admin
            WHERE username = %s
            AND password = %s
        """, (
            username,
            password
        ))


        user = cursor.fetchone()


        cursor.close()
        db.close()


        # ------------------------------
        # CORRECT LOGIN
        # ------------------------------

        if user:

            session["admin"] = True

            return redirect("/dashboard")


        # ------------------------------
        # WRONG LOGIN
        # ------------------------------

        return """
        <!DOCTYPE html>

        <html>

        <head>

            <title>Login Failed</title>

            <style>

                body {
                    font-family: Arial;
                    background: #f4efe6;
                    text-align: center;
                    padding-top: 100px;
                    color: #173c31;
                }

                a {
                    color: #173c31;
                }

            </style>

        </head>

        <body>

            <h2>Invalid username or password</h2>

            <p>
                <a href="/admin">
                    Try Again
                </a>
            </p>

        </body>

        </html>
        """


    # ------------------------------
    # LOGIN PAGE
    # ------------------------------

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>Admin Login | Swathi</title>


        <style>

            * {
                box-sizing: border-box;
            }


            body {

                margin: 0;

                min-height: 100vh;

                display: flex;

                justify-content: center;

                align-items: center;

                background: #f4efe6;

                font-family: Arial, sans-serif;

                color: #173c31;

            }


            .login-box {

                width: 90%;

                max-width: 420px;

                background: #fffdf8;

                padding: 45px;

                border: 1px solid rgba(23,60,49,.15);

                box-shadow:
                    0 15px 40px
                    rgba(23,60,49,.08);

            }


            .small {

                font-size: 10px;

                letter-spacing: 4px;

                color: #31594b;

                margin-bottom: 10px;

            }


            h1 {

                font-family: Georgia, serif;

                font-weight: normal;

                font-size: 42px;

                margin: 0 0 30px;

            }


            label {

                display: block;

                font-size: 12px;

                font-weight: bold;

                margin-bottom: 7px;

            }


            input {

                width: 100%;

                padding: 13px;

                margin-bottom: 20px;

                border: 1px solid #d5d0c6;

                background: #faf7f0;

                outline: none;

            }


            input:focus {

                border-color: #173c31;

            }


            button {

                width: 100%;

                padding: 14px;

                border: none;

                background: #173c31;

                color: white;

                cursor: pointer;

                font-weight: bold;

            }


            button:hover {

                background: #31594b;

            }


            .back {

                display: block;

                text-align: center;

                margin-top: 20px;

                font-size: 12px;

                color: #718078;

                text-decoration: none;

            }

        </style>

    </head>


    <body>


        <div class="login-box">

            <p class="small">
                PRIVATE AREA
            </p>


            <h1>
                Admin Login
            </h1>


            <form method="POST">


                <label>
                    USERNAME
                </label>


                <input
                    type="text"
                    name="username"
                    required
                >


                <label>
                    PASSWORD
                </label>


                <input
                    type="password"
                    name="password"
                    required
                >


                <button type="submit">
                    LOGIN
                </button>


            </form>


            <a
                href="/"
                class="back"
            >
                ← Back to Portfolio
            </a>


        </div>


    </body>

    </html>
    """


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    # Only logged-in admin can access

    if not session.get("admin"):

        return redirect("/admin")


    db = get_db()

    cursor = db.cursor(dictionary=True)


    # Profile

    cursor.execute("""
        SELECT *
        FROM profile
        WHERE id = 1
    """)

    profile = cursor.fetchone()


    # Skills

    cursor.execute("""
        SELECT *
        FROM skills
        ORDER BY id
    """)

    skills = cursor.fetchall()


    # Projects

    cursor.execute("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()


    cursor.close()
    db.close()


    return render_template(
        "dashboard.html",
        profile=profile,
        skills=skills,
        projects=projects
    )


# ==========================================
# UPDATE PROFILE
# ==========================================

@app.route("/update-profile", methods=["POST"])
def update_profile():

    if not session.get("admin"):

        return redirect("/admin")


    name = request.form["name"]

    title = request.form["title"]

    bio = request.form["bio"]

    email = request.form["email"]

    github = request.form["github"]


    db = get_db()

    cursor = db.cursor()


    cursor.execute("""
        UPDATE profile

        SET
            name = %s,
            title = %s,
            bio = %s,
            email = %s,
            github = %s

        WHERE id = 1
    """, (
        name,
        title,
        bio,
        email,
        github
    ))


    db.commit()


    cursor.close()
    db.close()


    return redirect("/dashboard")


# ==========================================
# ADD SKILL
# ==========================================

@app.route("/add-skill", methods=["POST"])
def add_skill():

    if not session.get("admin"):

        return redirect("/admin")


    skill = request.form["skill"].strip()


    if skill:

        db = get_db()

        cursor = db.cursor()


        cursor.execute("""
            INSERT INTO skills (name)
            VALUES (%s)
        """, (
            skill,
        ))


        db.commit()


        cursor.close()
        db.close()


    return redirect("/dashboard")


# ==========================================
# DELETE SKILL
# ==========================================

@app.route("/delete-skill/<int:id>")
def delete_skill(id):

    if not session.get("admin"):

        return redirect("/admin")


    db = get_db()

    cursor = db.cursor()


    cursor.execute("""
        DELETE FROM skills
        WHERE id = %s
    """, (
        id,
    ))


    db.commit()


    cursor.close()
    db.close()


    return redirect("/dashboard")


# ==========================================
# ADD PROJECT
# ==========================================

@app.route("/add-project", methods=["POST"])
def add_project():

    if not session.get("admin"):

        return redirect("/admin")


    title = request.form["title"].strip()

    description = request.form["description"].strip()

    technologies = request.form["technologies"].strip()

    github = request.form["github"].strip()


    if title:

        db = get_db()

        cursor = db.cursor()


        cursor.execute("""
            INSERT INTO projects
            (
                title,
                description,
                technologies,
                github
            )

            VALUES (%s, %s, %s, %s)
        """, (
            title,
            description,
            technologies,
            github
        ))


        db.commit()


        cursor.close()
        db.close()


    return redirect("/dashboard")


# ==========================================
# DELETE PROJECT
# ==========================================

@app.route("/delete-project/<int:id>")
def delete_project(id):

    if not session.get("admin"):

        return redirect("/admin")


    db = get_db()

    cursor = db.cursor()


    cursor.execute("""
        DELETE FROM projects
        WHERE id = %s
    """, (
        id,
    ))


    db.commit()


    cursor.close()
    db.close()


    return redirect("/dashboard")


# ==========================================
# CHANGE ADMIN PASSWORD
# ==========================================

@app.route("/change-password", methods=["POST"])
def change_password():

    # Only logged-in admin can change password

    if not session.get("admin"):

        return redirect("/admin")


    # Get passwords from form

    current_password = request.form["current_password"]

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]


    # Connect to database

    db = get_db()

    cursor = db.cursor(dictionary=True)


    # Get current admin

    cursor.execute("""
        SELECT *
        FROM admin
        WHERE username = %s
    """, (
        "swathi",
    ))


    admin_user = cursor.fetchone()


    # --------------------------------------
    # CHECK CURRENT PASSWORD
    # --------------------------------------

    if not admin_user or admin_user["password"] != current_password:

        cursor.close()
        db.close()

        return """
        <!DOCTYPE html>

        <html>

        <head>

            <title>Password Error</title>

            <style>

                body {

                    font-family: Arial, sans-serif;

                    background: #f4efe6;

                    color: #173c31;

                    text-align: center;

                    padding-top: 100px;

                }


                a {

                    color: #173c31;

                    text-decoration: none;

                    font-weight: bold;

                }

            </style>

        </head>


        <body>

            <h2>
                Current password is incorrect
            </h2>


            <p>

                <a href="/dashboard#password">

                    ← Try Again

                </a>

            </p>

        </body>

        </html>
        """


    # --------------------------------------
    # CHECK NEW PASSWORDS
    # --------------------------------------

    if new_password != confirm_password:

        cursor.close()
        db.close()

        return """
        <!DOCTYPE html>

        <html>

        <head>

            <title>Password Error</title>

            <style>

                body {

                    font-family: Arial, sans-serif;

                    background: #f4efe6;

                    color: #173c31;

                    text-align: center;

                    padding-top: 100px;

                }


                a {

                    color: #173c31;

                    text-decoration: none;

                    font-weight: bold;

                }

            </style>

        </head>


        <body>

            <h2>
                New passwords do not match
            </h2>


            <p>

                <a href="/dashboard#password">

                    ← Try Again

                </a>

            </p>

        </body>

        </html>
        """


    # --------------------------------------
    # CHECK EMPTY PASSWORD
    # --------------------------------------

    if not new_password.strip():

        cursor.close()
        db.close()

        return """
        <!DOCTYPE html>

        <html>

        <head>

            <title>Password Error</title>

            <style>

                body {

                    font-family: Arial, sans-serif;

                    background: #f4efe6;

                    color: #173c31;

                    text-align: center;

                    padding-top: 100px;

                }


                a {

                    color: #173c31;

                    text-decoration: none;

                    font-weight: bold;

                }

            </style>

        </head>


        <body>

            <h2>
                Password cannot be empty
            </h2>


            <p>

                <a href="/dashboard#password">

                    ← Try Again

                </a>

            </p>

        </body>

        </html>
        """


    # --------------------------------------
    # UPDATE PASSWORD
    # --------------------------------------

    cursor.execute("""
        UPDATE admin
        SET password = %s
        WHERE username = %s
    """, (
        new_password,
        "swathi"
    ))


    db.commit()


    cursor.close()
    db.close()


    # Return to dashboard

    return redirect("/dashboard#password")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    setup_database()

    app.run(debug=True)