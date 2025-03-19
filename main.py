from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_similarweb(domain):
    """Función para extraer datos de SimilarWeb usando requests en vez de Playwright"""
    url = f"https://www.similarweb.com/website/{domain}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"No se pudo acceder a SimilarWeb (status {response.status_code})"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        traffic = soup.select_one("span.engagementInfo-valueNumber").text.strip()
    except AttributeError:
        traffic = "No disponible"

    return {"domain": domain, "traffic": traffic}

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a la API de tráfico SimilarWeb 🚀"})

@app.route('/get_traffic', methods=['GET'])
def get_traffic():
    """Ruta para obtener el tráfico de un dominio"""
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Debes proporcionar un dominio"}), 400

    data = scrape_similarweb(domain)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
