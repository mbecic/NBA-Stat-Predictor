import pandas as pd
import datetime as dt
import seaborn as sns

'''In this file we join all the web scraped csvs into one master csv that will be used for the modelling.
We will also filter out any immediately unnecessary features that I know wont be relavent to any model from
my expereince of watching basketball as well as any columns that are measuring the same thing (eg. Field Goal Attempts,
Filed Goal Percentage, Field Goals Made all indicate how good of a shooter a player is, but the best shooters generally
shoot the most, so we just keep Field Goals Attempted'''


# Player_Statline DF will contain the offensive player stats that we are trying to predict in the final model
player_statline = pd.read_csv("Player Stat Lines 2014-2019.csv")
# Defender_Statline DF will contain the players defender, ie the the opponent who should be guarding them, use these
# 2 players as key for joining on the other dataframes, since these df contain all game data from last 5 years
defender_statline = pd.read_csv("Player Stat Lines 2014-2019.csv")


# Basketball reference has players in one of 10 positions which makes many joins not possible since there might
#  not be a player of the same position on the opponents team, so we simplfy by having all players as guards or forwards
def keep_primary_position(row):
    temp_pos = row['Pos'][0]
    if temp_pos=='G' or temp_pos=='F':
        return temp_pos
    else:
        return 'F'

player_statline['POS'] = player_statline.apply(keep_primary_position(),axis=1)


# Retrieving all relavent game stats and columns we will be joining data on
player_stat_line = player_stat_line.loc[:,['Player','Age','Season','Tm','Pos','Date','Home/Away','Opp','PTS','AST','TRB','GS']]
defender_stat_line = defender_stat_line.loc[:,['Player','Age','Tm','Pos','Date','GS']]

#POI and DOI stand for Player and Defender of interest
complete_game_stats = player_statline.merge(defender_statline, how='left', \
                                              left_on=['Date','Opp','Pos','GS'],\
                                              right_on=['Date','Tm','Pos','GS'],suffixes=('_(POI_Game_Stats)','_(DOI_Game_Stats)'))

complete_game_stats['Date'] = pd.to_datetime(complete_game_stats['Date'])

# Calculating season for each game
def season(row):
    if (row['Date'] >= pd.Timestamp('2014-09-30')) and (row['Date'] <= pd.Timestamp('2015-07-01')):
        return '2014-15'
    elif (row['Date'] >= pd.Timestamp('2015-09-30')) and (row['Date'] <= pd.Timestamp('2016-07-01')):
        return '2015-16'
    elif (row['Date'] >= pd.Timestamp('2016-09-30')) and (row['Date'] <= pd.Timestamp('2017-07-01')):
        return '2016-17'
    elif (row['Date'] >= pd.Timestamp('2017-09-30')) and (row['Date'] <= pd.Timestamp('2018-07-01')):
        return '2017-18'
    else: return '2018-19'

complete_game_stats['Season'] = complete_game_stats.apply(season,axis=1)


#for easier joining with the other data sets
complete_game_stats = complete_game_stats.rename(columns={'GS': 'Game Started'})


# read in the players advanced stats for the season and only keep relavent features
player_advanced = pd.read_csv("Player Advanced 14-2019.csv")
off_player_advanced = player_advanced.loc[:,['Player','Season', 'PER', '3PAr','FTr','ORB%','DRB%' ,'TRB%','AST%','TOV%','USG%','OWS','ORtg','OBPM']]
def_player_advanced = player_advanced.loc[:,['Player','Season','TRB%','ORB%','DRB%','STL%','BLK%','DRtg','DWS','DBPM']]

# Join season advanced statistics of each player with individual game records
complete_game_stats = complete_game_stats.merge(off_player_advanced,\
                                                 how='left', left_on=['Player_(POI_Game_Stats)','Season'],\
                                                 right_on=['Player','Season'])

complete_game_stats = complete_game_stats.merge(def_player_advanced,\
                                                 how='left', left_on=['Player_(DOI_Game_Stats)','Season'],\
                                                 right_on=['Player','Season'],suffixes=('_(POI_Advanced_Season)','_(DOI_Advanced_Season)'))

