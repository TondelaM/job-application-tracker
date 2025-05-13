from sqlalchemy import create_engine, Column, Integer, String, Date, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

Base = declarative_base()

class Statut(enum.Enum):
    EN_ATTENTE = "En attente"
    POSITIF    = "Positif"
    NEGATIF    = "Négatif"

class TypePoste(enum.Enum):
    PRESENTIEL = "Présentiel"
    HYBRIDE    = "Hybride"
    A_DISTANCE = "À distance"

class Candidature(Base):
    __tablename__ = "candidatures"

    id                  = Column(Integer, primary_key=True)
    date_candidature    = Column(Date, nullable=False)
    nom_contact         = Column(String, nullable=True)
    titre_poste         = Column(String, nullable=True)
    lieu                = Column(String, nullable=True)
    type_poste          = Column(Enum(TypePoste), default=TypePoste.PRESENTIEL)
    heures_semaine      = Column(Float, nullable=True)
    url                 = Column(String, nullable=True)
    salaire             = Column(Float, nullable=True)
    plateforme          = Column(String, nullable=True)
    description_poste   = Column(String, nullable=True)
    entreprise          = Column(String, nullable=False)
    lien                = Column(String)
    moyen               = Column(String)
    statut              = Column(Enum(Statut), default=Statut.EN_ATTENTE)
    date_entretien      = Column(Date, nullable=True)
    retour_entretien    = Column(String, nullable=True)
    notes               = Column(String, nullable=True)
    date_prise_poste    = Column(Date, nullable=True)

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    @classmethod
    def query_all(cls, session):
        return session.query(cls).order_by(cls.date_candidature).all()

engine  = create_engine("sqlite:///candidatures.db")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)