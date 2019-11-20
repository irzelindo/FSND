"""
  This file contains all the database connection definition,
  and all the CRUD for Fyyur web app.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import Config, SECRET_KEY
from flask_migrate import Migrate

DATABASE_PATH = Config.SQLALCHEMY_DATABASE_URI
SECRET_KEY = SECRET_KEY

db = SQLAlchemy()


def setup_db(app, secret_key=SECRET_KEY, database_path=DATABASE_PATH):
    """ Database setup """
    # print(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SECRET_KEY'] = secret_key
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    # No need to run db.create_all() as for now using flask migrations
    # library.
    # db.create_all()


# Implementing all necessary CRUD operations superclass
class crud_ops():

    def insert(self):
        """ Insert data """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Update data """
        db.session.commit()

    def delete(self):
        """ Delete data """
        db.session.delete(self)
        db.session.commit()


class Artist_Genre_Link(db.Model, crud_ops):
    __tablename__ = "artist_genre_link"

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), primary_key=True)
    likes = db.Column(db.Integer)
    deslikes = db.Column(db.Integer)


class Venue_Genre_Link(db.Model, crud_ops):
    __tablename__ = "venue_genre_link"

    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), primary_key=True)
    likes = db.Column(db.Integer)
    deslikes = db.Column(db.Integer)


class Venue_City_Link(db.Model, crud_ops):
    __tablename__ = "venue_city_link"

    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), primary_key=True)
    likes = db.Column(db.Integer)
    deslikes = db.Column(db.Integer)


class Genre(db.Model, crud_ops):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(250))
    artists = db.relationship("Artist", secondary="artist_genre_link")
    venues = db.relationship("Venue", secondary="venue_genre_link")

    def __init__(self, genre_id, name, description):
        self.id = genre_id
        self.name = name
        self.description = description

    def serialize(self):
        # Serialize genres table row data
        return {
            "genre_id": self.genre_id,
            "name": self.name,
            "description": self.description
        }


class Venue(db.Model, crud_ops):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", cascade="all, delete-orphan", back_populates="venues")
    venue_address = db.relationship("Venue_Address", cascade="all, delete", back_populates="venues")
    genres = db.relationship('Genre', secondary="venue_genre_link", back_populates='venues', lazy='joined', cascade="all, delete")
    cities = db.relationship('City', secondary="venue_city_link", back_populates='venues', lazy='joined', cascade="all, delete")

    def __init__(self, venue_id, name,
                 image_link=None, facebook_link=None, website=None, seeking_talent=None,
                 seeking_description=None):
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.name = name
        self.id = venue_id

    def serialize(self):
        """ Serialize venues table row data """
        return {
            "website": self.website,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "name": self.name,
            "id": self.id
        }


class Venue_Address(db.Model, crud_ops):
    __tablename__ = "venue_address"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250))
    phone = db.Column(db.String(120))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=True)
    venues = db.relationship("Venue", back_populates="venue_address")

    def __init__(self, id, address, phone):
        self.id = id
        self.address = address
        self.phone = phone

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "phone": self.phone,
        }


class State(db.Model, crud_ops):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    cities = db.relationship("City", cascade="all, delete-orphan")


    def __init__(self, id, name):
        self.id = id
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class City(db.Model, crud_ops):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=True)
    states = db.relationship("State", back_populates="cities")
    venues = db.relationship('Venue', secondary="venue_city_link")

    def __init__(self, city_id, name, state_id):
        self.id = city_id
        self.name = name
        self.state_id = state_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "state_id": self.state_id
        }


class Artist(db.Model, crud_ops):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    genres = db.relationship("Genre", secondary="artist_genre_link")
    shows = db.relationship("Show", cascade="all, delete-orphan", back_populates="artists")

    def __init__(self, artist_id, name, city, state, phone,
                 image_link, facebook_link, website, seeking_venue,
                 seeking_description):
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.city = city
        self.state = state
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.name = name
        self.id = artist_id

    def serialize(self):
        """ Serialize artists table row data """
        return {
            "website": self.website,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "state": self.state,
            "genres": self.genres,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "city": self.city,
            "name": self.name,
            "id": self.id
        }


class Show(db.Model, crud_ops):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.now())
    ticket_price = db.Column(db.String(15))

    venues = db.relationship("Venue", back_populates="shows")
    artists = db.relationship("Artist", back_populates="shows")

    def __init__(self, show_id, artist_id, venue_id, start_time, ticket_price):
        self.id = show_id
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time
        self.ticket_price = ticket_price

    def serialize(self):
        # Serialize Shows table row data
        return {
            "show_id": self.id,
            "venue_id": self.venue_id,
            "artist_id": self.artist_id,
            "start_time": self.start_time,
            "ticket_price": self.ticket_price
        }
