from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap
import wtf


def calculate(initial, daily_roi, compound_duration, compound_frequency):
    current_initial = initial
    # 1440 minutes in a day
    minutes_in_a_day = 60 * 24
    minutely_roi = int(daily_roi) / minutes_in_a_day

    values = []

    for _ in range(compound_duration):
        roi_for_compound_frequency = int(compound_frequency) * minutely_roi
        daily_returns = 0
        for _ in range(int(minutes_in_a_day / compound_frequency)):
            returns = (roi_for_compound_frequency / 100) * current_initial
            current_initial += returns
            daily_returns += returns
        values.append((round(current_initial, 2), round(daily_returns, 2)))
        print(f'Daily returns is {daily_returns}')
        print(f'Current Initial is {current_initial}\n')
    return values


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "kelex"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        initial = int(request.form['initials'])
        daily_roi = int(request.form['daily_roi'])
        compound_duration = int(request.form['compound_duration'])
        compound_frequency = int(request.form['compound_frequency'])
        values = calculate(initial, daily_roi,
                           compound_duration, compound_frequency)
        return render_template("calculate.html", values=values)
    else:
        return render_template("calculate.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
