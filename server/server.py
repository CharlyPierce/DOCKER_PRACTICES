from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    pod_name = os.environ.get("HOSTNAME", "unknown")
    return f"Hola desde HTTPS! Estoy en el pod: {pod_name}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
