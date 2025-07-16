from sqlalchemy import create_engine, Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Conexão com o banco de dados SQLite
db = create_engine("sqlite:///bancosalao.db")
Session = sessionmaker(bind=db)
db_session = Session()  # Renomeado para não confundir com 'session' do Flask

Base = declarative_base()

# --------------------------
# MODELOS DAS TABELAS
# --------------------------

class Servico(Base):
    __tablename__ = "servico"
    id_servico = Column("id", Integer, primary_key=True, autoincrement=True)
    servico_nome = Column("Nome do Serviço", String)
    duracao_minutos = Column("Tempo de duração", Integer)
    preco = Column("Preço do serviço", Numeric(precision=10, scale=2))

    def __init__(self, servico_nome, duracao_minutos, preco):
        self.servico_nome = servico_nome
        self.duracao_minutos = duracao_minutos
        self.preco = preco


class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column("idcliente", Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column("Nome do Cliente", String)
    email = Column("Email", String)
    senha = Column("Senha", String(9), nullable=False)

    def __init__(self, nome_cliente, email, senha):
        self.nome_cliente = nome_cliente
        self.email = email
        self.senha = senha


class Funcionario(Base):
    __tablename__ = "funcionario"
    id_funcionario = Column("id do funcionario", Integer, primary_key=True, autoincrement=True)
    nome_funcionario = Column("Nome do Funcionário", String)
    especialidade = Column("Especialidade", String)

    def __init__(self, nome_funcionario, especialidade):
        self.nome_funcionario = nome_funcionario
        self.especialidade = especialidade


class Agendamento(Base):
    __tablename__ = "agendamento"
    id_agendamento = Column("Id do agendamento", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("Id cliente", Integer, ForeignKey("cliente.idcliente"))
    id_funcionario = Column("Id do funcionário", Integer, ForeignKey("funcionario.id do funcionario"))
    id_servico = Column("Id do serviço", Integer, ForeignKey("servico.id"))
    data_hora_inicio = Column("Data e Hora do Inicio do agendamento", DateTime)
    data_hora_fim = Column("Data e Hora do fim do agendamento", DateTime)
    status = Column("Status do agendamento", String)
    ultima_atualizacao = Column("Ultima atualização", DateTime)

    def __init__(self, id_cliente, id_funcionario, id_servico, data_hora_inicio, data_hora_fim, status, ultima_atualizacao):
        self.id_cliente = id_cliente
        self.id_funcionario = id_funcionario
        self.id_servico = id_servico
        self.data_hora_inicio = data_hora_inicio
        self.data_hora_fim = data_hora_fim
        self.status = status
        self.ultima_atualizacao = ultima_atualizacao


class Horario(Base):
    __tablename__ = "horario"
    id_horarios = Column("Id do agendamento", Integer, primary_key=True, autoincrement=True)
    id_funcionario = Column("Id do funcionário", Integer, ForeignKey("funcionario.id do funcionario"))
    dia_semana = Column("Dia da semana", String)
    hora_inicio = Column("Horario do inicio do atendimento", DateTime)
    hora_fim = Column("Horario do fim do atendimento", DateTime)
    disponibilidade = Column("Disponibilidade", String)

    def __init__(self, id_funcionario, dia_semana, hora_inicio, hora_fim, disponivel):
        self.id_funcionario = id_funcionario
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.disponibilidade = disponivel


# --------------------------
# CRIAÇÃO DAS TABELAS
# --------------------------
Base.metadata.create_all(bind=db)

# --------------------------
# CADASTRO INICIAL DE DADOS
# --------------------------

# Cadastrar serviços se ainda não existirem
servico_existente = db_session.query(Servico).first()
if not servico_existente:
    servicos = [
        Servico("Manicure", 45, 35.00),
        Servico("Designer de Sobrancelha", 20, 35.00),
        Servico("Corte de cabelo", 30, 60.00),
        Servico("Pedicure", 30, 25.00),
        Servico("Depilação", 30, 30.00)
    ]
    db_session.add_all(servicos)
    db_session.commit()
    print("Serviços cadastrados com sucesso!")
else:
    print("Serviços já existem no banco.")

# Cadastrar funcionários se ainda não existirem
funcionario_existente = db_session.query(Funcionario).first()
if not funcionario_existente:
    funcionarios = [
        Funcionario("Camila Silva", "Manicure"),
        Funcionario("Larissa Almeida", "Designer de Sobrancelha"),
        Funcionario("João Costa", "Corte de cabelo"),
        Funcionario("Patrícia Santos", "Pedicure"),
        Funcionario("Fernanda Rocha", "Depilação")
    ]
    db_session.add_all(funcionarios)
    db_session.commit()
    print("Funcionários cadastrados com sucesso!")
else:
    print("Funcionários já existem no banco.")
