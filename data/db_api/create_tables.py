from loader import Session, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, orm
import sqlalchemy.ext.declarative as dec


Base = dec.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer)
    name = Column(String)
    email = Column(String)
    containers = orm.relation('Containers', back_populates='user')


class TrialAccess(Base):
    __tablename__ = 'trial'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer)
    is_trial = Column(Boolean)


class Containers(Base):
    __tablename__ = 'containers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id_user"))
    user = orm.relation('User')
