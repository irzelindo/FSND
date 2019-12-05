""" This is the base folder for Udacity the Fyyr project app """
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import babel
import dateutil.parser
from flask import \
    Flask, \
    render_template, \
    request, flash, \
    redirect, \
    url_for, \
    jsonify, \
    abort
from flask_moment import Moment
from forms import *
from models import *
from flask_cors import CORS
from datetime import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# app.config.from_object('config')
# setup_db(app)
# db = SQLAlchemy(app)

# @@TODO: connect to a local postgresql database
# Done in config.py file
# s = datetime.strftime(show.start_time, "%Y-%m-%d %H:%M")
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

# @TODO Implement Show and Artist models,
# and complete all model relationships and properties,
# as a database migration.
# Done in models.py file

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
CURRENT_DATE = datetime.now()


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):
    """ create and configure the app """
    app = Flask(__name__)
    setup_db(app)
    moment = Moment(app)
    CORS(app)
    app.jinja_env.filters['datetime'] = format_datetime

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # @TODO: Define ERROR handlers functions

    @app.errorhandler(404)
    def not_found(error):
        """ Returns 404 not found Error """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        """ Returns 400 Bad Request Error """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """ Returns 422 Unprocessable Request Error """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422

    #  Venues
    @app.route('/')
    def index():
        return render_template('pages/home.html')

    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        # @TODO: replace with real venues data.
        #   num_shows should be aggregated based on number of upcoming shows per venue.
        # Gathering data from database
        try:
            cities = City.query.all()
            data = [{"city": city.name,
                     "state": city.states.name,
                     "venues": [{"id": venue.id,
                                 "name": venue.name,
                                 "num_upcoming_shows":
                                     len([show for show in venue.shows
                                          if show.start_time > CURRENT_DATE])
                                 }
                                for venue in city.venues]
                     } for city in cities]

            return render_template('pages/venues.html', areas=data)
        except None:
            abort(404)

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        # @TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        try:
            venue_hint = "%{}%".format(request.form.get("search_term"))
            search_result = Venue.query.filter(Venue.name.ilike(venue_hint)).all()
            # print(search_result[0])
            data = [{"id": venue.id,
                     "name": venue.name} for venue in search_result]
            # Returning the response object
            response = {
                "data": data,
                "count": len(search_result)
            }
            return render_template('pages/search_venues.html', results=response,
                                   search_term=request.form.get('search_term', ''))
        except None:
            abort(404)

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # @TODO: replace with real venue data from the venues table, using venue_id
        try:
            venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
            # print(artist.shows)
            genres = [genre.name for genre in venue.genres]
            shows = [show for show in venue.shows]
            past_shows = [{"artist_id": show.artist_id,
                           "artist_name": show.artists.name,
                           "artist_image_link": show.artists.image_link,
                           "start_time": format_datetime(str(show.start_time), format="full")
                           } for show in shows
                          if show.start_time < CURRENT_DATE]
            upcoming_shows = [{"artist_id": show.artist_id,
                               "artist_name": show.artists.name,
                               "artist_image_link": show.artists.image_link,
                               "start_time": format_datetime(str(show.start_time), format="full")
                               } for show in shows
                              if show.start_time > CURRENT_DATE]
            # print(genres)
            data = {"id": venue.id,
                    "name": venue.name,
                    "genres": genres,
                    "address": venue.venue_address[0].address,
                    "city": venue.cities[0].name,
                    "state": venue.cities[0].states.name,
                    "phone": venue.venue_address[0].phone,
                    "website": venue.website,
                    "facebook_link": venue.facebook_link,
                    "seeking_talent": venue.seeking_talent,
                    "seeking_description": venue.seeking_description,
                    "image_link": venue.image_link,
                    "past_shows": past_shows,
                    "upcoming_shows": upcoming_shows,
                    "past_shows_count": len(past_shows),
                    "upcoming_shows_count": len(upcoming_shows)
                    }

            return render_template('pages/show_venue.html', venue=data)
        except None:
            abort(404)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        # @TODO: insert form data as a new Venue record in the db, instead
        # Querying venues and all related models to make sure we are not inserting
        # records that already exist in our database.
        venues = Venue.query.all()
        cities = City.query.all()
        states = State.query.all()
        genres = Genre.query.all()

        try:
            if request.method == 'POST':
                # Gather all data from the front end forms
                form_genres = request.form.getlist('genres')
                form_name = request.form.get('name')
                form_city = request.form.get('city')
                form_state = request.form.get('state')
                form_address = request.form.get('address')
                form_phone = request.form.get('phone')
                form_facebook_link = request.form.get('facebook_link')

                if len(form_genres) > 5:
                    flash('Cannot select more than 5 genres')
                    return redirect(url_for('create_venue_form'))
                else:
                    # Check if the Venue is already present on the database
                    check_venue = [venue for venue in venues if form_name.lower() == venue.name.lower()]
                    check_city = [city for city in cities if form_city.lower() == city.name.lower()]
                    check_states = [state for state in states if form_state.lower() == state.name.lower()]
                    check_genres = [genre for genre in genres if genre.name.lower()
                                    in list(map(str.lower, form_genres))]
                    # print(check_states)

                    if check_venue:
                        # If venue already exists flash message to the client
                        # Else create new venue
                        flash('Venue ' + request.form['name'] + ' already exists!')
                    else:
                        venue = Venue(venue_id=None, name=form_name, image_link=None,
                                      facebook_link=form_facebook_link, website=None,
                                      seeking_talent=None, seeking_description=None)
                        venue.insert()
                        if check_city:
                            for city in check_city:
                                venue.cities.append(city)
                        else:
                            city = City
                            if check_states:
                                print(check_states)
                                for state in check_states:
                                    city = City(city_id=None, name=form_city, state_id=state.id)
                            else:
                                state = State(id=None, name=form_state)
                                state.insert()
                                state = State.query.filter(State.name.lower() == form_state.lower()).one_or_none()
                                city = City(city_id=None, name=form_city, state_id=state.id)
                            venue.cities.append(city)

                        if check_genres:
                            # The genres are already set up by default
                            # There is no need to create a new on
                            # The genres will be appended into the venue
                            for genre in check_genres:
                                venue.genres.append(genre)
                        # After all checks
                        # Update the early create venue
                        # No need to check for address because if the venue is new
                        # The address will also be new
                        address = Venue_Address(id=None, address=form_address, phone=form_phone)
                        venue.venue_address.append(address)
                        venue.update()
                        # @TODO: modify data to be the data object returned from db insertion

                        # on successful db insert, flash success
                        flash('Venue ' + venue.name + ' was successfully created!')
                    return render_template('pages/home.html')

            else:
                # @TODO: on unsuccessful db insert, flash an error instead.
                flash('An error occurred. Venue ' + request.form.get('name') + ' could not be created.')
                # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                return render_template('pages/home.html')
        except None:
            abort(422)

    @app.route('/venues/<venue_id>', methods=['POST'])
    def delete_venue(venue_id):
        # @TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
        # print("Hello")
        venue = Venue.query.filter(Venue.id == venue_id).one_or_none()

        if venue:
            venue.delete()
            flash('Venue ' + venue.name + ' was successfully deleted!')
            return redirect(url_for('venues'))
        else:
            flash('Venue ' + venue.name + ' does not exist!')
            return render_template('pages/home.html')
        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage

    #  Artists
    #  ----------------------------------------------------------------
    @app.route('/artists')
    def artists():
        # @TODO: replace with real data returned from querying the database
        try:
            artist_list = Artist.query.all()
            serialized_artist_list = [artist.serialize() for artist in artist_list]
            # print(serialized_artist_list)
            data = [{"id": row["id"], "name": row["name"]} for row in serialized_artist_list]
            return render_template('pages/artists.html', artists=data)
        except None:
            abort(404)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # @TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        # Getting current data so that can compare it to the shows start time
        try:
            artist_hint = "%{}%".format(request.form.get("search_term"))
            search_result = Artist.query.filter(Artist.name.ilike(artist_hint)).all()
            # Since we can get more than one artist we only get the
            # number of upcoming shows if we get one artist instead of
            # a list of artists
            # If the search_result has more than one artist
            # upcoming_shows list will still empty
            # Else if the result is only one artist
            # Then the upcoming_shows list shall be fulfilled with the shows
            # print(search_result[0])
            data = [{"id": artist.id,
                     "name": artist.name} for artist in search_result]
            # Returning the response object
            response = {
                "data": data,
                "count": len(search_result)
            }

            return render_template('pages/search_artists.html', results=response,
                                   search_term=request.form.get('search_term', ''))
        except None:
            abort(404)

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        # shows the artist page with the given artist_id
        # @TODO: replace with real artist data from the artists table, using artist_id
        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
            # print(artist.shows)
            if artist:
                genres = [genre.name for genre in artist.genres]
                shows = [show for show in artist.shows]
                past_shows = [{"venue_id": show.venue_id,
                               "venue_name": show.venues.name,
                               "venue_image_link": show.venues.image_link,
                               "start_time": format_datetime(str(show.start_time), format="full")
                               } for show in shows
                              if show.start_time < CURRENT_DATE]
                upcoming_shows = [{"venue_id": show.venue_id,
                                   "venue_name": show.venues.name,
                                   "venue_image_link": show.venues.image_link,
                                   "start_time": format_datetime(str(show.start_time), format="full")
                                   } for show in shows
                                  if show.start_time > CURRENT_DATE]
                # print(genres)
                data = {"id": artist.id,
                        "name": artist.name,
                        "genres": genres,
                        "city": artist.city,
                        "state": artist.state,
                        "phone": artist.phone,
                        "website": artist.website,
                        "facebook_link": artist.facebook_link,
                        "seeking_venue": artist.seeking_venue,
                        "seeking_description": artist.seeking_description,
                        "image_link": artist.image_link,
                        "past_shows": past_shows,
                        "upcoming_shows": upcoming_shows,
                        "past_shows_count": len(past_shows),
                        "upcoming_shows_count": len(upcoming_shows)
                        }

                return render_template('pages/show_artist.html', artist=data)
            else:
                flash('Artist with ID ' + artist_id + ' do not exist!')
                return render_template('pages/home.html')
        except None:
            abort(404)

    #  Update
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        form = ArtistForm()
        artist = {
            "id": 4,
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        }
        # @TODO: populate form with fields from artist with ID <artist_id>
        return render_template('forms/edit_artist.html', form=form, artist=artist)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # @TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_artist', artist_id=artist_id))

    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        form = VenueForm()
        venue = {
            "id": 1,
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom Street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }
        # @TODO: populate form with values from venue with ID <venue_id>
        return render_template('forms/edit_venue.html', form=form, venue=venue)

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        # @TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # @TODO: insert form data as a new Artist record in the db, instead
        # @TODO: modify data to be the data object returned from db insertion
        artists = Artist.query.all()
        genres = Genre.query.all()

        try:
            if request.method == 'POST':
                # Gather all data from the front end forms
                form_genres = request.form.getlist('genres')
                form_name = request.form.get('name')
                form_city = request.form.get('city')
                form_state = request.form.get('state')
                form_image = request.form.get('image_link')
                form_phone = request.form.get('phone')
                form_facebook_link = request.form.get('facebook_link')

                if len(form_genres) > 10:
                    flash('Cannot select more than 5 genres')
                    return redirect(url_for('create_artist_form'))
                else:
                    # Check if the Artist is already present on the database
                    check_artist = [artist for artist in artists if form_name.lower() == artist.name.lower()]
                    check_genres = [genre for genre in genres if genre.name.lower()
                                    in list(map(str.lower, form_genres))]
                    # print(check_states)

                    if check_artist:
                        # If Artist already exists flash message to the client
                        # Else create new venue
                        flash('Artist ' + form_name + ' already exists!')
                    else:
                        artist = Artist(artist_id=None, name=form_name, city=form_city,
                                        state=form_state, phone=form_phone,
                                        image_link=form_image, facebook_link=form_facebook_link,
                                        website=None, seeking_venue=None, seeking_description=None)
                        artist.insert()

                        if check_genres:
                            # The genres are already set up by default
                            # There is no need to create a new on
                            # The genres will be appended into the artist
                            for genre in check_genres:
                                artist.genres.append(genre)
                        # After all checks
                        artist.update()
                        # @TODO: modify data to be the data object returned from db insertion

                        # on successful db insert, flash success
                        flash('Artist ' + artist.name + ' was successfully created!')
                    return render_template('pages/home.html')

            else:
                # @TODO: on unsuccessful db insert, flash an error instead.
                flash('An error occurred. Venue ' + request.form.get('name') + ' could not be created.')
                # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                return render_template('pages/home.html')
        except None:
            abort(422)
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully created!')
        # @TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        # @TODO: replace with real venues data.
        #       num_shows should be aggregated based on number of upcoming shows per venue.
        shows = Show.query.all()

        data = [{"venue_id": shows[i].venue_id,
                 "venue_name": shows[i].venues.name,
                 "artist_id": shows[i].artist_id,
                 "artist_name": shows[i].artists.name,
                 "artist_image_link": shows[i].artists.image_link,
                 "ticket_price": shows[i].ticket_price,
                 "start_time": format_datetime(str(shows[i].start_time), format="full")} for i in range(len(shows))]

        return render_template('pages/shows.html', shows=data)

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # @TODO: insert form data as a new Show record in the db, instead
        try:
            if request.method == 'POST':
                artist_id = request.form.get('artist_id')
                venue_id = request.form.get('venue_id')
                start_time = request.form.get('start_time')
                ticket_price = request.form.get('ticket_price')
                #print(artist_id, venue_id, start_time, ticket_price)
                show = Show(show_id=None, artist_id=artist_id, venue_id=venue_id,
                            start_time=start_time, ticket_price=ticket_price)
                show.insert()
                # on successful db insert, flash success
                # @TODO: on successful db insert, flash an error instead.
                flash('Show was successfully created!')
                # e.g., flash('An error occurred. Show could not be listed.')
                # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                return redirect(url_for('shows'))
            else:
                # on successful db insert, flash success
                # @TODO: on unsuccessful db insert, flash an error instead.
                flash('Show was not created!')
                # e.g., flash('An error occurred. Show could not be listed.')
                # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                return redirect(url_for('create_shows'))

        except None:
            abort(401)

    return app
