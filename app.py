from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Plantilla HTML básica con formulario
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cielo de tu Cumpleaños</title>
</head>
<body style="font-family: Arial; text-align: center;">
    <h1>🔭 Ver el cielo en tu cumpleaños</h1>
    <form method="post">
        <label for="fecha">Introduce una fecha (YYYY-MM-DD):</label><br><br>
        <input type="date" name="fecha" required>
        <button type="submit">Ver cielo</button>
    </form>

    {% if imagen %}
        <h2>{{ titulo }}</h2>
        <img src="{{ imagen }}" width="500"><br><br>
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
    app.run(debug=True)
