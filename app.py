from tkinter import *
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

#ROTAS DE API

app = Flask(__name__)

#inserir registros de emprestimos (POST)

DB_NAME = "biblioteca_db"
DB_USER = "postgres"
DB_PASSWORD = "samuel123"
DB_HOST = "localhost"


def get_connection():
    return psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST
        )

@app.route('/emprestimos', methods = ['GET']) 
def get_view_emprestimo():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM lista_emprestimo')
        emprestimos = cur.fetchall()
        return jsonify(emprestimos)
    except psycopg2.Error as e:
        return jsonify({'erro':str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@app.route('/emprestimos/insert', methods = ['POST'])
def add_emprestimo():
    data = request.get_json()
    id_livro = data.get('livro_id')
    id_usuario = data.get('usuario_id')
    status_emprestimo = data.get('status_emprestimo')

    if not id_livro or not id_usuario or not status_emprestimo:
        #messagebox.showwarning('Erro de entrada. preencha todos os campos corretamente')
        return jsonify({'error': 'Dados incompletos'}), 400
    
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO emprestimos(livro_id, usuario_id, status_emprestimo) VALUES (%s, %s, %s)", (int(id_livro), int(id_usuario), status_emprestimo))
        conn.commit()
        return jsonify({'message': 'dados informados com sucesso'}), 200
    except psycopg2.Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

#melhorar para atualizar qualquer coisa
@app.route('/emprestimos/update/<id_emprestimo>', methods=['PATCH'])
def update_emprestimo(id_emprestimo):
    status = ['livro_id', 'usuario_id', 'status_emprestimo']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados incompletos'}), 400

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        for key, value in data.items():
            if key in status:
                cur.execute(f'UPDATE emprestimos SET {key} = %s WHERE id = %s', (str(value), id_emprestimo))
            else:
                return jsonify(f"message: key {key} incorreta ou inexistente")
        conn.commit()
        return jsonify({'message': 'dados atualizados com sucesso'}), 200
    except psycopg2.Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@app.route('/emprestimos/delete/<id_emprestimo>', methods = ["DELETE"])
def delete_emprestimo(id_emprestimo):
    conn = None
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM emprestimos WHERE id = %s",(id_emprestimo))
        conn.commit()
        return jsonify("message: Dados deletados com sucesso")
    except psycopg2.Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)