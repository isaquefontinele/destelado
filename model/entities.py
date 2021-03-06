import datetime
import locale

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
locale.setlocale( locale.LC_ALL, 'pt_BR.utf8' )

class Deputado(Base):
    __tablename__ = 'deputado'

    id = Column(Integer, primary_key = True)
    nome = Column(String(80))
    estado = Column(String(2))
    partido = Column(String(10))
    assiduidades = relationship("Assiduidade")
    gastos = relationship("Gasto")

    def __init__(self, nome, estado, partido):
        self.nome = nome
        self.estado = estado
        self.partido = partido
    
    def total_faltas(self):
        return sum(map(lambda x : x.faltas, self.assiduidades))

    def total_presencas(self):
        return sum(map(lambda x : x.presencas, self.assiduidades))
    
    def porcentagem_assiduidade(self):
        if (self.total_presencas() != 0):
            return (self.total_presencas() / float(self.total_presencas() + self.total_faltas())) * 100
        else:
            return None

    def total_gastos(self):
        return sum(map(lambda x : x.valor, self.gastos))
    
    def total_gastos_str(self):
        return locale.currency( self.total_gastos(), grouping=True )

    def __repr__(self):
        return "Deputado %d:%s" % (self.id, self.nome.encode('utf-8'))

class Assiduidade(Base):
    __tablename__ = 'assiduidade'

    id_deputado = Column(Integer, ForeignKey('deputado.id'), primary_key = True)
    data = Column(Date, primary_key=True)
    presencas = Column(Integer)
    faltas = Column(Integer)

    def __init__(self, id_deputado, data, presencas, faltas):
        self.id_deputado = id_deputado
        self.data = data
        self.presencas = presencas
        self.faltas = faltas
    
    def porcentagem(self):
        if (self.presencas != 0):
            return (self.presencas / float(self.presencas + self.faltas)) * 100
        else:
            return None

    def __repr__(self):
        return "Em %s, o deputado %d faltou %d vezes e compareceu %d vezes" % (self.data, self.id_deputado, self.faltas, self.presencas)

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    id_deputado = Column(Integer, ForeignKey('deputado.id'))
    ano = Column(Numeric)
    descricao = Column(String(200))
    categoria = Column(String(80))
    valor = Column(Numeric(12, 2))

    def __init__(self, id_deputado, ano, descricao, categoria, valor):
        self.id_deputado = id_deputado
        self.ano = ano
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor

    def valor_str(self):
        return locale.currency( self.valor, grouping=True )

    def __repr__(self):
        return 'Na categoria %s o deputado %d gastou R$%.2f em %s' % (self.categoria, self.id_deputado, self.valor, self.ano)

if __name__ == '__main__':
    some_engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(some_engine) 

    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()

    # work with sess
    dep = Deputado('a', 'b', 'c')

    assiduidade = Assiduidade(0, datetime.date(2011, 1, 1), 10, 20)

    gasto = Gasto(0, 2011, 'Passeio com a familia', 'Viagem', 1500.45)

    session.add(dep)
    session.commit()

    assiduidade.id_deputado = dep.id
    session.add(assiduidade)
    session.commit()

    gasto.id_deputado = dep.id
    session.add(gasto)
    session.commit()

    print session.query(Deputado).all()
    print session.query(Assiduidade).all()
    print session.query(Gasto).all()
