import requests
import json
from datetime import datetime

def capturar_dados_direto():
    # Esta é a URL real que o UOL usa para preencher as tabelas de índices
    # Ela retorna um JSON puro, sem precisar "raspar" HTML
    url_dados = "https://api.cotacoes.uol.com.br/asset/list/?fields=name,price,high,low,open,variation,close,date&format=json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    resultados = {
        "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "indicadores": []
    }

    # Mapeamento de nomes que queremos
    alvos = {
        "CDI": "CDI",
        "SELIC": "Selic",
        "IPCA": "IPCA"
    }

    try:
        response = requests.get(url_dados, headers=headers, timeout=20)
        data = response.json()

        if "data" in data:
            for item in data["data"]:
                nome_uol = item.get("name", "")
                
                # Verificamos se o item está na nossa lista de desejados
                for chave, busca in alvos.items():
                    if busca.lower() in nome_uol.lower():
                        # Tratamento da data que vem do UOL (Ex: 20260102180000)
                        data_uol = str(item.get("date", ""))
                        if len(data_uol) >= 8:
                            data_formatada = f"{data_uol[6:8]}/{data_uol[4:6]}/{data_uol[0:4]}"
                        else:
                            data_formatada = "Recente"

                        # Evita duplicados (como IPCA-15) se quisermos apenas o IPCA cheio
                        if not any(i['nome'] == chave for i in resultados["indicadores"]):
                            resultados["indicadores"].append({
                                "nome": chave,
                                "valor": f"{item.get('price', 0)}%",
                                "data_referencia": data_formatada
                            })

        # Salva o arquivo
        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Sucesso total via API interna!"

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    print(capturar_dados_direto())
