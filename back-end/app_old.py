#Importar o flask e o os
from flask import Flask, send_from_directory, request, jsonify 
import os, openpyxl #Biblioteca para ler arquivos Excel
from datetime import (
    datetime,
)
      
#Obter o caminho base do projeto, o caminho da pasta Front e o caminho da pasta static para conseguir usar os arquivos CSS
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 
FRONTEND_DIR = os.path.join(BASE_DIR, 'front-end')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

#Obter o caminho do Banco de Dados e do arquivo Excel para ler os dados dos clientes
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'DB')
EXCEL_FILE = os.path.join(DB_DIR, 'clientes.xlsx')

#Criação das colunas do banco de dados (Linha 1)
COLUMNS = ["ID", "Nome", "CPF", "E-mail", "Telefone", "Endereço", "Observações", "Data Cadastro"]

def init_excel():
    #Verificação se o diretório do DB existe. Se não existir ele cria o diretório
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR) #Criar o diretório do DB

    #Verificação se o arquivo do Excel existe. Se não existir ele cria o arquivo e adiciona as colunas (Linha 1)
    if not os.path.exists(EXCEL_FILE):
        workbook = openpyxl.Workbook() #Cria uma planilha
        sheet = workbook.active        #Pega a planilha ativa 
        sheet.title = "Clientes"       #Dá um nome para a planilha
        sheet.append(COLUMNS)          #Adiciona as colunas na primeira linha da planilha
        workbook.save(EXCEL_FILE)      #Salva o arquivo do Excel

#Criar o server (Os parâmetros permitem utilizar o css)
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/" + STATIC_DIR)

#Criar a route da página, no caso a raiz/home
@app.route("/")                               
def home():
    return send_from_directory(FRONTEND_DIR, "index.html") #Retornar o HTML                      

#Página de Consulta
@app.route("/consulta")                               
def consulta_page():
    return send_from_directory(FRONTEND_DIR, "consulta.html") #Retornar o HTML      

#Página de Alterar
@app.route("/alterar")                               
def alterar_page():
    return send_from_directory(FRONTEND_DIR, "alterar.html") #Retornar o HTML 

@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("../front-end/assets", filename)

@app.route("/cadastrar", methods=["POST"])
def cadastrar_cliente():
    try:
        data = request.json
        required_fields = ["nome", "cpf", "email", "telefone", "endereco"]
        if not all(field in data and data[field] for field in required_fields):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Todos os campos obrigatórios devem estar definidos.",
                    }
                ),
                400,
            )
        
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active

        last_id = 0

        if sheet.max_row > 1:
            last_id = sheet.cell(row=sheet.max_row, column=1).value or 0            
        
        new_id = last_id + 1
        
        novo_cliente = [
            new_id, 
            data.get("nome"), 
            data.get("cpf"), 
            data.get("email"), 
            data.get("telefone"), 
            data.get("endereco"), 
            data.get("observacao"), 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        sheet.append(novo_cliente)
        workbook.save(EXCEL_FILE)

        return(
            jsonify(
                {
                    "status": "success",
                    "message": "Cliente cadastrado com sucesso.",
                    "id": new_id
                }
            )
        )
    
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Erro ao cadastrar cliente: {str(e)}"
                }
            ),
            500,
        )
    
@app.route("/buscar", methods=["GET"])
def buscar_clientes():
    nome_query = request.args.get("nome", "").lower()

    try:
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active
        resultados = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row): continue
            
            cliente = {}
            for i, col_name in enumerate(COLUMNS):
                val = row[i] if i < len(row) else None
                cliente[col_name] = val if val is not None else ""

            nome_cliente = str(cliente.get("Nome") or "").lower()
        
            if nome_query in nome_cliente:
                resultados.append(cliente)

        return jsonify(resultados)
    
    except FileNotFoundError:
        return (jsonify({"status": "error", "message": "Arquivo de dados não encontrado."}), 404)
        
    except Exception as e:
        return (jsonify({"status": "error", "message": f"Não foi possível ler os dados: {str(e)}"}), 500)

@app.route("/cliente/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):

    try:
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active

        for row_idx in range(2, sheet.max_row + 1):
            row_id = sheet.cell(row=row_idx, column=1).value
            if row_id == cliente_id:
                row_values = [cell.value for cell in sheet[row_idx]]
                
                cliente = {}
                for i, col_name in enumerate(COLUMNS):
                    val = row_values[i] if i < len(row_values) else None
                    cliente[col_name] = val if val is not None else ""
                
                return jsonify(cliente)
            
        return (jsonify({"status": "error", "message": "Cliente não encontrado."}), 404)

    except Exception as e:
        return (jsonify({"status": "error", "message": f"Erro ao buscar cliente: {str(e)}"}), 500)

@app.route("/api/atualizar/<int:cliente_id>", methods=["POST"])
def atualizar_cliente(cliente_id):
    
    try:
        data = request.json
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active

        row_to_update = -1

        for row_idx in range(2, sheet.max_row + 1):
            if sheet.cell(row=row_idx, column=1).value == cliente_id:
                row_to_update = row_idx
                break

        if row_to_update == -1:
            return (
                jsonify({
                    "status": "error", 
                    "message": f"Cliente não encontrado para atualização: {str(e)}"
                }), 
                404,
            )

    except Exception as e:
        return (
            jsonify({
                "status": "error", 
                "message": f"Erro ao acessar o arquivo de dados: {str(e)}"
            }), 
            500
        )
    #Atualizar os campos do cliente na planilha
    sheet.cell(row = row_to_update, column = 2, value = data.get("nome"))
    sheet.cell(row = row_to_update, column = 3, value = data.get("cpf"))
    sheet.cell(row = row_to_update, column = 4, value = data.get("email"))
    sheet.cell(row = row_to_update, column = 5, value = data.get("telefone"))
    sheet.cell(row = row_to_update, column = 6, value = data.get("endereco"))
    sheet.cell(row = row_to_update, column = 7, value = data.get("observacao"))

    workbook.save(EXCEL_FILE)

    return (
        jsonify({
            "status": "success", 
            "message": "Dados do cliente atualizados com sucesso."
        })
    )



if __name__ == "__main__":
    print("BASE_DIRECTORY:", BASE_DIR)
    print("FRONTEND_DIRECTORY:", FRONTEND_DIR)
    print("STATIC_DIRECTORY:", STATIC_DIR)
    init_excel()
    app.run(debug=True)

