from flask import Flask, request, send_file, render_template_string
from generate_gif import add_name_to_gif
import os

app = Flask(__name__)

# Home: just redirect to greeting form if needed or show HTML form
@app.route('/')
def home():
    return "Go to /greeting?name=YourName to see preview"

# HTML preview page
@app.route('/greeting')
def greeting():
    name = request.args.get('name', 'ضيف')
    # Dynamically replace {{name}} in the HTML template
    with open('greeting.html', 'r', encoding='utf-8') as file:
        html_content = file.read().replace("{{name}}", name)
    return render_template_string(html_content)

# API to generate GIF and serve it
@app.route('/generate')
def generate():
    name = request.args.get('name', 'ضيف')
    output_gif = os.path.join("static", "generated", f"EIF-personalized.gif")
    add_name_to_gif("EIF.gif", output_gif, name)
    return send_file(output_gif, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("static/generated", exist_ok=True)
    app.run(debug=True)
