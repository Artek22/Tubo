from sqlalchemy import BigInteger, Column, String, Date
from sqlalchemy.orm import declarative_base

from db.engine import engine

DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column("user_id", BigInteger, nullable=False, primary_key=True)
    name = Column(String(50), nullable=False)
    oracle_date_save = Column(Date, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


def create_db():
    # Метод создания таблиц бд по коду сверху
    DeclarativeBase.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
