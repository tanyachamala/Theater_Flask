from flask import json
from . import db
import flask_login
import enum

# User Roles
class UserRole(enum.Enum):
    customer = 1
    manager = 2

# ------------------- Models -------------------

class User(flask_login.UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    # Relationship: one user has many reservations
    booked = db.relationship('Reservation', backref='user', lazy=True)


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    director = db.Column(db.String(60), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    main_cast = db.Column(db.String(512), nullable=False)
    synopsis = db.Column(db.String(512), nullable=False)
    img = db.Column(db.String(512))  # path to image

    # Relationship: one movie has many projections
    projected = db.relationship('Projection', backref='movie', lazy=True)


class Screen(db.Model):
    __tablename__ = "screen"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    num_total_seats = db.Column(db.Integer, nullable=False)

    # Relationship: one screen has many projections
    projected = db.relationship('Projection', backref='screen', lazy=True)


class Projection(db.Model):
    __tablename__ = "projection"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=False)

    # Relationship: one projection has many reservations
    movie_booked = db.relationship('Reservation', backref='projection', lazy=True)


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    projection_id = db.Column(db.Integer, db.ForeignKey('projection.id'), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime(), nullable=False)
