import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def capturar_indicadores():
    url = "https://economia.uol.com.br/cotacoes/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # No UOL, os indicadores costumam ficar em tabelas ou componentes de 'indices'
        # Criamos um dicionário para armazenar os resultados
        resultados = {
            "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "indicadores": []
        }

        # Buscamos os blocos de índices (ajustado para a estrutura comum do portal)
        indices = soup.find_all("div", class_="info-index") # Classe comum no UOL

        for item in indices:
            nome = item.find("span", class_="name").text.strip()
            
            if nome in ["CDI", "SELIC", "IPCA"]:
                valor = item.find("span", class_="value").text.strip()
                # A data no UOL geralmente fica em um elemento pequeno ou title
                data_elemento = item.find("span", class_="date")
                data_valor = data_elemento.text.strip() if data_elemento else "Não informada"

                resultados["indicadores"].append({
                    "nome": nome,
                    "valor": valor,
                    "data_referencia": data_valor
                })

        # Salva o resultado em um arquivo JSON
        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Arquivo 'indicadores.json' gerado com sucesso!"

    except Exception as e:
        return f"Erro ao processar: {str(e)}"

print(capturar_indicadores())
