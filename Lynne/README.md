# NFL-Fantasy Draft "sleepers" Model Tuning and Creation space

Folder Contents: 

This folder contains all of the testing and model development for the Fantasy "Sleeper" prediction project.

#### Initial Data Evaluations 
* NFLExplore.ipynb  
* NFL_Model.ipynb    

#### ML learning model testing  
* NFL_unsupervised_model_Tuner_woQB.ipynb  
* NFL_Fantasy_NN.ipynb  
* NFL_Fantasy_model_Tuner.ipynb  
* NFL_Model.ipynb   

#### Model Creation  
* NFL_Fantasy_Rookie_QB.ipynb  
* NFL_Fantasy_Rookie_woQB.ipynb  
* NFL_Fantasy_model_Tuner_QB.ipynb  
* NFL_Fantasy_model_Tuner_woQB.ipynb  

#### Misc Development Notebooks
* Rookie.ipynb (obsolete) see .py
* NFL_Fantasy_Predictor.ipynb (obsolete) see .py
* Integration.ipynb (obsolete) see NFL_Fantasy_Predictor.py

#### Production Scripts
* NFL_Fantasy_Predictor.py
    * This script takes the target calculated imput files from Ronnie directory and the webscraped rookie data from Yi directory makes data and format changes. Then runs them against their respective ML Models and produces a raw output file to rebuild the postgres data. 
*  Rookie.py
    * This script contains all the custom functions to prepare the raw files to be run through the ML models.    

#### Set-up Scripts 
* NFLHeadShots.ipynb
   * Adds headshots for all players in our current draft file (that have headshots available)
