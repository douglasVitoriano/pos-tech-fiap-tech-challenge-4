# Desafio de Desenvolvimento do Modelo LSTM


## Descrição do Projeto

Este projeto tem como objetivo desenvolver um modelo de deep learning utilizando LSTM para prever os preços das ações da VIVT3. O projeto inclui a coleta de dados, pré-processamento, desenvolvimento do modelo, treinamento, avaliação, salvamento e deploy do modelo, além de monitoramento utilizando MLflow.

## Estrutura do Projeto

1. **Coleta de Dados**
   - **Escolha da Empresa**: Telefônica Brasil (VIVT3.SA)
   - **Fonte de Dados**: Biblioteca `yfinance` para coletar os dados históricos das ações.
   - **Período de Dados**: Últimos 5 anos, de 1º de janeiro de 2020 a 31º de dezembro de 2024.

2. **Pré-processamento de Dados**
   - Tratamento de valores ausentes.
   - Verificação de outliers.
   - Normalização e padronização dos dados.
   - Salvamento dos dados pré-processados.

3. **Desenvolvimento do Modelo LSTM**
   - **Construção do Modelo**: Implementação de um modelo LSTM para capturar padrões temporais nos dados de preços das ações.
   - **Treinamento**: Treinamento do modelo utilizando uma parte dos dados e ajuste dos hiperparâmetros para otimizar o desempenho.
   - **Avaliação**: Avaliação do modelo utilizando dados de validação e métricas como MAE, RMSE e MAPE.

4. **Salvamento e Exportação do Modelo**
   - **Salvar o Modelo**: Salvamento do modelo treinado em um formato que possa ser utilizado para inferência, neste caso, utilizamos o modelo .pkl

5. **Deploy do Modelo**
   - **Criação da API**: Desenvolvimento de uma API RESTful utilizando FastAPI para servir o modelo. A API permite que o usuário forneça dados históricos de preços e receba previsões dos preços futuros.

6. **Escalabilidade e Monitoramento**
   - **Monitoramento**: Configuração de ferramentas de monitoramento para rastrear a performance do modelo em produção, incluindo tempo de resposta e utilização de recursos. Neste caso, utilizamos o MLFlow.

## Requisitos

- Python 3.8+
- Bibliotecas: `tensorflow`, `scikit-learn`, `pandas`, `yfinance`, `fastapi`, `uvicorn`, `joblib`, `mlflow`, `matplotlib`, `numpy`

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/douglasVitoriano/pos-tech-fiap-tech-challenge-4.git
   cd pos-tech-fiap-tech-challenge-4
