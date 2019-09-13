from flask import Flask, render_template, request, url_for, redirect, flash
import pandas as pd
import pickle
from forms import StatSearch


app = Flask(__name__)

app.config['SECRET_KEY'] = "\xdek\x10m\xcba\xf9\x84\xdd\x8a\x9e^\xae\x0eS\xdak\xff\x00\xd1',b4\x9ebB\xc2*a\xf17"


# Load up model
def ValuePredictor(point_list,ast_list,reb_list):

# Loading Pickle files of the 3 models
    point_model = pickle.load(open('points.pkl','rb'))
    rebound_model = pickle.load(open('rebound.pkl', 'rb'))
    assist_model  = pickle.load(open('assist.pkl', 'rb'))

    points = point_model.predict(point_list)
    ast = assist_model.predict(ast_list)
    reb = rebound_model.predict(reb_list)

    return [points[0],ast[0],reb[0]]


@app.route('/', methods=['GET','POST'])
def index():
    form = StatSearch(request.form)
    if form.validate_on_submit():
        return redirect(url_for('result',player=form.player_search.data,team=form.team_search.data))
    return render_template('index.html', form=form)


@app.route('/result')
def result():
    player = request.args.get('player')
    team = request.args.get('team')

    # Getting Point Data
    point_data = pd.read_csv("data/point_input.csv")

# CHecking for Valid Input
    if player not in point_data['Player'].values:
        flash(f'Not a Valid Player','failure')
        return redirect(url_for('index'))

    if team not in point_data['Opp'].values:
        flash(f'Not a Valid Team', 'failure')
        return redirect(url_for('index'))

    point_data = point_data[(point_data['Player'] == player) & (point_data['Opp'] == team)]
    point_data = point_data.drop(['Player', 'Date2', 'Opp'], axis=1)

    # Getting Assist Data
    ast_data = pd.read_csv("data/ast_input.csv")
    ast_data = ast_data[(ast_data['Player'] == player) & (ast_data['Opp'] == team)]
    ast_data = ast_data.drop(['Player','Date2', 'Opp'], axis=1)

    # Getting Rebound Data
    reb_data = pd.read_csv("data/rebound_input.csv")
    reb_data = reb_data[(reb_data['Player'] == player) & (reb_data['Opp'] == team)]
    reb_data = reb_data.drop(['Player', 'Date2', 'Opp'], axis=1)

    prediction = ValuePredictor(point_data,ast_data,reb_data)

    return render_template("result.html",prediction=prediction)



if __name__ == '__main__':
    app.run(debug=True)

