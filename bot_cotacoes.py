import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def capturar_dados_uol():
    url = "https://economia.uol.com.br/cotacoes/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Estrutura base do nosso arquivo
    resultados = {
        "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "indicadores": []
    }

    # Lista do que queremos buscar exatamente
    alvos = ["CDI", "SELIC", "IPCA"]

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscamos todas as linhas de tabela (tr) da página
        linhas = soup.find_all('tr')

        for linha in linhas:
            colunas = linha.find_all('td')
            
            # Verificamos se a linha tem pelo menos 3 colunas (como no seu código fonte)
            if len(colunas) >= 3:
                # Pegamos o texto da primeira coluna e limpamos espaços
                texto_item = colunas[0].get_text(strip=True).upper()
                
                # Verificamos se o texto é um dos nossos alvos
                if texto_item in alvos:
                    valor = colunas[1].get_text(strip=True)
                    data_ref = colunas[2].get_text(strip=True)
                    
                    # Adicionamos ao nosso dicionário, evitando duplicados
                    if not any(i['nome'] == texto_item for i in resultados["indicadores"]):
                        resultados["indicadores"].append({
                            "nome": texto_item,
                            "valor": valor,
                            "data_referencia": data_ref
                        })

        # Ordenar os indicadores para ficarem sempre na mesma ordem (opcional)
        resultados["indicadores"].sort(key=lambda x: x['nome'])

        # Salva o arquivo JSON final
        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Sucesso! Dados extraídos conforme o código fonte."

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    print(capturar_dados_uol())
