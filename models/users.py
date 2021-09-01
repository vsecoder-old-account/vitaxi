import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    ref = sa.Column(sa.String, nullable=True)
    refs = sa.Column(sa.String, autoincrement=True)
    score = sa.Column(sa.String, autoincrement=True)
    test = sa.Column(sa.String, autoincrement=True)
