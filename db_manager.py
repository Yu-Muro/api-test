import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20))
    password = Column(String(20))
    nickname = Column(String(30))
    comment = Column(String(100))


#PostgreSQLとの接続用
db_uri = os.environ['DATABASE_URL']
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
engine = create_engine(db_uri)
session_factory = sessionmaker(bind=engine)
session = session_factory()

Base.metadata.create_all(bind=engine)

def add_default_user():
    default_user = User(
        user_id = "TaroYamada",
        password = "PaSSwd4TY",
        nickname = "たろー",
        comment = "僕は元気です"
    )
    session.add(default_user)
    session.commit()
    session.close()

def add_new_user(user_id, password, nickname, comment=""):
    if nickname == "":
        nickname = user_id
    new_user = User(
        user_id = user_id,
        password = password,
        nickname = nickname,
        comment = comment
    )
    session.add(new_user)
    session.commit()
    session.close()
    return None


def is_exist(user_id, password):
    result = session.query(User.user_id, User.nickname).filter(User.user_id == user_id, User.password == password).all()
    session.close()
    if result == []:
        return False
    else:
        return True

def get_user(user_id):
    result = session.query(User.user_id, User.nickname, User.comment).filter(User.user_id == user_id).all()
    session.close()
    return result

if __name__ == "__main__":
    add_default_user()
