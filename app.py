from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cielo de tu Cumpleaños</title>
    <style>
        body {
            background-color: #0e1a2b;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding: 50px;
        }

        h1 {
            color: #00c2ff;
            font-size: 2.5em;
        }

        label {
            font-size: 1.2em;
            margin-bottom: 10px;
            display: block;
        }

        input[type="date"] {
            padding: 10px;
            font-size: 1em;
            border-radius: 10px;
            border: none;
            outline: none;
            width: 200px;
        }

        button {
            margin-top: 20px;
            padding: 12px 25px;
            font-size: 1em;
            background-color: #00c2ff;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        button:hover {
            background-color: #0099cc;
        }

        img {
            max-width: 90%;
            border-radius: 15px;
            margin-top: 30px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }

        p {
            font-size: 1.1em;
            margin: 20px auto;
            max-width: 800px;
            color: #d3d3d3;
        }
    </style>
</head>
<body>
    <h1>🔭 Ver el cielo en tu cumpleaños</h1>
    <form method="post">
        <label for="fecha">Introduce una fecha (YYYY-MM-DD):</label>
        <input type="date" name="fecha" required>
        <br>
        <button type="submit">Ver cielo</button>
    </form>

    {% if imagen %}
        <h2>{{ titulo }}</h2>
        <img src="{{ imagen }}" alt="Imagen del cielo en tu cumpleaños">
        <p>{{ descripcion }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def cielo():
    imagen = titulo = descripcion = None

    if request.method == "POST":
        fecha = request.form["fecha"]
        api_url = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={fecha}"
        respuesta = requests.get(api_url).json()

        if "url" in respuesta:
            imagen = respuesta["url"]
            titulo = respuesta.get("title", "Sin título")
            descripcion = respuesta.get("explanation", "Sin descripción disponible")

    return render_template_string(HTML, imagen=imagen, titulo=titulo, descripcion=descripcion)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
