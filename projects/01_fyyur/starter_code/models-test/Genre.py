from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

def genres_to_string(obj_genres):
    return [ sub.name for sub in obj_genres ]


def string_to_genres(str_genres):
    genres = []
    for genre in str_genres:
        o_genre = Genre.query.filter_by(name=genre).first()
        genres.append(o_genre)
    return genres

venue_genre = db.Table('venue_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
)

artist_genre = db.Table('artist_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
)