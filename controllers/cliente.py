from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.cliente import Cliente
from models.convenio import Convenio

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
def index():
    clientes = Cliente.obter_todos()
    convenios = Convenio.obter_todos()
    
    return render_template('clientes/index.html', clientes=clientes, convenios=convenios)

@cliente_bp.route('/criar', methods=['POST'])
def criar_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form.get('email', '')
    convenio_id = request.form.get('convenio_id', 1)
    num_carteirinha = request.form.get('num_carteirinha', '')
    
    sucesso, mensagem = Cliente.criar(nome, telefone, email, convenio_id, num_carteirinha)
    flash(mensagem)
    
    return redirect(url_for('cliente.index'))

@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form.get('email', '')
        convenio_id = request.form.get('convenio_id', 1)
        num_carteirinha = request.form.get('num_carteirinha', '')
        
        sucesso, mensagem = Cliente.atualizar(id, nome, telefone, email, convenio_id, num_carteirinha)
        flash(mensagem)
        
        return redirect(url_for('cliente.index'))
    else:
        cliente = Cliente.obter_por_id(id)
        convenios = Convenio.obter_todos()
        
        return render_template('clientes/editar.html', 
                              cliente=cliente, 
                              convenios=convenios)

@cliente_bp.route('/excluir/<int:id>')
def excluir_cliente(id):
    sucesso, mensagem = Cliente.excluir(id)
    flash(mensagem)
    
    return redirect(url_for('cliente.index'))