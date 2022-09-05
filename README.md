# NFL Fantasy Football AI Assistant

<p align="center">
<img src="https://user-images.githubusercontent.com/101227638/187763276-cece406f-0808-48cc-a861-8d94bf1ad3ed.png" />
</p>  

<p align="center">
<img src="https://user-images.githubusercontent.com/101227638/187761595-659835db-2994-48fb-b2d0-8246b14088f9.png" />
</p>                                                                                                               

**Introduction:** 

NFL fantasy football is a game in which football league managers and fans alike take on the role of the coach or general manager of a pro football team that they draft. Participants draft their initial teams, select players to play each week and trade players in order to compete weekly during a season against other teams. The winning teams are determined by the real-life statistics of the pro athletes. A team consists of 9 starters in 7 positions. The 7 positions are quarterback (QB), running back (RB), wide receiver (WR), tight end (TE), kicker(K) and team defense (DF). We wanted to see if we could transform data sources and NFL statistics, engineer features for machine learning, create data frames and a database to try predict and "cheat" the draft all in an effort to look for potential "sleepers" in our home leagues or daily fantasy drafts to find maximum ability and player for minimal costs. This is our NFL Fantasy AI Predictor. 

**Data Munging and Transformation:**

The datasets used for modeling came from https://www.pro-football-reference.com/. The data consisted of over 1800+ data points over 3 different csvs providing the last 3 years of detailed stats for every player in the NFL since the year 2019. The raw data was initially transformed and munged in Pandas in order to make a more concise and meaningful data extraction to make columns of relevant data for all 2019, 2020, and 2021 NFL players. Considering the draft, we want to predict we made sure that if a player wasn’t eligible to be drafted for the 2022 NFL Fantasy draft, then he would not be including in the testing or training data. The initial analysis formed the basis for the modeling data. From the initial modeling data, we took it multiple steps forward and leveraged our data to create new variables, using calculated fields, that weren’t in the training set or initial data. Some feature engineering, we deemed relevant to fantasy football players were: Total yards from scrimmage, usage, production, total touchdowns, and games played. Also, the fantasy points were calculated for each game of each season for every 2019, 2020, 2021 player. Separate data frames were used for QBs than that of Tight Ends, Running Backs, and Wide Receivers to ensure accuracy. The training data for the models used all the data available for each player up through the 2019-2020 seasons with the 2021 data used as the test data. 

*Running Back DataFrame:*

![Screenshot (135)](https://user-images.githubusercontent.com/101227638/187561481-16959d9b-c094-4549-8691-fe486a647fb5.png)

Additionally, to handle to the rookie class of 2022 we used web scraping and API calls to scrape projected fantasy points for every eligible rookie player from https://www.fantasypros.com/nfl/rankings/rookies.php to gather all projections, match their variables with the ones we created and then combined them to our data of existing players. After multiple data frames were assembled we then combined all of data with a Average Draft Position csv downloaded from https://www.fantasypros.com/nfl/adp/overall.php to see where people were generally drafting the players on the list and how those draft positions stacked up with our feature engineering to then feed into our machine learning methods. 

*Web Scraping FantasyPros:*

![Screenshot (137)](https://user-images.githubusercontent.com/101227638/187561673-9ecd4f0b-03f6-4332-8180-58eca0b144e3.png)


**Machine Learning:** 

Our initial goal is to predict “sleepers”, those players who have potential for big Fantasy Scores but are overlooked by the current models. Since, we are providing suggested draft order for the entire fantasy squad this had to be balanced with “conventional wisdom”, we had to make sure that in our efforts to predict “sleepers” that favored candidates still appeared in draft locations that insured a winning fantasy team. Evaluating models – we looked at a wide range of models in each of the disciplines. We looked at unsupervised learning and while our data did lend itself to clustering, which you will see in a later slide.  We also looked at deep-learning models. We ran our largest dataset though 179 Keras turner trials.  However, the deep learning models suffered to produce good results. We chose to concentrate on supervised learning models to achieve our prediction results. We tested our data against 9 algorithms, with 6 scalers.  We ran each of our 4 sets of data independent of each other. Not all datasets performed equally with each model. Each data set has it own saved ML model. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/101227638/187763616-d7fd26cc-e707-4b15-b98a-80a40afbc2c0.png" />
</p>

In total we ran our largest dataset through over 450 models. In the end linear regression and extra trees regressions produced the best results respective to their input datasets. While our data did form the expected clusters by skill position – the models were unable to produce the ranked results we were looking to get. After establishing some effective models – we focused on creating features and standardizing input features to produce our desired rankings. The wizardry really did happen in this step, If you are interested in seeing how we calculated our magic features by all means check it out in the NFL_Fantasy_improve _Target_woQB notebook.  We were able to verify our magic, by watching a specific player we predicted should be higher in the draft order – move up in the draft order during the few days we had to monitor changes! Yay magic.

<p align="center">
  <img src="https://user-images.githubusercontent.com/101227638/187756292-67800daf-b741-41b9-88c7-3c1126f6608c.png" />
</p>

Lastly, the original target was designed to predict a player’s fantasy value using a target that defines a player by productivity score. This target intentionally discards the current fantasy draft rankings in order to identify "sleepers". However, this target creates some predictor issues from a human analysis. Two examples that precipitated the reevaluation are Andre Roberts and Jonathan Taylor. These two players represent opposite ends of the prediction spectrum. Andre Roberts has an original target Value of 288 the highest of all players. His stats are Production of 288, Usage of .1875, 2021 Fantasy points of 7.0 and a current year draft ranking of Null. Modeling projects him to have the highest draft ranking of 288 in line with his production score. However, given that he has no current ADP he should not be considered a viable draft pick. This is cause by having extremely low usage numbers which causes a very high production score. The other player Jonathan Taylor has an original target value of 97.25, Usage of 3.53, 2021, 2021 Fantasy points of 333 and a current year draft ranking of 1. While preserving the scope of the project of finding sleepers, I am attempting to find a new target that will still identify outliers without skewing the results of high-ranking high score players. Previous evaluations have demonstrated that our ML Models can predict with 99% accuracy the current draft ranking and Production Scores at 98%. This notebook does not intend to improve the modeling but rather the usefulness of the predicted player draft rankings.

![download](https://user-images.githubusercontent.com/101227638/187556446-b91cd149-38c8-4af3-ba9a-276b1897939a.png)
