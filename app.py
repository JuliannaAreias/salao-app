# Importações necessárias do Flask e SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, session
from banco_de_dados import Cliente, Servico, Funcionario, Agendamento, db_session
from datetime import datetime, timedelta

# Inicialização do app Flask
app = Flask(__name__)

# Chave secreta necessária para usar sessões no Flask
app.secret_key = "sua_chave_secreta_segura"

# Rota da página inicial
@app.route("/")
def paginaInicial():
    return render_template("PaginaInicial.html")

# Rota de login do cliente
@app.route("/LoginCliente", methods=["GET", "POST"])
def login_clientes():
    if request.method == "POST":
        # Captura os dados enviados pelo formulário
        email = request.form['email']
        senha = request.form['senha']

        # Busca cliente no banco com base no email e senha
        cliente = db_session.query(Cliente).filter_by(email=email, senha=senha).first()

        if cliente:
            # Armazena o nome do cliente na sessão Flask
            session["nome_cliente"] = cliente.nome_cliente
            # Redireciona para a página de agendamento
            return redirect(url_for('cliente_agendamento'))
        else:
            return "Email ou senha incorretos"

    # Se for uma requisição GET, renderiza o formulário
    return render_template("LoginCliente.html")

# Rota para cadastro de novo cliente
@app.route("/CadastrarCliente", methods=["GET", "POST"])
def Cadastro():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Cria novo cliente e salva no banco
        novo_cliente = Cliente(nome_cliente=nome, email=email, senha=senha)
        db_session.add(novo_cliente)
        db_session.commit()

        # Redireciona para a tela de login
        return redirect(url_for('login_clientes'))

    return render_template("CadastrarCliente.html")

# Rota de agendamento do cliente
@app.route("/Cliente", methods=["GET", "POST"])
def cliente_agendamento():
    # Consulta os serviços e profissionais disponíveis no banco
    servicos = db_session.query(Servico).all()
    profissionais = db_session.query(Funcionario).all()

    # Cria um dicionário com os profissionais por tipo de serviço
    profissionais_por_servico = {}
    for s in servicos:
        nomes = [f.nome_funcionario for f in profissionais if f.especialidade == s.servico_nome]
        profissionais_por_servico[s.servico_nome] = nomes

    if request.method == "POST":
        # Dados do formulário de agendamento
        nome = request.form["nome"]
        servico_nome = request.form["servico"]
        profissional_nome = request.form["profissional"]
        data = request.form["data"]
        horario = request.form["horario"]

        # Busca o cliente, serviço e profissional no banco
        cliente = db_session.query(Cliente).filter_by(nome_cliente=nome).first()
        servico = db_session.query(Servico).filter_by(servico_nome=servico_nome).first()
        profissional = db_session.query(Funcionario).filter_by(nome_funcionario=profissional_nome).first()

        # Validação: se algum item não for encontrado
        if not cliente or not servico or not profissional:
            return "Cliente, serviço ou profissional não encontrado."

        # Converte os dados de data/hora para datetime
        data_hora_inicio = datetime.strptime(f"{data} {horario}", "%Y-%m-%d %H:%M")
        data_hora_fim = data_hora_inicio + timedelta(minutes=servico.duracao_minutos)

        # Cria o objeto de agendamento e salva no banco
        novo_agendamento = Agendamento(
            id_cliente=cliente.id_cliente,
            id_funcionario=profissional.id_funcionario,
            id_servico=servico.id_servico,
            data_hora_inicio=data_hora_inicio,
            data_hora_fim=data_hora_fim,
            status="agendado",
            ultima_atualizacao=datetime.now()
        )

        db_session.add(novo_agendamento)
        db_session.commit()

        # Recarrega a página com os dados atualizados
        return render_template(
            "Cliente.html",
            servicos=[s.servico_nome for s in servicos],
            profissionais_por_servico=profissionais_por_servico,
            nome_cliente=session.get("nome_cliente", "")
        )

    # Renderiza o formulário de agendamento (GET)
    return render_template(
        "Cliente.html",
        servicos=[s.servico_nome for s in servicos],
        profissionais_por_servico=profissionais_por_servico,
        nome_cliente=session.get("nome_cliente", "")
    )

# Rota da página do profissional (a ser implementada)
@app.route("/Profissional")
def profissional():
    agora = datetime.now()

    # Buscar todos os agendamentos futuros
    agendamentos_futuros = db_session.query(Agendamento).filter(
        Agendamento.data_hora_inicio >= agora
    ).order_by(Agendamento.data_hora_inicio.asc()).all()

    # Montar lista com informações completas
    resumo = []
    for ag in agendamentos_futuros:
        cliente = db_session.query(Cliente).filter_by(id_cliente=ag.id_cliente).first()
        servico = db_session.query(Servico).filter_by(id_servico=ag.id_servico).first()
        funcionario = db_session.query(Funcionario).filter_by(id_funcionario=ag.id_funcionario).first()

        resumo.append({
            "cliente": cliente.nome_cliente,
            "servico": servico.servico_nome,
            "profissional": funcionario.nome_funcionario,
            "data": ag.data_hora_inicio.strftime("%d/%m/%Y"),
            "hora": ag.data_hora_inicio.strftime("%H:%M")
        })

    return render_template("Profissional.html", agendamentos=resumo)

# Executa o app Flask
if __name__ == "__main__":
    app.run(debug=True)
