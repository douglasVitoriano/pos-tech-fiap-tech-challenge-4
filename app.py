import mlflow

import uvicorn
from fastapi import FastAPI
from joblib import load
import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
import mlflow
import mlflow.keras  # Importa o módulo Keras do MLflow

tags_metadata = [{"name": "tech-challenge-4", "description": "prevendo valor de fechamento da VIV3"}]

app = FastAPI(
    title="VIV3 API",
    description="tech-challenge-4",
    version="1.0",
    openapi_tags=tags_metadata
)

# Inicializa o MLflow
mlflow.set_tracking_uri("http://localhost:5000")  # Defina o URI para o servidor MLflow
mlflow.set_experiment("viv3_model_predictor")  # Nome do experimento

@app.get("/")
def message():
    texto = "API para prever valor de fechamento da VIV3"
    return texto

@app.get("/predict", tags=["tech-challenge"])
async def predict():

    #ticker
    ticker = yf.Ticker("VIVT3.SA")

    #baixa os ultimos 150 dias de dados de preço
    valor_historico = ticker.history(period="150d", actions=False)

    #remove localizacao do fuso
    valor_historico = valor_historico.tz_localize(None) 

    #ordena os dados pelo índice
    valor_historico = valor_historico.sort_index(ascending=False)

    #seleciona os dados de entrada
    dados_entrada = valor_historico

    #carrega o scaler
    scaler = load("scaler.pkl")

    #padroniza os dados de entrada
    dados_entrada_2d = scaler.transform(dados_entrada.values)

    dados_entrada = dados_entrada_2d.reshape(1, dados_entrada_2d.shape[0], dados_entrada_2d.shape[1])

    #carrega o modelo de ML
    arquivo = "modelo_completo.h5"
    model = load_model(arquivo, compile=False)

    # Inicia o rastreamento do MLflow para a previsão
    with mlflow.start_run():

        # Faz a previsão
        previsao = model.predict(dados_entrada)

        # Se for um único valor no array, arredonde
        previsao_arredondada = np.round(previsao[0], 2) if len(previsao) == 1 else np.round(previsao, 2)

        # Obtém o último preço conhecido
        ultimo_preco = valor_historico.iloc[-1, 3]

        # Log de métricas no MLflow (por exemplo, último preço e previsão)
        mlflow.log_metric("Ultimo_Preço", round(ultimo_preco, 2))
        mlflow.log_metric("Previsao", previsao_arredondada.tolist()[0])

        # Log do modelo
        mlflow.keras.log_model(model, "modelo_viv3")

        # Prepara a resposta
        response = {
            "Modelo": arquivo,
            "Ultimo_Preço": round(ultimo_preco, 2),
            "Previsao": previsao_arredondada.tolist() if isinstance(previsao_arredondada, np.ndarray) else previsao_arredondada
        }

        # Retorna a resposta
        return response

# Inicia o servidor
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3000)
