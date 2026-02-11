from flask import Flask, request, jsonify, render_template_string
import requests

# ================= CONFIG =================

API_KEY = "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"
MODEL = "openai/gpt-4o-mini"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000",
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
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3000
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print("Error:", response.text)
            return None

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("Request failed:", e)
        return None


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Gokul WebCraft AI — Website Builder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            margin: 0;
            font-family: system-ui;
            background: linear-gradient(135deg, #eef2ff, #f8fafc);
        }

        header {
            text-align: center;
            padding: 60px 20px;
        }

        header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
        }

        header p {
            color: #555;
        }

        .container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 14px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        }

        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        button {
            margin-top: 15px;
            padding: 14px 30px;
            border-radius: 999px;
            border: none;
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white;
            cursor: pointer;
            font-size: 16px;
        }

        iframe {
            width: 100%;
            height: 650px;
            margin-top: 30px;
            border: none;
            border-radius: 14px;
            background: white;
        }

        footer {
            text-align: center;
            padding: 40px;
            color: #777;
            font-size: 14px;
        }
    </style>
</head>
<body>

<header>
    <h1>WebCraft AI</h1>
    <p>Describe your idea. We build the website.</p>
</header>

<div class="container">
    <div class="card">
        <textarea id="prompt" placeholder="Example: A premium startup landing page with modern UI and animations"></textarea>
        <br>
        <button onclick="generate()">Generate Website</button>
    </div>

    <iframe id="preview"></iframe>
</div>

<footer>
    Built using AI • Gokul WebCraft AI
</footer>

<script>
async function generate() {
    const prompt = document.getElementById("prompt").value.trim();

    if (!prompt) {
        alert("Please describe your website first.");
        return;
    }

    document.getElementById("preview").srcdoc =
        "<h2 style='padding:40px;font-family:system-ui'>Generating...</h2>";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (data.html) {
            document.getElementById("preview").srcdoc = data.html;
        } else {
            document.getElementById("preview").srcdoc =
                "<h2 style='color:red;padding:40px'>AI failed</h2>";
        }

    } catch (e) {
        document.getElementById("preview").srcdoc =
            "<h2 style='color:red;padding:40px'>Request failed</h2>";
    }
}
</script>

</body>
</html>
""")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")

    html = ask_ai(prompt)

    if not html:
        return jsonify({"error": "AI failed"}), 500

    html = html.replace("```html", "").replace("```", "")
    return jsonify({"html": html})


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

