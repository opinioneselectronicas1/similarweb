from flask import Flask, request, jsonify
import os
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_similarweb(domain):
    """Función para extraer datos de SimilarWeb usando Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.similarweb.com/website/{domain}/", timeout=30000)

        try:
            traffic = page.locator("span.engagementInfo-valueNumber").text_content()
        except:
            traffic = "No disponible"

        browser.close()
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
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
