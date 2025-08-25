from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    concluida = db.Column(db.Boolean, default=False)

class Compromisso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    data_hora = db.Column(db.String(50))

class Humor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String(50))

db.create_all()

# -------- Rotas ---------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarefas', methods=['GET', 'POST'])
def tarefas():
    if request.method == 'POST':
        data = request.json
        tarefa = Tarefa(descricao=data['descricao'])
        db.session.add(tarefa)
        db.session.commit()
        return jsonify({'id': tarefa.id, 'descricao': tarefa.descricao, 'concluida': tarefa.concluida})
    else:
        tarefas = Tarefa.query.all()
        return jsonify([{'id': t.id, 'descricao': t.descricao, 'concluida': t.concluida} for t in tarefas])

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    data = request.json
    tarefa.concluida = data['concluida']
    db.session.commit()
    return jsonify({'id': tarefa.id, 'concluida': tarefa.concluida})

@app.route('/compromissos', methods=['GET', 'POST'])
def compromissos():
    if request.method == 'POST':
        data = request.json
        c = Compromisso(descricao=data['descricao'], data_hora=data['data_hora'])
        db.session.add(c)
        db.session.commit()
        return jsonify({'id': c.id, 'descricao': c.descricao, 'data_hora': c.data_hora})
    else:
        compromissos = Compromisso.query.all()
        return jsonify([{'id': c.id, 'descricao': c.descricao, 'data_hora': c.data_hora} for c in compromissos])

@app.route('/humor', methods=['GET', 'POST'])
def humor():
    if request.method == 'POST':
        data = request.json
        h = Humor.query.first()
        if not h:
            h = Humor(valor=data['valor'])
            db.session.add(h)
        else:
            h.valor = data['valor']
        db.session.commit()
        return jsonify({'valor': h.valor})
    else:
        h = Humor.query.first()
        return jsonify({'valor': h.valor if h else ''})

if __name__ == '__main__':
    app.run(debug=True)
