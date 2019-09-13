from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def scrape(url_base, url_pages, write_file) :
    html = urlopen(url_base)
    soup = BeautifulSoup(html,"lxml")
    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
    stats = pd.DataFrame(player_stats, columns=headers)

    i = 1

    #Loop through All Pages until failure to open page, then append page to existing dataframe

    #to loop through every page, we tread url as a string and replace the last part of the string that identifies the page using the format method
    while html(url_pages.format(i)):
        url = url_pages.format(i)
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        soup.findAll('tr', limit=2)
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
        headers = headers[1:]
        rows = soup.findAll('tr')[1:]
        player_stats = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
        stats_temp = pd.DataFrame(player_stats, columns=headers)
        stats = stats.append(stats_temp)
        ++i

    stats.to_csv(write_file, index=False)

# Scraping for every players regular season game stats from 2014-15 season to 2018-19
scrape("https://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2015&year_max=2019&is_playoffs=N&age_min=0&age_max=99&season_start=1&season_end=-1&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=pts",
"https://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&player_id=&match=game&year_min=2015&year_max=2019&age_min=0&age_max=99&team_id=&opp_id=&season_start=1&season_end=-1&is_playoffs=N&draft_year=&round_id=&game_num_type=&game_num_min=&game_num_max=&game_month=&game_day=&game_location=&game_result=&is_starter=&is_active=&is_hof=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c1val_orig=&c2stat=&c2comp=&c2val=&c2val_orig=&c3stat=&c3comp=&c3val=&c3val_orig=&c4stat=&c4comp=&c4val=&c4val_orig=&is_dbl_dbl=&is_trp_dbl=&order_by=pts&order_by_asc=&offset={}",
       "Player Stat Lines 2014-2019.csv"
)

#Scraping every players advanced metrics average for each season

scrape("https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&per_minute_base=36&per_poss_base=100&type=advanced&season_start=1&season_end=-1&lg_id=NBA&age_min=0&age_max=99&is_playoffs=N&height_min=0&height_max=99&year_min=2015&year_max=2019&birth_country_is=Y&as_comp=gt&as_val=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=ws",
       "https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=advanced&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2015&year_max=2019&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=0&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=&c6stat=&order_by=ws&order_by_asc=&offset={}",
       "Player Advanced 2014-19.csv")

# Scraping every players ger game season averages
scrape("https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_game&per_minute_base=36&per_poss_base=100&season_start=1&season_end=-1&lg_id=NBA&age_min=0&age_max=99&is_playoffs=N&height_min=0&height_max=99&year_min=2015&year_max=2019&birth_country_is=Y&as_comp=gt&as_val=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=ws",
       "https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_game&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2015&year_max=2019&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=0&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=&c6stat=&order_by=ws&order_by_asc=&offset={}",
       "Player Per Game 2014-19.csv")

#scraping every teams advanced season metrics
scrape("https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=advanced&year_min=2015&year_max=2019&lg_id=NBA&order_by=wins",
       "https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=advanced&year_min=2015&year_max=2019&lg_id=NBA&franch_id=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=wins&order_by_asc=&offset={}",
       "Team Season Avg 2014-19.csv")
#scraping every teams per game season metrics
scrape("https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=team_per_game&year_min=2015&year_max=2019&lg_id=NBA&order_by=wins",
       "https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=team_per_game&year_min=2015&year_max=2019&lg_id=NBA&franch_id=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=wins&order_by_asc=&offset={}",
       "Team Season Avg 12-2019.csv")
#scraping every teams opponents per game season metrics
scrape("https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=opp_per_game&year_min=2015&year_max=2019&lg_id=NBA&order_by=wins",
"https://www.basketball-reference.com/play-index/tsl_finder.cgi?request=1&match=single&type=opp_per_game&year_min=2015&year_max=2019&lg_id=NBA&franch_id=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=wins&order_by_asc=&offset={}",
       "Team Opp Season Avg 2014-19.csv")