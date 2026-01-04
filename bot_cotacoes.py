import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def capturar_dados():
    url = "https://economia.uol.com.br/cotacoes/"
    
    # Headers mais completos para parecer um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,ir/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    resultados = {
        "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "indicadores": []
    }

    try:
        # Usamos uma sessão para lidar com cookies se necessário
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        # Se o UOL bloquear, tentamos pegar o conteúdo bruto
        soup = BeautifulSoup(response.content, 'html.parser')
        html_puro = str(soup)

        # Alvos que você definiu
        alvos = ["CDI", "SELIC", "IPCA"]

        # Vamos procurar nas tabelas (tr)
        linhas = soup.find_all('tr')
        
        for linha in linhas:
            texto_linha = linha.get_text()
            for alvo in alvos:
                if alvo in texto_linha:
                    colunas = linha.find_all('td')
                    if len(colunas) >= 3:
                        nome_encontrado = colunas[0].get_text(strip=True).upper()
                        # Verificação exata para não pegar "IPCA-15" no lugar de "IPCA"
                        if nome_encontrado == alvo:
                            valor = colunas[1].get_text(strip=True)
                            data_ref = colunas[2].get_text(strip=True)
                            
                            if not any(i['nome'] == alvo for i in resultados["indicadores"]):
                                resultados["indicadores"].append({
                                    "nome": alvo,
                                    "valor": valor,
                                    "data_referencia": data_ref
                                })

        # Backup: Se a lista ainda estiver vazia, vamos usar busca por texto bruto (Regex)
        if not resultados["indicadores"]:
            for alvo in alvos:
                # Procura o nome do alvo seguido de tags HTML e um valor com %
                padrao = rf"{alvo}.*?<td>(.*?)<\/td>.*?<span class=\"small\">(.*?)<\/span>"
                match = re.search(padrao, html_puro, re.DOTALL | re.IGNORECASE)
                if match:
                    resultados["indicadores"].append({
                        "nome": alvo,
                        "valor": BeautifulSoup(match.group(1), "html.parser").get_text(strip=True),
                        "data_referencia": BeautifulSoup(match.group(2), "html.parser").get_text(strip=True)
                    })

        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Processado!"

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    print(capturar_dados())
