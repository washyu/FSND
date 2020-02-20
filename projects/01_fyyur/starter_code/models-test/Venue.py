from flask_sqlalchemy import SQLAlchemy
from models.Genre import venue_genre, Genre, genres_to_string, string_to_genres
from models.Show import Show
from collections import defaultdict
from datetime import datetime

db = SQLAlchemy()

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
  
        data = []
        for venue in venues:
            d = {}
            d['id'] = venue.id
            d['name'] = venue.name
            d['num_upcoming_shows'] = sum(1 for i in venue.shows if not i.passed_show)
            data.append(d)

        response={
            "count": len(venues),
            "data": data
        }

        return response

    def get_venue_list():
        venues = db.session.query(Venue).all()

        citys = defaultdict(list)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
        # Grouping venues by cities
        for venue in venues:
            city = {}
            city['id'] = venue.id
            city['name'] = venue.name
            city['num_upcoming_shows'] = sum(1 for i in venue.shows if i.start_time > current_time)

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
        current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
        venue = Venue.query.filter_by(id=venue_id).first()
        p_shows  = [show for show in venue.shows if Show.start_time < current_time]
        up_shows = [show for show in venue.shows if Show.start_time > current_time]

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