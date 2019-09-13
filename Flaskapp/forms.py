from wtforms import StringField
from flask_wtf import FlaskForm

# Player Search Form
class StatSearch(FlaskForm):
    player_search = StringField('Player:')
    team_search = StringField('Team:')