# method of previous joins results in multiple joins as there can be multiple players on the opponents team that are
# playing the same position and defending the player of interest. So we only keep the defender with the best DWS (Defensive Win Shares) so we would
# assume the worst possible case
filtered = def_player_advanced.sort_values(by=['Date','Player_(POI_Game_Stats)','DWS'], ascending=False).drop_duplicates(['Date','Player_(POI_Game_Stats)'])

# Joining Offensive Player Per Game and Keeping only Relavent fields
per_game = pd.read_csv("/Users/Mihailo/Documents/Pythonprojects/NBA Stat Prediction/Player Per Game 14-2019.csv")
per_game = per_game.drop(['Age', 'Tm','Lg', 'G', 'GS','WS'], axis=1)

off_per_game = per_game.drop(['FG','2P','3P','FT','STL','BLK','PF','eFG%','TS%'], axis=1)

filtered_per_game = filtered.merge(off_per_game,how='left', left_on=['Player_(POI_Game_Stats)','Season'],\
                                   right_on=['Player','Season'], suffixes=('','_(POI_Per_Game)'))

# Reading in all team related data
team_advanced = pd.read_csv("Team Advanced Season 14-2019.csv")
team_opp = pd.read_csv("Team Opp Season Avg 14-2019.csv")
team_avg = pd.read_csv("/Team Season Avg 14-2019.csv")

# Fixing Team Column Formatting
def proper_team(row):
    if '*' in row['Tm']:
        return row['Tm'][0:3]
    else:
        return row['Tm']

team_advanced = team_advanced.drop_duplicates(subset=['Tm','Season'])
team_opp = team_opp.drop_duplicates(subset=['Tm','Season'])
team_avg = team_avg.drop_duplicates(subset=['Tm','Season'])

# Offensive and defensibe team advanced statistics
off_team_advanced = team_advanced.loc[:,['Season','Tm','MOV','Pace','ORtg', 'ORB%_Team','ORB%_Opp']]
def_team_advanced = team_advanced.loc[:,['Season','Tm','DRtg','eFG%_Opp','FT/FGA_Opp','ORB%_Team','ORB%_Opp']]

# Joining the advanced stats to the main df
player_with_team = filtered_per_game.merge(off_team_advanced,how='left', left_on=['Tm_(POI_Game_Stats)','Season'],\
                                           right_on=['Tm','Season'], suffixes=('','_(OT_Advanced)'))

player_with_team = player_with_team.merge(def_team_advanced,how='left', left_on=['Opp','Season'],\
                                           right_on=['Tm','Season'],suffixes=('_(OT_Advanced)','_(DT_Advanced)'))

# Joining the defensive teams opponenet average
def_team_opp = team_opp.drop(['Lg','G','W','L','W/L%','STL','BLK','PF','2P','3P','FT'], axis=1)

player_with_team = player_with_team.merge(def_team_opp,how='left', left_on=['Tm_(POI_Game_Stats)','Season'],\
                                           right_on=['Tm','Season'],suffixes=('','_(DT_Opp_Avg)'))

# Joining the player of interests team averages
off_team_avg = team_avg.drop(['Lg','G','W','L','W/L%','MP','STL','BLK','TOV','2P','3P','FT'], axis=1)

player_with_team = player_with_team.merge(off_team_avg,how='left', left_on=['Tm_(POI_Game_Stats)','Season'],\
                                           right_on=['Tm','Season'],suffixes=('','_(OT_Tm_Avg)'))

# Master File is Prepped, checking for any null values

player_with_team.isna().sum(axis=0).plot(kind='bar')

'''We see that all nulls arise from stats that would be 0. For instance Field Goals made is null since field goals
attempted is 0. So we can fill all nulls with 0.'''

player_with_team.fillna(0)

# Save as Master CSV

player_with_team.to_csv('Master.csv', index=False)


