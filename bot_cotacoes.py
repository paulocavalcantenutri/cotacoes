import requests
import json
from datetime import datetime

def capturar_indicadores():
    resultados = {
        "data_da_extracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "indicadores": []
    }

    try:
        # 1. Capturar SELIC e CDI (Via API HG Brasil - Gratuita para pequenos volumes)
        # Usamos essa API pois ela já entrega o dado mastigado
        url_hg = "https://api.hgbrasil.com/finance/taxes?key=console" # Chave pública de teste
        res = requests.get(url_hg).json()
        
        if res['results']:
            dados = res['results'][0]
            resultados["indicadores"].append({
                "nome": "SELIC",
                "valor": f"{dados['selic']}%",
                "data_referencia": dados['date']
            })
            resultados["indicadores"].append({
                "nome": "CDI",
                "valor": f"{dados['cdi']}%",
                "data_referencia": dados['date']
            })

        # 2. Capturar IPCA (Via API do IBGE - Oficial e Grátis)
        # Pega o acumulado dos últimos 12 meses
        url_ibge = "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/-1/variaveis/2265?localidades=N1[all]"
        res_ibge = requests.get(url_ibge).json()
        
        if res_ibge:
            valor_ipca = res_ibge[0]['resumes'][0]['res'][0]['v']
            mes_ipca = res_ibge[0]['resumes'][0]['res'][0]['p']
            resultados["indicadores"].append({
                "nome": "IPCA (12 meses)",
                "valor": f"{valor_ipca}%",
                "data_referencia": mes_ipca
            })

        # Salva o JSON
        with open('indicadores.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        
        return "Dados atualizados com sucesso via API!"

    except Exception as e:
        return f"Erro na captura: {str(e)}"

print(capturar_indicadores())
