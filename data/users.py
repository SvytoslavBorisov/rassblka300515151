import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Emails(SqlAlchemyBase, UserMixin):
    __tablename__ = 'emails'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    email = sqlalchemy.Column(sqlalchemy.String)
