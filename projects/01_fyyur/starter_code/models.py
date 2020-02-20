
from collections import defaultdict
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

venue_genre = db.Table('venue_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
)

artist_genre = db.Table('artist_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
)

#  Artists
#  ----------------------------------------------------------------

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
        artist.seeking_venue = form_data['seeking_venue']
        artist.seeking_description = form_data['seeking_description']
        artist.website = form_data['website']

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
        artist.seeking_venue = form_data['seeking_venue']
        artist.seeking_description = form_data['seeking_description']
        artist.website = form_data['website']

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
        
        p_shows = []
        up_shows = []

        # Looping over the shows to find the past shows.  I would have rather used the date to figure the past show but
        # wanted to display the same state of the site from the example code. 
        for show in artist.shows:
            venue = show.Venues_shows
            temp = show.__dict__
            temp['venue_id'] = venue.id
            temp['venue_name'] = venue.name
            temp['venue_image_link'] = venue.image_link
            # Format the string to the example format had to trim some of the microsecond percision hense the -5 from the end of the string.
            temp_time = show.start_time
            if datetime.strptime(show.start_time, '%Y-%m-%d %H:%S:%M') < current_time:
                p_shows.append(temp)
            else:
                up_shows.append(temp)

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
        current_time = datetime.now()
        data = []
        for artist in artists:
            d = {}
            d['id'] = artist.id
            d['name'] = artist.name
            d['num_upcoming_shows'] = sum(1 for show in artist.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%S:%M') > current_time)
            data.append(d)

        response={
            "count": len(artists),
            "data": data
        }

        return response


#  Genre
#  ----------------------------------------------------------------
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


#  Show
#  ----------------------------------------------------------------
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)

    def create_show(form_data):
        show = Show()
        show.artist_id = form_data['artist_id']
        show.venue_id = form_data['venue_id']
        show.start_time = form_data['start_time']

        try:
            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            return 'Show was successfully listed!'
        except Exception as e:
            return 'An error occurred. Show could not be listed.'
            db.session.rollback()
        finally:
            db.session.close()

    def get_show_list():
        shows = db.session.query(Show.start_time.label('start_time'),
        Venue.id.label('venue_id'),
        Venue.name.label('venue_name'),
        Artist.id.label('artist_id'),
        Artist.name.label('artist_name'),
        Artist.image_link.label('artist_image_link'))\
        .join(Artist, Venue).all()

        data = []
        for show in shows:
            temp={
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time
            }
            data.append(temp)

        return data


#  Venue
#  ----------------------------------------------------------------
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venues_shows', lazy=True)
    genres = db.relationship('Genre', secondary=venue_genre, backref=db.backref('Venue_genres', lazy=True)) 

    def delete_venue(venue_id):
        try:
            db.session.query(Venue).filter(Venue.id == venue_id).delete(False)
            db.session.commit()
            return 'Venue was successfully deleted!'
        except Exception as e:
            db.session.rollback()
            return 'Unable to delete Venue!'
        finally:
            db.session.close()

    def update_venue(venue_id, form_data):
        venue = Venue.query.filter_by(id=venue_id).first()
        
        venue.genres = string_to_genres(form_data['genres'])
        venue.address = form_data['address']
        venue.name = form_data['name']
        venue.city = form_data['city']
        venue.state = form_data['state']
        venue.phone = form_data['phone']
        venue.facebook_link = form_data['facebook_link']
        venue.image_link = form_data['image_link']
        venue.website = form_data['website']
        venue.seeking_talent = form_data['seeking_talent']
        venue.seeking_description = form_data['seeking_description']

        try:
            db.session.commit()
            return f'Venue {form_data["name"]} was successfully updated!'
        except Exception as e:
            db.session.rollback()
            return f'An error occurred! Venue {form_data["name"]} could not be updated.'
        finally:
            db.session.close()   


    def create_venue(form_data):
        venue = Venue()

        venue.genres = string_to_genres(form_data['genres'])
        venue.address = form_data['address']
        venue.name = form_data['name']
        venue.city = form_data['city']
        venue.state = form_data['state']
        venue.phone = form_data['phone']
        venue.facebook_link = form_data['facebook_link']
        venue.image_link = form_data['image_link']
        venue.website = form_data['website']
        venue.seeking_talent = form_data['seeking_talent']
        venue.seeking_description = form_data['seeking_description']

        try:
            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            return f'Venue {form_data["name"]} was successfully listed!'
        except Exception as e:
            db.session.rollback()
            return f'An error occurred! Venue {form_data["name"]} could not be listed.'
        finally:
            db.session.close()

    def search_venues_by_name(search_term):
        venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')

        data = []
        for venue in venues:
            d = {}
            d['id'] = venue.id
            d['name'] = venue.name
            d['num_upcoming_shows'] = sum(1 for i in venue.shows if i.start_time > current_time)
            data.append(d)

        response={
            "count": len(venues),
            "data": data
        }

        return response

    def get_venue_list():
        venues = db.session.query(Venue).all()

        citys = defaultdict(list)
        current_time = datetime.now()
        # Grouping venues by cities
        for venue in venues:
            city = {}
            city['id'] = venue.id
            city['name'] = venue.name
            city['num_upcoming_shows'] = sum(1 for show in venue.shows if datetime.strptime(show.start_time, '%Y-%m-%d %H:%S:%M') > current_time)

            citys[f"{venue.city},{venue.state}"].append(city)

        #creating required data format for venues page.
        data = []
        for city_state, venues in citys.items():
            temp = {}
            temp['city'], temp['state'] = city_state.split(',')
            temp['venues'] = venues
            data.append(temp)
        
        return data

    def get_venue(venue_id):
        #returns a venue with the givin id.
        current_time = datetime.now()
        venue = Venue.query.filter_by(id=venue_id).first()

        p_shows = []
        up_shows = []

        for show in venue.shows:
            artist = show.Artists
            temp = show.__dict__
            temp['artist_id'] = artist.id
            temp['artist_name'] = artist.name
            temp['artist_image_link'] = artist.image_link
            temp_time = show.start_time
            if datetime.strptime(show.start_time, '%Y-%m-%d %H:%S:%M') < current_time:
                p_shows.append(temp)
            else:
                up_shows.append(temp)

        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": genres_to_string(venue.genres),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": p_shows,
            "upcoming_shows": up_shows,
            "past_shows_count": len(p_shows),
            "upcoming_shows_count": len(up_shows),
        }
        return data