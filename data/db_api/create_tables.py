from loader import Session, engine
from sqlalchemy import Column, Integer, String, ForeignKey, orm
import sqlalchemy.ext.declarative as dec


Base = dec.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    containers = orm.relation('Containers', back_populates='user')


class Containers(Base):
    __tablename__ = 'containers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = orm.relation('User')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # user = User()
    # user.name = 'Daniil'
    # user.email = 'daniil.shtompel@gmail.com'
    # Session.add(user)
    # Session.commit()

