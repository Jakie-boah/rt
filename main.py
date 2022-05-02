from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///My_movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()

all_movies = []

class NewMovie(FlaskForm):
    movie_title = StringField('Title', validators=[DataRequired()])
    release = StringField('Release date', validators=[DataRequired()])
    movie_description = StringField('Description', validators=[DataRequired()])
    movie_rating = StringField('How would you rate it?', validators=[DataRequired()])
    movie_ranking = StringField('Position, which should it take in the list', validators=[DataRequired()])
    movie_review = StringField('Your opinion on that movie', validators=[DataRequired()])
    movie_img_url = StringField('Img_URL', validators=[DataRequired()])
    submit = SubmitField('Add')

class EditInfo(FlaskForm):
    new_title = StringField('Change title', validators=[DataRequired()])
    new_release = StringField('Change release date', validators=[DataRequired()])
    new_movie_description = StringField('Change description', validators=[DataRequired()])
    new_movie_rating = StringField('How would you rate it?', validators=[DataRequired()])
    new_movie_review = StringField('Your opinion on that movie', validators=[DataRequired()])
    new_movie_img_url = StringField('Img_URL', validators=[DataRequired()])
    submit = SubmitField('Add')




@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()

    return render_template("index.html", all_movies=all_movies)


@app.route('/add', methods=['POST', 'GET'])
def add_movie():
    form = NewMovie()
    if request.method == "POST":
        new_movie = Movie(
            title=request.form['movie_title'],
            year=request.form['release'],
            description=request.form['movie_description'],
            rating=request.form['movie_rating'],
            ranking=request.form['movie_ranking'],
            review=request.form['movie_review'],
            img_url=request.form['movie_img_url'],
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route('/update_info/<int:id>', methods=['POST', 'GET'])
def edit_movie(id):
    all_movies = db.session.query(Movie).all()
    form = EditInfo()
    if request.method == "POST":
        movie_id = id
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.title = request.form['new_title']
        movie_to_update.release = request.form['new_release']
        movie_to_update.description = request.form['new_movie_description']
        movie_to_update.rating = request.form['new_movie_rating']
        movie_to_update.review = request.form['new_movie_review']
        movie_to_update.img_url = request.form['new_movie_img_url']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, id=id, all_movies=all_movies)

@app.route('/delete/<int:id>')
def delete(id):
    movie_id = id
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))






if __name__ == '__main__':
    app.run(debug=True)
