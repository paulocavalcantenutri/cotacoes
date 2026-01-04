import requests
import json
from datetime import datetime

def capturar_indicadores():
    resultados = {
        "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "indicadores": []
    }

    # Códigos das séries no Banco Central: 11 (SELIC), 12 (CDI), 433 (IPCA mensal)
    series = {
        "SELIC": "11",
        "CDI": "12",
        "IPCA": "433"
    }

    try:
        for nome, codigo in series.items():
            # Pegamos o último valor disponível (last/1)
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                if dados:
                    item = dados[0]
                    resultados["indicadores"].append({
                        "nome": nome,
                        "valor": f"{item['valor']}%",
                        "data_referencia": item['data']
                    })

        # Salva o JSON final
        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Dados capturados com sucesso do Banco Central!"

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    print(capturar_indicadores())
