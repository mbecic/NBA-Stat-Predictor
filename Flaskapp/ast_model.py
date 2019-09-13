import pandas as pd
import numpy as np
import datetime as dt
import xgboost as xgb
import pickle

''' Here I'm Preparing The Assist Model Data. It is Identical to the code in the Jupyter Notebook for the assist model except for
    I keep the Player, Date and Opponent information in order to save it to a csv containing the features for the model. 
    From this csv we will pass the features to the model to see the predicted amount of assists of the player in the game '''
np.random.seed(123)
data = pd.read_csv("data/Pts Ast Reb 2.csv")

#Filtering out players who played less than 10 career games
data = data.groupby('Player_(POI_Game_Stats)').filter(lambda x: len(x) > 10)

# Dropping Rebounds and Points Since they are not needed to predict points
data = data.drop(['PTS','TRB'], axis=1)

# Keeping only year age of players and dropping number of days
def year_age(row,column):
    year = int(row[column][0:2])
    return year

data['Age_(POI_Game_Stats)'] = data.apply(year_age,args=('Age_(POI_Game_Stats)',), axis=1)
data['Age_(DOI_Game_Stats)'] = data.apply(year_age,args=('Age_(DOI_Game_Stats)',), axis=1)
# Converting Date columne to Datetime type
data['Date'] = pd.to_datetime(data['Date'])
# sorting in descending order of dates, so when i get the rolling mean in the next code block, it's for the past X games
data = data.sort_values('Date')

# Getting Trend for average number of points in the past i games
def past_X_games(i,df):
    group = df.groupby('Player_(POI_Game_Stats)')['AST'].apply(lambda x: x.shift().rolling(i).mean()).reset_index()
    column_name = "AST_{}".format(i)
    thing = group.set_index('index').rename(columns={"AST":column_name})
    return thing

# Calculating Average points in past 3,5,7 and 10 games
moving_days = [3,5,7,10]

for i in moving_days:
    window_av = past_X_games(i,data)
    data = data.join(window_av,how='left')

data['Date2'] = data['Date']

# Keeping only month of date
data['Date'] = data['Date'].dt.strftime('%b')

# Keeping only the year the season began
def season(row):
    return int(row['Season'][0:4])

data['Season'] = data.apply(season,axis=1)

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import VarianceThreshold

le = LabelEncoder()
# Creating binary variables for Position and Home/Away since they both ony have 2 options
data['Pos'] = le.fit_transform(data['Pos'])
data['Home/Away'] = le.fit_transform(data['Home/Away'])

# Creating dummy variables for categorical data, ie the month of the game played
data = data.drop(['Tm_(POI_Game_Stats)','Player_(DOI_Game_Stats)', 'Season'], axis=1)
dummy = pd.get_dummies(data['Date'])
data = data.drop('Date',axis=1)
data = data.join(dummy, how='left')


# Filter out features that have limited correlation to the Assists  in a game
for i in data.columns.values:
    # Skip the player, date and the opponent since correlation would fail, these are used for the csv
    # from which we will query the data
    if i =='Player_(POI_Game_Stats)' or i=='Date2' or i=='Opp':
        continue
    cor = abs(data['AST'].corr(data[i]))
    if cor > 0.1:
        continue
    else:
        del data[i]

# 3 data frame containing player, opponent and date data
names, dates, Opp_Team = data['Player_(POI_Game_Stats)'], data['Date2'],data['Opp']

# Training data for mode
X = data.drop(['AST','Player_(POI_Game_Stats)', 'Date2', 'Opp'],axis=1)
y = data['AST']

sel = VarianceThreshold()
vt = sel.fit(X)
X = X.iloc[:, vt.variances_ > 0.16]

# Readding data that will will query csv by
X['Player'] = names
X['Date2'] = dates
X['Opp'] = Opp_Team

Ast_Input = X

# Sorting dataframe by Player, Team and Date to get it in descending date order
Ast_Input = Ast_Input.sort_values(by=['Player', 'Opp','Date2'])
# keep only the most recent features for each player and drop the rest
Ast_Input = Ast_Input.drop_duplicates(subset=['Player','Opp'], keep='last')
Ast_Input.to_csv('data/ast_input.csv',index=False)

from sklearn.model_selection import train_test_split

X = X.drop(['Player','Date2', 'Opp'], axis=1)

# Training Final Assist model
X_train,X_test ,y_train,y_test = train_test_split(X,y,test_size=0.3,train_size=0.7)
# Hyperparameters were selected in the Jupyter Notebook for the assist model
best_reb_model = xgb.XGBRegressor(n_estimators=250,learning_rate=0.05,max_depth=3,min_child_weight=5)
best_reb_model.fit(X_train,y_train)

# Dumping assist model into pickle file
pickle.dump(best_reb_model, open('assist.pkl','wb'))
