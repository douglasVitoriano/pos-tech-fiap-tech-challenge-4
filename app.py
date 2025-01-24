import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import yfinance as yf
import numpy as np

tags_metadata = [{"name": "tech-challenge-4", "description": "prevendo valor de fechamento da VIV3"}]

app = FastAPI(
    title="VIV3 API",
    description="tech-challenge-4",
    version="1.0",
    openapi_tags=tags_metadata

)

@app.get("/")
def message():
    texto = "api pra prever valor de fechamento da VIV3"
    return texto

@app.post("/predict", tags=["tech-challenge"])
async def predict():

    #ticker
    ticker = yf.Ticker("VIVT3.SA")

    #baixa os ultimos 200 dias de dados de preço sem incluir acoes
    valor_historico = ticker.history(period="200d", actions = False)

    #remove localizacao do fuso
    valor_historico = valor_historico.tz_localize(None) 

    #ordena os dados pelo indice de forma crescente
    valor_historico = valor_historico.sort_index(ascending = False)

    #seleciona linhas a partir do indice 0 e todos as colunas
    dados_entrada = valor_historico

    #substitui valores ausentes por 0
    #dados_entrada = dados_entrada.fillna(0)

    #converte os dados para uma array
    #dados_entrada = dados_entrada.array

    #redimensiona o array para o formato esperado pelo modelo
    dados_entrada_2d = dados_entrada.values


    #carrega o scaler
    scaler = load("scaler.pkl")

    #padroniza os dados de entrada
    dados_entrada_2d = scaler.transform(dados_entrada_2d)

    dados_entrada = dados_entrada_2d.reshape(1, dados_entrada_2d.shape[0], dados_entrada_2d.shape[1])
    
    #carrega modelo de ml
    arquivo = "modelo.pkl"
    model = load(arquivo)
    
    # Faz a previsão
    previsao = model.predict(dados_entrada)

    # Verifique o conteúdo de 'previsao'
    print("Conteúdo da previsão:", previsao)

    # Se for um único valor no array, arredonde o primeiro valor
    previsao_arredondada = np.round(previsao[0], 2) if len(previsao) == 1 else np.round(previsao, 2)

    # Obtém o último preço conhecido
    ultimo_preco = valor_historico.iloc[-1, 3]

    # Verifique o conteúdo de 'ultimo_preco'
    print("Último preço:", ultimo_preco)

    # Monta a resposta com o modelo usado, o último preço e a previsão
    response = {
        "Modelo": arquivo,
        "Ultimo_Preço": round(ultimo_preco, 2),
        "Previsao": previsao_arredondada.tolist() if isinstance(previsao_arredondada, np.ndarray) else previsao_arredondada
    }

    # Verifique o conteúdo de 'response' antes de retornar
    print("Conteúdo da resposta:", response)

    return response

#inicia server
if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port= 3000)
