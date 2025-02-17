import requests


# Faz a requisição à API
resposta = requests.get("http://localhost:3000/predict")

# Imprime o código de status da resposta
print("Status code:", resposta.status_code)


# Verifica se a resposta foi bem-sucedida
if resposta.status_code == 200:
    # Imprime a resposta JSON
    print('\nResposta da API:\n', resposta.json())
else:
    print('\nErro na requisição:\n', resposta.text)

print('\nObrigado Por Usar Esta API!\n')
