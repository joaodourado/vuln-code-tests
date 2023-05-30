import sqlite3
import yaml
from flask import Flask, request, render_template

app = Flask(__name__)

SECRET = "FM6DQ6Bcrr6MBJMiY6HL"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("data")
        file_path = request.form.get("file_path")
				
        result = None
        response = None
        status_url = request.form.get("url")

    try:
        response = request.get(status_url)
    except request.exceptions.RequestException as e:
        return f"Failed to make request: {e}", 500

    if not response.text.lower() == "true":
        return f"Bad status check", 500

    with open(file_path, "r") as file:
        content = file.read()
        result = eval(content, {"__builtins__": None})
        yaml_data = yaml.load(result)
        

    if result != SECRET:
        return "Invalid secret"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS data (data TEXT)")
    cursor.execute("INSERT INTO data (data) VALUES (?)", (str(result),))

    conn.commit()
    conn.close()

    return render_template("index.html", name=data)

if __name__ == "__main__":
    app.run()
