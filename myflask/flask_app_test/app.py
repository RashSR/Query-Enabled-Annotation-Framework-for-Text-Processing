from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", name="Flask User")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    return f"Hello, {username}!"

@app.route("/api/data")
def api_data():
    return jsonify({"message": "This is a JSON response", "status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
