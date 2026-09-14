from flask import Flask, request, redirect, session, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = "swathi_portfolio_secret"


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="swathi2008",
        database="portfolio_db"
    )


def setup_database():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            technologies VARCHAR(300),
            github VARCHAR(300)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM admin")

    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO admin (username, password)
            VALUES (%s, %s)
        """, ("swathi", "1234"))

    cursor.execute("SELECT COUNT(*) FROM profile")

    if cursor.fetchone()[0] == 0:
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

    cursor.execute("SELECT COUNT(*) FROM skills")

    if cursor.fetchone()[0] == 0:
        skills = [
            ("Python",),
            ("SQL",),
            ("HTML/CSS",),
            ("MySQL",),
            ("Git/GitHub",)
        ]

        cursor.executemany(
            "INSERT INTO skills (name) VALUES (%s)",
            skills
        )

    db.commit()

    cursor.close()
    db.close()


@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM profile WHERE id = 1")
    profile = cursor.fetchone()

    cursor.execute("SELECT * FROM skills ORDER BY id")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "portfolio.html",
        profile=profile,
        skills=skills,
        projects=projects
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM admin
            WHERE username = %s AND password = %s
        """, (username, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            session["admin"] = True
            return redirect("/dashboard")

        return """
        <h2>Invalid username or password</h2>
        <a href="/admin">Try Again</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Swathi | Admin Login</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f4efe6;
                font-family: Arial, sans-serif;
                color: #26352f;
            }

            .login-box {
                width: 380px;
                padding: 40px;
                background: #fffdf8;
                border: 1px solid #d8cebf;
                box-shadow: 12px 12px 0 #ebe3d5;
            }

            h1 {
                margin-top: 0;
                margin-bottom: 30px;
                color: #173c31;
                font-family: Georgia, serif;
            }

            label {
                display: block;
                margin-bottom: 7px;
                font-size: 14px;
            }

            input {
                width: 100%;
                padding: 13px;
                margin-bottom: 20px;
                border: 1px solid #cfc5b5;
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
            }

            button:hover {
                background: #31594b;
            }

            .back {
                display: block;
                margin-top: 20px;
                text-align: center;
                color: #31594b;
                text-decoration: none;
                font-size: 13px;
            }
        </style>
    </head>

    <body>

        <div class="login-box">

            <h1>Admin Login</h1>

            <form method="POST">

                <label>Username</label>

                <input
                    type="text"
                    name="username"
                    required
                >

                <label>Password</label>

                <input
                    type="password"
                    name="password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

            <a class="back" href="/">
                ← Back to Portfolio
            </a>

        </div>

    </body>
    </html>
    """


@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/admin")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM profile WHERE id = 1")
    profile = cursor.fetchone()

    cursor.execute("SELECT * FROM skills ORDER BY id")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        profile=profile,
        skills=skills,
        projects=projects
    )


@app.route("/update-profile", methods=["POST"])
def update_profile():

    if not session.get("admin"):
        return redirect("/admin")

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
        request.form["name"],
        request.form["title"],
        request.form["bio"],
        request.form["email"],
        request.form["github"]
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/dashboard")


@app.route("/add-skill", methods=["POST"])
def add_skill():

    if not session.get("admin"):
        return redirect("/admin")

    skill = request.form["skill"].strip()

    if skill:

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO skills (name) VALUES (%s)",
            (skill,)
        )

        db.commit()

        cursor.close()
        db.close()

    return redirect("/dashboard")


@app.route("/delete-skill/<int:id>")
def delete_skill(id):

    if not session.get("admin"):
        return redirect("/admin")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM skills WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/dashboard")


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
            (title, description, technologies, github)
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


@app.route("/delete-project/<int:id>")
def delete_project(id):

    if not session.get("admin"):
        return redirect("/admin")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)