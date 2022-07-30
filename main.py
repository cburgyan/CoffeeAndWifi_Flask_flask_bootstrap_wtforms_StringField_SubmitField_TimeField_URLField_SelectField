import wtforms
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = TimeField('Open Time e.g. 8AM', validators=[DataRequired()])
    close_time = TimeField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi_strength = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    available_power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        print(form.open_time.data)

        #Converting 24 hour into 12 hour
        open_time = datetime.datetime.strptime(str(form.open_time.data), "%H:%M:%S")
        open_time = open_time.strftime("%I:%M%p")
        close_time = datetime.datetime.strptime(str(form.close_time.data), "%H:%M:%S")
        close_time = close_time.strftime("%I:%M%p")
        if open_time[0] == '0':
            open_time = open_time[1:]
        if close_time[0] == '0':
            close_time = close_time[1:]

        #Save to file
        with open('cafe-data.csv', 'a', encoding='utf8') as csv_file:
            csv_file.write(f'{form.cafe.data},{form.location.data},{open_time},{close_time},{form.coffee_rating.data},{form.wifi_strength.data},{form.available_power.data}\n')
        return redirect(url_for('cafes'))

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
            print(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
