from flask import Flask, request, jsonify, render_template_string
import requests
import os
import random

# ================= CONFIG =================

API_KEY = "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"
MODEL = "openai/gpt-4o-mini"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://gokulwebcraft.onrender.com",
    "X-Title": "WebCraft AI"
}

SYSTEM_PROMPT = """
You are a world-class frontend engineer and UI/UX designer.

RULES:
- Return ONLY valid HTML
- Single HTML file
- Include CSS and JS inside the HTML
- Ultra premium design (Apple / Stripe / Linear quality)
- Smooth animations
- Responsive
- No explanations
"""

app = Flask(__name__)

# ================= AI WEBSITE FUNCTION =================

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
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("Exception:", e)
        return None


# ================= AI PROMPT GENERATOR =================

def generate_ai_prompt():

    themes = ["Dark Futuristic", "Light Minimal", "Neon Cyberpunk", "Luxury Gold"]

    selected_theme = random.choice(themes)

    system_prompt = f"""
Generate ONE premium website idea.
Theme: {selected_theme}
Include:
- Hero section
- Features
- Animations
- Visual style description
Return ONLY the prompt text.
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system_prompt}],
        "max_tokens": 300
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        return None, None

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"], selected_theme
    except:
        return None, None


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>WebCraft AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

<style>
*{margin:0;padding:0;box-sizing:border-box}

body{
font-family:'Inter',sans-serif;
background:#0f172a;
color:white;
overflow-x:hidden;
}

header{
text-align:center;
padding:100px 20px;
}

header h1{
font-size:4rem;
background:linear-gradient(90deg,#6366f1,#8b5cf6);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

header p{
margin-top:20px;
opacity:0.7;
font-size:1.2rem;
}

/* 🔥 Wider container */
.container{
max-width:1500px;
margin:auto;
padding:20px;
}

.card{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(20px);
padding:30px;
border-radius:20px;
box-shadow:0 20px 60px rgba(0,0,0,0.6);
margin-bottom:40px;
}

textarea{
width:100%;
height:160px;
padding:15px;
border-radius:15px;
border:none;
font-size:16px;
background:#1e293b;
color:white;
}

button{
margin-top:20px;
padding:14px 35px;
border:none;
border-radius:999px;
font-size:16px;
font-weight:600;
cursor:pointer;
background:linear-gradient(90deg,#6366f1,#8b5cf6);
color:white;
transition:0.3s;
}

button:hover{
transform:scale(1.05);
box-shadow:0 10px 30px rgba(99,102,241,0.6);
}

/* 🔥 MUCH BIGGER WEBSITE DISPLAY */
iframe{
width:100%;
height:95vh;               /* Almost full screen height */
border:none;
border-radius:30px;
background:white;
margin-top:50px;
box-shadow:0 50px 150px rgba(0,0,0,0.9);
}

#generatedPrompt{
margin-top:20px;
min-height:100px;
opacity:0.8;
font-size:15px;
line-height:1.6;
}

.themeLabel{
margin-top:10px;
font-weight:600;
color:#8b5cf6;
font-size:16px;
}

footer{
text-align:center;
padding:60px;
opacity:0.5;
}
</style>
</head>

<body>

<header>
<h1>WebCraft AI</h1>
<p>AI-powered premium website builder</p>
</header>

<div class="container">

<div class="card">
<h2>AI Prompt Generator</h2>
<button onclick="generatePrompt()">Generate AI Idea</button>
<div class="themeLabel" id="themeLabel"></div>
<div id="generatedPrompt"></div>
</div>

<div class="card">
<textarea id="prompt" placeholder="Or write your own idea here..."></textarea>
<button onclick="generate()">Generate Website</button>
</div>

<iframe id="preview"></iframe>

</div>

<footer>
© 2026 WebCraft AI • Built by Gokul
</footer>

<script>

function typeWriter(text, element){
element.innerHTML="";
let i=0;
function typing(){
if(i<text.length){
element.innerHTML+=text.charAt(i);
i++;
setTimeout(typing,15);
}
}
typing();
}

async function generatePrompt(){

document.getElementById("preview").srcdoc = `
<!DOCTYPE html>
<html>
<head>
<style>
body{
margin:0;
height:100vh;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
background:linear-gradient(135deg,#0f172a,#1e293b);
font-family:Inter,sans-serif;
color:white;
overflow:hidden;
}

.loader{
width:70px;
height:70px;
border:6px solid rgba(255,255,255,0.2);
border-top:6px solid #8b5cf6;
border-radius:50%;
animation:spin 1s linear infinite;
margin-bottom:30px;
}

@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}

.text{
font-size:22px;
letter-spacing:1px;
animation:pulse 1.5s ease-in-out infinite;
}

@keyframes pulse{
0%{opacity:0.4;}
50%{opacity:1;}
100%{opacity:0.4;}
}
</style>
</head>
<body>
<div class="loader"></div>
<div class="text">AI is crafting your premium website...</div>
</body>
</html>
`;

document.getElementById("themeLabel").innerHTML="";

const response=await fetch("/generate-prompt",{method:"POST"});
const data=await response.json();

if(data.prompt){
document.getElementById("themeLabel").innerHTML="Theme: "+data.theme;
typeWriter(data.prompt,document.getElementById("generatedPrompt"));
document.getElementById("prompt").value=data.prompt;
}else{
document.getElementById("generatedPrompt").innerHTML="Failed.";
}
}

async function generate(){

const prompt=document.getElementById("prompt").value.trim();
if(!prompt){alert("Enter idea first");return;}

document.getElementById("preview").srcdoc=
"<h2 style='padding:60px;font-family:sans-serif'>Generating...</h2>";

const response=await fetch("/generate",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({prompt})
});

const data=await response.json();

if(data.html){
document.getElementById("preview").srcdoc=data.html;
}else{
document.getElementById("preview").srcdoc=
"<h2 style='color:red;padding:60px'>AI Failed</h2>";
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

    html = ask_ai(prompt)

    if not html:
        return jsonify({"error": "AI failed"}), 500

    html = html.replace("```html", "").replace("```", "")
    return jsonify({"html": html})


@app.route("/generate-prompt", methods=["POST"])
def prompt_generator():

    prompt, theme = generate_ai_prompt()

    if not prompt:
        return jsonify({"error": "Failed"}), 500

    return jsonify({"prompt": prompt, "theme": theme})


if __name__ == "__main__":
    app.run()
