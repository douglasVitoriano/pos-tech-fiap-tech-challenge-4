#caso tenha duvidas, checar comentarios em: 
# /home/ayres/Documents/estudos/DSA - FEML4.0/Eng Software para ML/14-construcao-e-deploy-api-ml-prever-preco-bitcoin/8-Cap14/app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import yfinance as yf

tags_metadata = [{"name": "tech-challenge-4", "description": "prevendo valor de fechamento da VIV3"}]

app = FastAPI(
    title="VIV3 API",
    description="tech-challenge-4",
    version="1.0",
    openapi_tags=tags_metadata

)

class Features(BaseModel):
    Model: str

@app.get("/")
def message():
    texto = "api pra prever valor de fechamento da VIV3"
    return texto

@app.post("/predict", tags=["tech-challenge"])
async def predict(Features: Features):

    #ticker
    ticker = yf.Ticker("VIVT3.SA")

    #baixa os ultimos 200 dias de dados de preço sem incluir acoes
    valor_historico = ticker.history(period="200d", actions = False)

    #remove localizacao do fuso
    valor_historico = valor_historico.tz_localize(None) 

    #ordena os dados pelo indice de forma crescente
    valor_historico = valor_historico.sort_index(ascending = False)

    #seleciona linhas a partir do indice 0 e todos as colunas
    dados_entrada = valor_historico.iloc[0,:]

    #substitui valores ausentes por 0
    #dados_entrada = dados_entrada.fillna(0)

    #converte os dados para uma array
    dados_entrada = dados_entrada.array

    #redimensiona o array para o formato esperado pelo modelo
    dados_entrada = dados_entrada.reshape(1,-1)

    #carrega o scaler
    scaler = load("scaler.pkl")

    #padroniza os dados de entrada
    dados_entrada = scaler.transform(dados_entrada)

    #atribui modelo especificado pelo usuario
    Model = Features.Model

    #carrega modelo de ml se especificado
    if Model == "Machine Learning":
        arquivo = "modelo.pkl"
        model = load(arquivo)
    
    #faz o predict
    previsao = model.predict(dados_entrada)

    #obtem o ultimo preco conhecido
    ultimo_preco = valor_historico.iloc[0,3]

    #monta respostas com modelo usado, ultimo preco e previsao
    response = {"Modelo": Model,
                "Ultimo_Preço": round(ultimo_preco, 2),
                "Previsao": round(previsao.tolist()[0], 2)}
    
    return response

#inicia server
if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port= 3000)
