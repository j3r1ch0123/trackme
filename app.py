from flask import Flask, render_template, request, redirect
import secrets
import os
import requests

app = Flask(__name__)
filename = "location.txt"
api_tokens = {}

@app.route("/", methods=["GET"])
def home():
    try:
        with open(filename, "r") as thefile:
            content = thefile.read().replace("\n", "<br>")
    except Exception as e:
        print(f"Error reading file: {e}")
        return "Internal Server Error", 500

    return render_template("index.html", content=content)

@app.route("/add-message", methods=["POST"])
def add_message():
    try:
        message = request.get_data(as_text=True) + "\n"
        with open(filename, "w") as thefile:
            thefile.write(message)
    except Exception as e:
        print(f"Error writing file: {e}")
        return "Internal Server Error", 500

    return redirect("/")

if __name__ == "__main__":
    app.run(port=80)

