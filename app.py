from flask import Flask, render_template, request, redirect
import csv
import random
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Variável global para armazenar o caminho do arquivo CSV
csv_file = "/cenarios/cenarios.csv"

UPLOAD_FOLDER = "cenarios"  # Pasta para salvar os arquivos carregados
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# @app.route("/upload_csv", methods=["POST"])
# def upload_csv():
#     global csv_file
#
#     if "file" not in request.files:
#         print("redirect 1")
#         return redirect("/")  # Volta para a página inicial se nenhum arquivo for enviado
#
#     file = request.files["file"]
#
#     if file.filename == "":
#         print("redirect 2")
#         return redirect("/")  # Volta para a página inicial se nenhum arquivo for selecionado
#
#     if file:
#         print("file set")
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(file_path)
#         csv_file = file_path  # Define o arquivo CSV carregado como o ativo
#         return redirect("/")


# Função para gerar um cenário
def gerar_cenario():
    distancia = random.uniform(0, 1500)
    if distancia < 500:
        altitude = random.uniform(0, 150)
    else:
        altitude = random.uniform(0, 100)

    if distancia < 500:
        bateria = random.randint(80, 100)
    elif distancia < 1000:
        bateria = random.randint(50, 80)
    else:
        bateria = random.randint(20, 50)

    if distancia < 500:
        num_satelites = random.randint(8, 12)
    else:
        num_satelites = random.randint(4, 8)

    if distancia < 500:
        qualidade_sinal = random.randint(80, 100)
    elif distancia < 1000:
        qualidade_sinal = random.randint(60, 80)
    else:
        qualidade_sinal = random.randint(30, 60)

    if distancia > 1000:
        obstaculos = random.choice([0, 1])
    else:
        obstaculos = random.choice([0])

    autonomia_restante = 2000 - distancia
    if autonomia_restante <= 0 or bateria < 20:
        status = 3
    elif obstaculos == 1:
        status = 4
    elif qualidade_sinal < 50 and num_satelites < 7:
        status = 3
    elif qualidade_sinal < 50 and num_satelites >= 7:
        status = 2
    elif bateria < 20 or obstaculos == 1:
        status = 4
    elif num_satelites < 7:
        status = 5
    else:
        status = 0

    return [int(distancia), int(bateria), num_satelites, int(qualidade_sinal), obstaculos, status]


@app.route("/")
def index():
    contador_cenarios = 0
    try:
        with open("cenarios.csv", mode="r") as f:
            contador_cenarios = sum(1 for row in csv.reader(f)) - 1  # Subtrair o cabeçalho
    except FileNotFoundError:
        with open("cenarios.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Distância", "Bateria", "Satélites", "Sinal", "Obstáculos", "Status"])
    finally:
        return render_template("index.html", csv_file=csv_file, cenario=None, contador_cenarios=contador_cenarios)


@app.route("/gerar_cenario_rota", methods=["POST"])
def gerar_cenario_rota():
    cenario = gerar_cenario()
    return render_template("index.html", csv_file=csv_file, cenario=cenario, contador_cenarios=0)




@app.route("/salvar_cenario", methods=["POST"])
def salvar_cenario():
    global csv_file
    print("salvando")

    # Obtenha os dados do formulário
    distancia = request.form["distancia"]
    bateria = request.form["bateria"]
    satelites = request.form["satelites"]
    sinal = request.form["sinal"]
    obstaculos = request.form["obstaculos"]
    status = request.form["status"]

    # Converte os dados para o formato correto
    cenario = [int(distancia), int(bateria), int(satelites), int(sinal), int(obstaculos), int(status)]

    # Adiciona o cenário ao arquivo CSV
    with open("cenarios.csv", mode="a", newline="") as file:
        print("add")
        writer = csv.writer(file)
        writer.writerow(cenario)  # Adiciona uma nova linha com os dados do cenário

    return redirect("/")  # Redireciona de volta para a página principal



@app.route("/carregar_csv", methods=["POST"])
def carregar_csv():
    global csv_file
    csv_file = request.form.get("csv_path")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
