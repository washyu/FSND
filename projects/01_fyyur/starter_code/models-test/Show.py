from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
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
            temp_time = show.start_time.strftime("%Y-%m-%dT%H:%M:%S.0000Z")
            temp={
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": temp_time
            }
            data.append(temp)

        return data
