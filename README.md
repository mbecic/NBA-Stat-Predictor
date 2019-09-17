# NBA-Stat-Predictor
Flask app that allows you to search for any NBA player and any NBA team and see the players predicted points, assists and rebounds vs. the opposing team. Rebounds and assists were predicted using Gradient Boosting Regresssion from the XGBoost library, while points were predicted using a simple linear regression from Scikit-learn. Neural Nets were also texted, but performed the worst out of the 3 different model types. All data was scraped from basketball reference using Beautiful Soup.

Search Page

![alt text](https://i.imgur.com/QczrUEY.png)

Results

![alt text](https://i.imgur.com/Kha05rT.png)
