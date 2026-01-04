import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def capturar_indicadores():
    url = "https://economia.uol.com.br/cotacoes/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        resultados = {
            "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "indicadores": []
        }

        # Nova estratégia: Procurar em todas as tabelas e links do site
        # O UOL geralmente coloca esses dados em elementos <a> ou <td>
        alvos = ["CDI", "SELIC", "IPCA"]
        
        # Vamos buscar todas as linhas de tabelas ou blocos de cotação
        for celula in soup.find_all(['tr', 'div', 'a']):
            texto = celula.get_text().upper()
            
            for alvo in alvos:
                if alvo in texto and len(texto) < 100: # Filtro para pegar apenas o bloco do índice
                    # Tenta encontrar o valor (número com %) dentro ou próximo do elemento
                    parent = celula if not celula.name == 'a' else celula.parent
                    valor_elem = parent.find(lambda tag: '%' in tag.text or ',' in tag.text)
                    
                    if valor_elem:
                        valor = valor_elem.text.strip()
                        # Evita duplicados
                        if not any(i['nome'] == alvo for i in resultados["indicadores"]):
                            resultados["indicadores"].append({
                                "nome": alvo,
                                "valor": valor,
                                "data_referencia": "Atualizado"
                            })

        # Caso a busca automática falhe, vamos usar um seletor específico de backup
        if not resultados["indicadores"]:
             # Busca simplificada por tabelas
             for row in soup.find_all('tr'):
                 cols = row.find_all('td')
                 if len(cols) >= 2:
                     nome = cols[0].text.strip().upper()
                     if any(a in nome for a in alvos):
                         resultados["indicadores"].append({
                             "nome": nome,
                             "valor": cols[1].text.strip(),
                             "data_referencia": "Consulta UOL"
                         })

        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Sucesso!"

    except Exception as e:
        return f"Erro: {str(e)}"

print(capturar_indicadores())
