# NBA-Stat-Predictor
Flask app that allows you to search for any NBA player and any NBA team and see the players predicted points, assists and rebounds vs. the opposing team. Rebounds and assists were predicted using gradient boosted regression from the XGBoost library, while points were predicted using a simple linear regression from Scikit-learn. Neural Nets were also tested, but performed the worst out of the 3 different model types. All data was scraped from basketball reference using Beautiful Soup.

Disclaimer: Player with under 10 career games played were excluded since they did not have enough data to model.

Search Page

![alt text](https://i.imgur.com/QczrUEY.png)

Results

![alt text](https://i.imgur.com/Kha05rT.png)


Future Plans:
- Implement SQL database to store data and remove all csv files
- Automate Webscraping so data can be updated everyday
