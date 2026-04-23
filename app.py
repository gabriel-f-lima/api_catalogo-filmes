from flask import Flask, request, jsonify, render_template, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from controllers.adicionar_filme_controller import adiconar_filme_controller
from controllers.buscar_filme_porID_controller import buscar_filme_porID_controller
from controllers.buscar_filmes_controller import buscar_filmes_controller
from database import get_connection
from controllers.atualizar_filme_controller import atualizar_filme
from controllers.remover_filme_controller import remover_filme
from flask import redirect
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

# Teste API
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garantir que a pasta existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API de catalogo de filmes"}), 200

# Ping

@app.route('/ping', methods=['GET'])
def ping():
    conn = get_connection()
    conn.close()
    return jsonify({"message": "pong! API Rodando!", "db": str(conn)}), 200


# 🔹 Listar todos os filmes

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    try:
        filmes = buscar_filmes_controller()
        return render_template("index.html", filmes=filmes), 200
    except Exception as ex:
        import traceback
        print("MENSAGEM DE ERRO:")
        print(str(ex))
        traceback.print_exc() # Isso vai mostrar a linha exata e o motivo técnico no terminal
        return jsonify({"message": f"Erro técnico: {str(ex)}"}), 500

# 🔹 Buscar filme por ID

@app.route('/filmes/<int:id>', methods=['GET'])
def buscar_filme(id):
    try:
        filme = buscar_filme_porID_controller(id)
        return jsonify(filme), 200
    except:
        return jsonify({"erro": "Erro interno no servidor"}), 404

# 🔹 Adicionar novo filme

@app.route('/filmes', methods=['POST'])
def adicionar_filme_route():
    try:
        dados = request.get_json()
        filme_salvo = adiconar_filme_controller(dados)
        print('Dados request--------', filme_salvo)
        return jsonify(filme_salvo), 200
    except Exception as ex:
        print('Erro adicionar filme', str(ex))
        return jsonify({"message": "Erro interno no servidor"}), 500

# 🔹 Atualizar filme

@app.route('/filmes/<int:id>', methods=['PUT'])
def atualizar_filme_route(id):
    try:
        dados = request.get_json()
        return render_template("editar_filme.html", filme=dados)
        resposta = atualizar_filme(dados, id)
        return jsonify(resposta), 200
    except Exception as ex:
        print('Erro atualizar filme', str(ex))
        return jsonify({"message": "Erro interno no servidor"}), 500


# 🔹 Remover filme

@app.route('/deletar/<int:id>', methods=['POST', 'DELETE'])
def deletar_filme(id): 
    try:
        remover_filme(id) # Chama seu controller/repositório
        return redirect(url_for('listar_filmes'))
    except Exception as ex:
        print('Erro remover filme', str(ex))
        return jsonify({"message": "Erro ao remover filme"}), 500


@app.route('/novo', methods=['GET', 'POST'])
def novo_filme(): # Nome alterado para bater com o HTML
    try:
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            genero = request.form.get('genero')
            ano = request.form.get('ano')
            file = request.files.get('capa')

            if file and allowed_file(file.filename):
                extensao = file.filename.rsplit('.', 1)[1].lower()
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                
                # Salva na pasta uploads dentro de static
                caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_unico)
                file.save(caminho_completo)

                # Salvamos apenas o caminho relativo para o Flask encontrar fácil depois
                url_banco = f"uploads/{nome_unico}"
                
                dados = {
                    "titulo": titulo,
                    "genero": genero,
                    "ano": ano,
                    "url_capa": url_banco 
                }

                adiconar_filme_controller(dados) 
                return redirect(url_for("listar_filmes"))
            
        return render_template("novo_filme.html")
    except Exception as ex:
        print(f'Erro ao adicionar filme: {ex}')
        return jsonify({"message": "Erro ao salvar filme"}), 500

# Mude o nome desta função para 'editar_filme' para bater com o HTML
@app.route('/editar', methods=['GET', 'POST'])
def editar_filme():
    filme_id = request.args.get('id') or request.args.get('filme_id')
    
    if not filme_id:
        return "ID do filme não fornecido", 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        if request.method == 'POST':
            novo_titulo = request.form.get('titulo')
            novo_genero = request.form.get('genero')
            novo_ano = request.form.get('ano')
            
            # 1. Pegar o novo arquivo de imagem (se houver)
            file = request.files.get('capa') 
            
            if file and allowed_file(file.filename):
                # Se enviou uma nova foto, fazemos o upload igual na rota /novo
                extensao = file.filename.rsplit('.', 1)[1].lower()
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_unico)
                file.save(caminho_completo)
                url_capa = f"uploads/{nome_unico}"
                
                # Update incluindo a nova imagem
                cur.execute("""
                    UPDATE filmes 
                    SET titulo = %s, genero = %s, ano = %s, url_capa = %s 
                    WHERE id = %s
                """, (novo_titulo, novo_genero, novo_ano, url_capa, filme_id))
            else:
                # Se NÃO enviou foto nova, atualiza apenas os textos
                cur.execute("""
                    UPDATE filmes 
                    SET titulo = %s, genero = %s, ano = %s 
                    WHERE id = %s
                """, (novo_titulo, novo_genero, novo_ano, filme_id))
            
            conn.commit()
            return redirect(url_for('listar_filmes'))

        # GET: Busca dados para o formulário
        cur.execute("SELECT * FROM filmes WHERE id = %s;", (filme_id,))
        filme = cur.fetchone()
        return render_template('editar_filme.html', filme=filme)

    except Exception as e:
        print(f"Erro ao editar: {e}")
        return "Erro interno", 500
    finally:
        cur.close()
        conn.close()      

if __name__ == '__main__':
    app.run(debug=True, port=5001)