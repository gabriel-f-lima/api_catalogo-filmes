from flask import Flask, request, jsonify, render_template, url_for

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
    except:
        return jsonify({"messege": "Erro interno no servidor"}), 500

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

@app.route('/filmes/<int:id>', methods=['DELETE'])
def remover_filme_route(id):
    try:
        filme = remover_filme(id)
        return jsonify(filme), 200
    except Exception as ex:
        print('Erro remover filme', str(ex))
        return jsonify({"message": "Erro interno no servidor"}), 500


@app.route('/novo', methods=['GET', 'POST'])
def adicionar_filme():
    try:
        if request.method == 'POST':
            dados = request.form.to_dict() 
            adiconar_filme_controller(dados) 
            return redirect(url_for("listar_filmes"))
            
        return render_template("novo_filme.html")
    except Exception as ex:
        print('Erro ao adicionar filme------', str(ex))
        return jsonify({"message": "Erro ao salvar filme"}),

@app.route('/editar', methods=['GET', 'POST']) # Mudei para POST por ser o padrão em formulários HTML
def atualizar_filme():
    # Pega o ID da URL (ex: /editar?filme_id=1)
    filme_id = request.args.get('filme_id')
    
    # Previne erro caso o ID não seja passado na URL
    if not filme_id:
        return "ID do filme não fornecido", 400

    conn = get_connection() # Correção: Parênteses adicionados!
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Se o usuário submeteu o formulário com as alterações
        if request.method == 'POST':
            novo_titulo = request.form.get('titulo')
            cur.execute("UPDATE filmes SET titulo = %s WHERE id = %s", (novo_titulo, filme_id))
            conn.commit()
            return redirect(url_for('alguma_outra_rota'))

        # Se for GET (apenas carregando a página de edição)
        cur.execute("SELECT * FROM filmes WHERE id = %s;", (filme_id,))
        filme = cur.fetchone()
        print('filme -------------------------', filme)

        return render_template('editar_filme.html', filme=filme)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return "Erro interno do servidor", 500

    finally:
        # O bloco finally garante que a conexão será fechada, dando erro ou não
        cur.close()
        conn.close()        

if __name__ == '__main__':
    app.run(debug=True, port=5001)