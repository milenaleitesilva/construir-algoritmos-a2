import datetime
import requests

def cotar():
    cotacoes = []
    hoje = datetime.date.today()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cache_cotacoes = {}

    def obter_cotacao_dia(data):
        data_busca = data
        while data_busca.weekday() >= 5:
            data_busca -= datetime.timedelta(days=1)

        data_str = data_busca.strftime("%m-%d-%Y")

        if data_str in cache_cotacoes:
            return cache_cotacoes[data_str]
        dias_retrocessos = 0
        while dias_retrocessos < 10:
            data_fmt = data_busca.strftime("%m-%d-%Y")
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data_fmt}'&$format=json"
            
            try:
                resposta = requests.get(url, headers=headers, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json().get("value", [])

                if dados:
                    valor = dados[0]["cotacaoCompra"]
                    cache_cotacoes[data_str] = valor
                    return valor
            except Exception:
                pass
            data_busca -= datetime.timedelta(days=1)
            dias_retrocessos += 1

        return None
    for i in range(365):
        dia_atual = hoje - datetime.timedelta(days=i)
        valor = obter_cotacao_dia(dia_atual)
        if valor is not None:
            cotacoes.append(valor)

    return cotacoes


if __name__ == "__main__":
    resultado = cotar()
    print("Quantidade de cotações retornadas:", len(resultado))
    print(resultado)
