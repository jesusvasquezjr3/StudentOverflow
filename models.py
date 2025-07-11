# --- 1. Importar 'db' desde el nuevo archivo 'extensions.py' ---
from extensions import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID, SMALLINT
import uuid

# El resto del archivo es exactamente igual
class Profile(db.Model, UserMixin):
    __tablename__ = 'profiles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    reputation = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    questions = db.relationship('Question', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)
    votes = db.relationship('Vote', backref='voter', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    best_answer_id = db.Column(db.BigInteger, db.ForeignKey('answers.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    answers = db.relationship('Answer', backref='question', lazy='dynamic', foreign_keys='Answer.question_id')
    tags = db.relationship('Tag', secondary='question_tags', backref=db.backref('questions', lazy='dynamic'))

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profiles.id'), nullable=False)
    question_id = db.Column(db.BigInteger, db.ForeignKey('questions.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    question_as_best = db.relationship('Question', backref='best_answer', uselist=False, foreign_keys=[Question.best_answer_id])

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

question_tags = db.Table('question_tags', db.Model.metadata,
    db.Column('question_id', db.BigInteger, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profiles.id'), nullable=False)
    question_id = db.Column(db.BigInteger, db.ForeignKey('questions.id'), nullable=True)
    answer_id = db.Column(db.BigInteger, db.ForeignKey('answers.id'), nullable=True)
    vote_type = db.Column(SMALLINT, nullable=False)
