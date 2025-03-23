from flask import Flask, request, send_file
from generate_gif import add_name_to_gif

app = Flask(__name__)

@app.route('/generate')
def generate():
    name = request.args.get('name', '')
    gif_bytes = add_name_to_gif("EIF.gif", name)
    return send_file(
        gif_bytes,
        mimetype='image/gif',
        as_attachment=True,
        download_name=f'{name}_personalized.gif'
    )

if __name__ == '__main__':
    app.run(debug=True)
