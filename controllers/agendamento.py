from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.agendamento import Agendamento
from models.cliente import Cliente
from models.procedimento import Procedimento

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/')
def index():
    # Filtros
    filtros = {
        'data': request.args.get('data', ''),
        'cliente': request.args.get('cliente', ''),
        'procedimento': request.args.get('procedimento', '')
    }
    
    agendamentos = Agendamento.obter_todos(filtros)
    clientes = Cliente.obter_para_select()
    procedimentos = Procedimento.obter_para_select()
    
    return render_template('agendamentos/index.html', 
                          agendamentos=agendamentos, 
                          clientes=clientes, 
                          procedimentos=procedimentos,
                          data_filtro=filtros['data'],
                          cliente_filtro=filtros['cliente'],
                          procedimento_filtro=filtros['procedimento'])

@agendamento_bp.route('/criar', methods=['POST'])
def criar_agendamento():
    data = request.form['data']
    hora = request.form['hora']
    cliente_id = request.form['cliente_id']
    procedimento_id = request.form['procedimento_id']
    observacoes = request.form.get('observacoes', '')
    
    sucesso, mensagem = Agendamento.criar(data, hora, cliente_id, procedimento_id, observacoes)
    flash(mensagem)
    
    return redirect(url_for('agendamento.index'))

@agendamento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    if request.method == 'POST':
        data = request.form['data']
        hora = request.form['hora']
        cliente_id = request.form['cliente_id']
        procedimento_id = request.form['procedimento_id']
        observacoes = request.form.get('observacoes', '')
        status = request.form['status']
        
        sucesso, mensagem = Agendamento.atualizar(id, data, hora, cliente_id, procedimento_id, observacoes, status)
        flash(mensagem)
        
        return redirect(url_for('agendamento.index'))
    else:
        agendamento = Agendamento.obter_por_id(id)
        clientes = Cliente.obter_para_select()
        procedimentos = Procedimento.obter_para_select()
        
        return render_template('agendamentos/editar.html', 
                              agendamento=agendamento, 
                              clientes=clientes, 
                              procedimentos=procedimentos)

@agendamento_bp.route('/excluir/<int:id>')
def excluir_agendamento(id):
    sucesso, mensagem = Agendamento.excluir(id)
    flash(mensagem)
    
    return redirect(url_for('agendamento.index'))