# -------------------------------------------------------------------
# NFL Fantasy Football Draft Position Predictor
# -------------------------------------------------------------------
# This script runs the model from NFL_Fantasy_model_Tuner(s).
# Two Input files are required 
#     All skills positions
#     Quaterbacks only 
# They use two different Models and has different features
# Input data with the values of Infinity cannot be scaled.
# Those players with a value of Infinty in any field will be dropped.
# -------------------------------------------------------------------
# laf 08.24.2022

# Dependancies
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import joblib
import sys
from Rookie import rookie_fix, rookie_fix_qb, inactive_fix, inactive_fix_qb

# Results Column Labels
RSC = ['Player','2019 FantasyPoints', '2020 FantasyPoints', '2021 FantasyPoints',
       'Production21', 'Average Total Production', '2021 Tm', 'Pos', 'AVG'] 

# Load NFL Fantasy Prediction Model
draft = joblib.load("Resources/draft_position_no_QB.joblib")
qbdraft = joblib.load("Resources/draft_position_qb.joblib")
rdraft = joblib.load("Resources/draft_Rookie.joblib")

# Load Data to run predictions
# Skill Players Not Including Quarterbacks
adp = pd.read_csv('Resources/ADPxFinal.csv') # Skill Players Not Including Quarterbacks
qb = pd.read_csv('Resources/QBxADPxFinal.csv') # Quarterbacks
r = pd.read_csv('Resources/Rookies_RB_WR_TE.csv') # Skill Players Not Including Quarterbacks(rookies)
rqb = pd.read_csv('Resources/Rookies_QB.csv') # Quarterbacks(rookies)

# Drop players ineligible to be drafted 
adp.dropna(subset=['AVG'], inplace=True)
qb.dropna(subset=['AVG'], inplace=True)
r.dropna(subset=['AVG'], inplace=True)
rqb.dropna(subset=['AVG'], inplace=True)
qb.drop(qb[qb['AVG'] == 0].index, inplace = True)  # For Veteran QB Only null AVG 0 in source

r = rookie_fix(r)
rqb = rookie_fix_qb(rqb)
adp = inactive_fix(adp)
adp = inactive_fix_qb(qb)

# Preserve label information for Output file 
adp_scope = adp[RSC].copy()
qb_scope = qb[RSC].copy()
r_scope = r[RSC].copy()
rqb_scope = rqb[RSC].copy()

# Drop unnamed column, Player, Pos and 2021 Team
col = [0,1,2,3]
adp.drop(adp.columns[col],axis=1,inplace=True)
qb.drop(qb.columns[col],axis=1,inplace=True)
r.drop(r.columns[col],axis=1,inplace=True)
rqb.drop(rqb.columns[col],axis=1,inplace=True)

# For all dataset verify validity of data
# Veteran players non_QB and QB
# Verify that expected numeric data is numeric 
invalidNumbers = adp[~adp.applymap(np.isreal).all(1)]
if len(invalidNumbers) > 0:
    sys.exit(f'There are {len(invalidNumbers)} rows with invalid numeric data')
invalidNumbers = qb[~qb.applymap(np.isreal).all(1)]
if len(invalidNumbers) > 0:
    sys.exit(f'There are {len(invalidNumbers)} rows with invalid numeric data')
    
# Check for unexpected nulls 
count_nan = adp.isna().sum().sum()
if count_nan > 0:
    sys.exit(f'Invalid data Encountered: {count_nan} fields have null values')
count_nan = qb.isna().sum().sum()
if count_nan > 0:
    sys.exit(f'Invalid data Encountered: {count_nan} fields have null values')

# All other skill rookie
# Verify that all numeric data is numeric 
invalidNumbers = r[~r.applymap(np.isreal).all(1)]
if len(invalidNumbers) > 0:
    sys.exit(f'There are {len(invalidNumbers)} rows with invaid numeric data')
    
# Check for unexpected nulls 
count_nan = r.isna().sum().sum()
if count_nan > 0:
    sys.exit(f'Invaid data Encountered: {count_nan} fields have null values')

# QB Rookie
# Verify that all numeric data is numeric 
invalidNumbers = rqb[~rqb.applymap(np.isreal).all(1)]
if len(invalidNumbers) > 0:
    sys.exit(f'There are {len(invalidNumbers)} rows with invaid numeric data')
    
# Check for unexpected nulls 
count_nan = rqb.isna().sum().sum()
if count_nan > 0:
    sys.exit(f'Invaid data Encountered: {count_nan} fields have null values')


# Drop rows that contain infinity values in our Results Dataset 
adp_scope.replace([np.inf, -np.inf], 'drop', inplace=True)
adp_scope = adp_scope[~adp_scope.eq('drop').any(1)]

qb_scope.replace([np.inf, -np.inf], 'drop', inplace=True)
qb_scope = qb_scope[~qb_scope.eq('drop').any(1)]

r_scope.replace([np.inf, -np.inf], 'drop', inplace=True)
r_scope = r_scope[~r_scope.eq('drop').any(1)]

rqb_scope.replace([np.inf, -np.inf], 'drop', inplace=True)
rqb_scope = rqb_scope[~rqb_scope.eq('drop').any(1)]


# Drop rows that contain infinity values in our Prediction Dataset 
adp.replace([np.inf, -np.inf], np.nan, inplace=True)
adp.dropna(inplace=True)

qb.replace([np.inf, -np.inf], np.nan, inplace=True)
qb.dropna(inplace=True)

r.replace([np.inf, -np.inf], np.nan, inplace=True)
r.dropna(inplace=True)

rqb.replace([np.inf, -np.inf], np.nan, inplace=True)
rqb.dropna(inplace=True)


# Standarize data with Scaler required by model 
qbs = MinMaxScaler().fit_transform(qb)
apds = MinMaxScaler().fit_transform(adp)
rs = MinMaxScaler().fit_transform(r)
rqbs = MinMaxScaler().fit_transform(rqb)


# Applying PCA to reduce dimensions to the number required by each model  
pca = PCA(n_components= 23)
pcaq = PCA(n_components= 14)
pcar = PCA(n_components= 3)
pcarq = PCA(n_components= 3)


# Fit our new Principal Component Analysis reduced Features to our Model
pfa = pca.fit_transform(apds)
pfb = pcaq.fit_transform(qbs)
pfc = pcar.fit_transform(r)
pfd = pcarq.fit_transform(rqb)


# Transform PCA data to a DataFrame
pf = pd.DataFrame(data=pfa)
pfqb = pd.DataFrame(data=pfb)
pfr = pd.DataFrame(data=pfc)
pfrqb = pd.DataFrame(data=pfd)


# Predict Draft Positions
draft_position = draft.predict(pf)
qb_draft_position = qbdraft.predict(pfqb)
r_draft_position = rdraft.predict(pfc)
rqb_draft_position = rdraft.predict(pfd)


# Add predicted draft positions to our results file 
adp_scope['Prediction'] = draft_position
qb_scope['Prediction'] = qb_draft_position
r_scope['Prediction'] = r_draft_position
rqb_scope['Prediction'] = rqb_draft_position


# Variable to hold dfs that make up our result set
frames = [adp_scope, qb_scope, r_scope, rqb_scope]

# Combine DataFrames into complete dataset
final = pd.concat(frames)
final = final.reset_index()

# Write file to csv 
final.to_csv('Resources/DraftTest.csv')