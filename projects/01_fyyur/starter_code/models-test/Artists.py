from flask_sqlalchemy import SQLAlchemy
from models.Genre import artist_genre, Genre, genres_to_string, string_to_genres

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artists', lazy=True)
    genres = db.relationship('Genre', secondary=artist_genre, backref=db.backref('Artist', lazy=True))  

    def get_artists_list():
        return db.session.query(Artist.id, Artist.name).order_by(Artist.id).all()

    def update_artist(artist_id, form_data):
        artist = Artist.query.filter_by(id=artist_id).first()

        artist.genres = string_to_genres(form_data['genres'])
        artist.name = form_data['name']
        artist.city = form_data['city']
        artist.state = form_data['state']
        artist.phone = form_data['phone']
        artist.facebook_link = form_data['facebook_link']
        artist.image_link = form_data['image_link']

        try:
            db.session.commit()
            return f'Artist {form_data["name"]} was successfully updated!'
        except Exception as e:
            db.session.rollback()
            return f'An error occurred! Artist {form_data["name"]} could not be updated.'
        finally:
            db.session.close()   

    def create_artist(form_data):
        artist = Artist()

        artist.genres = string_to_genres(form_data['genres'])
        artist.name = form_data['name']
        artist.city = form_data['city']
        artist.state = form_data['state']
        artist.phone = form_data['phone']
        artist.facebook_link = form_data['facebook_link']
        artist.image_link = form_data['image_link']

        try:
            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            return f'Artist {form_data["name"]} was successfully listed!'
        except Exception as e:
            db.session.rollback()
            return f'An error occurred. Artist {form_data["name"]} could not be listed.'
        finally:
            db.session.close()
        

    def get_artist(artist_id):
        current_time = datetime.now()
        artist = Artist.query.filter_by(id=artist_id).first()
        # Get a list of the artist genre names 
        p_shows  = [show for show in venue.shows if show.start_time < current_time]
        up_shows = [show for show in venue.shows if show.start_time > current_time]


        # Filling out the dict manualy rather then using the __dict__ conversion since we probably don't want to push all the table info the 
        # client browser.
        data={
            "id": artist.id,
            "name": artist.name,
            "genres": genres_to_string(artist.genres),
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": p_shows,
            "upcoming_shows": up_shows,
            "past_shows_count": len(p_shows),
            "upcoming_shows_count": len(up_shows)
        }
        return data

    def search_artists_by_name(search_term):
        artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  
        data = []
        for artist in artists:
            d = {}
            d['id'] = artist.id
            d['name'] = artist.name
            d['num_upcoming_shows'] = sum(1 for i in artist.shows if not i.passed_show)
            data.append(d)

        response={
            "count": len(artists),
            "data": data
        }

        return response