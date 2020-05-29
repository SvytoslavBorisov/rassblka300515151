import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    members = sqlalchemy.Column(sqlalchemy.String, unique=True)
    admin = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)