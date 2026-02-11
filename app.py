from flask import Flask, request, jsonify, render_template_string
import requests
import os

# ================= CONFIG =================

API_KEY = os.environ.get("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")
MODEL = "openai/gpt-4o-mini"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://webcraft-ai.onrender.com",
    "X-Title": "WebCraft AI"
}

SYSTEM_PROMPT = """
You are a world-class frontend engineer and UI/UX designer.

RULES:
- Return ONLY valid HTML
- Single HTML file
- Include CSS and JS inside the HTML
- Modern, premium UI
- Smooth animations
- No explanations
"""

# ================= APP =================

app = Flask(__name__)

# ================= AI FUNCTION =================

def ask_ai(prompt):
    if not API_KEY:
        return None

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print("API ERROR:", response.text)
            return None

        data = response.json()

        if "choices" not in data:
            print("Invalid API response:", data)
            return None

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("Exception:", e)
        return None


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>WebCraft AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    margin: 0;
    font-family: system-ui;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    color: #111;
}

header {
    text-align: center;
    padding: 60px 20px;
}

header h1 {
    font-size: 3rem;
    margin: 0;
}

.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

textarea {
    width: 100%;
    height: 140px;
    padding: 15px;
    font-size: 16px;
    border-radius: 12px;
    border: 1px solid #ccc;
    resize: none;
}

button {
    margin-top: 15px;
    padding: 14px 30px;
    font-size: 16px;
    border: none;
    border-radius: 999px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    cursor: pointer;
    transition: 0.2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(79,70,229,0.35);
}

iframe {
    width: 100%;
    height: 650px;
    margin-top: 30px;
    border: none;
    border-radius: 16px;
    background: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.loading {
    padding: 40px;
    font-size: 18px;
}
</style>
</head>

<body>

<header>
    <h1>WebCraft AI</h1>
    <p>Describe your idea. We build it instantly.</p>
</header>

<div class="container">
    <div class="card">
        <textarea id="prompt" placeholder="Example: A premium startup website with smooth animations and modern UI..."></textarea>
        <button onclick="generate()">✨ Generate Website</button>
    </div>

    <iframe id="preview"></iframe>
</div>

<script>
async function generate() {
    const prompt = document.getElementById("prompt").value.trim();

    if (!prompt) {
        alert("Please describe your website.");
        return;
    }

    const preview = document.getElementById("preview");
    preview.srcdoc = "<div class='loading'>Generating your website...</div>";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (data.html) {
            preview.srcdoc = data.html;
        } else {
            preview.srcdoc = "<h2 style='color:red;padding:40px;'>AI failed. Try again.</h2>";
        }

    } catch (error) {
        preview.srcdoc = "<h2 style='color:red;padding:40px;'>Server error.</h2>";
    }
}
</script>

</body>
</html>
""")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    html = ask_ai(prompt)

    if not html:
        return jsonify({"error": "AI failed"}), 500

    html = html.replace("```html", "").replace("```", "")

    return jsonify({"html": html})


# ================= RUN =================

if __name__ == "__main__":
    app.run()
