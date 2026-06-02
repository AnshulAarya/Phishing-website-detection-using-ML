from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model & vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("phishing.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""

    if request.method == "POST":
        url = request.form.get("url", "")

        if url.strip() == "":
            prediction = "Please enter a URL"
            return render_template("index.html", prediction=prediction)

        # Clean URL
        clean_url = re.sub(r"https?://(www\.)?", "", url)

        # Predict
        result = model.predict(vectorizer.transform([clean_url]))[0]

        # Handle both numeric & string outputs
        if result in [1, "bad"]:
            prediction = "❌ Phishing Website Detected"
        elif result in [0, "good"]:
            prediction = "✅ Safe Website"
        else:
            prediction = "⚠️ Unknown Result"

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
