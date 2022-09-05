#--------------------------------------------------
#           Fantasy Draft Functions           
#      Reformat dissimilar input files       
# Assign players data for the testing period  
#--------------------------------------------------
# laf 08.28.2022


#--------------------------------------------------
#       Function : rookie_fix         
#     Argument: Rookie Non-QB df  
#--------------------------------------------------
def rookie_fix(rx):
    # Add Columns required for ouput 
    rx['2019 FantasyPoints'] = 0
    rx['2020 FantasyPoints'] = 0
    rx['Average Total Production'] = 0
    rx['Production21'] = 0
    
    # Rename column to match non-rookie data 
    rx = rx.rename(columns={'2021 Fantasy Points':'2021 FantasyPoints'})

    # Preserve label information for Output file 
    rxx = rx[['Unnamed: 0',
             'Player',
             '2021 Tm',
             'Pos',
             '2019 FantasyPoints',
             '2020 FantasyPoints',
             '2021 FantasyPoints',
             '2021 Rec',
             '2021 RushingYds',
             '2021 ReceivingTD',
             'Average Total Production',
             'Production21',
             'AVG'
           ]].copy()

    
    # Invert ADP
    rxx['AvgInvert'] = (rxx['AVG'].max() + 1) - rxx['AVG']
    # Give Production Scores and Most recent Fantasy Point equal Weight
    rxx['ProdWeighted'] = rxx['2021 FantasyPoints']
    # Factor in "human factor" of current ADP
    rxx['ProdWeightedSRA'] = (rxx['ProdWeighted'] + rxx['AvgInvert'])/2
    # Correct any Nulls created by source data errors 
    rxx["ProdWeightedSRA"] = rxx["ProdWeightedSRA"].fillna(114)

    return rxx

#--------------------------------------------------
#       Function : rookie_fix_qb         
#     Argument: Rookie Non-QB df  
#--------------------------------------------------
def rookie_fix_qb(rqbx):
    # Add Columns required for ouput 
    rqbx['2019 FantasyPoints'] = 0
    rqbx['2020 FantasyPoints'] = 0
    rqbx['Average Total Production'] = 0
    rqbx['Production21'] = 0
    
    # Rename column to match non-rookie data 
    rqbx = rqbx.rename(columns={'2021 Fantasy Points':'2021 FantasyPoints'})
    
    # Preserve label information for Output file 
    ror = rqbx[['Unnamed: 0',
                'Player',
               '2021 Tm',
               'Pos',
               '2019 FantasyPoints',
               '2020 FantasyPoints',
               '2021 FantasyPoints',
               '2021 RushingYds',
               'Touchdowns21',
               'Average Total Production',
               'Production21',
               'AVG'
            ]].copy()
    
    # Invert ADP
    ror['AvgInvert'] = (ror['AVG'].max() + 1) - ror['AVG']
    # Give Production Scores and most recent Fantasy Point equal Weight
    ror['ProdWeighted'] = ror['2021 FantasyPoints']
    # Factor in "human factor" of current ADP
    ror['ProdWeightedSRA'] = (ror['ProdWeighted'] + ror['AvgInvert'])/2
    # Correct any Nulls created by source data errors 
    ror["ProdWeightedSRA"] = ror["ProdWeightedSRA"].fillna(114)

    return ror

#--------------------------------------------------
#       Function : inactive_fix         
#     Argument: Veteran Non-QB df  
#--------------------------------------------------
# Backfill Features for players who were inactive in prior years
# for the prescribed testing period - NonQB Skill Positions 
def inactive_fix(z):
    # Variables for year substitution 
    C2021 = ['2021 Games', '2021 FantasyPoints','2021 GS','2021 Tgt', '2021 Rec', '2021 RushingTD',
             '2021 RushingYds', '2021 RushingAtt', '2021 ReceivingYds', '2021 ReceivingTD']
    C2020 = ['2020 Games', '2020 FantasyPoints','2020 GS','2020 Tgt', '2020 Rec', '2020 RushingTD',
             '2020 RushingYds', '2020 RushingAtt', '2020 ReceivingYds', '2020 ReceivingTD']
    C2019 = ['2019 Games', '2019 FantasyPoints','2019 GS','2019 Tgt', '2019 Rec', '2019 RushingTD',
             '2019 RushingYds', '2019 RushingAtt', '2019 ReceivingYds', '2019 ReceivingTD']
    CKS = ['Active2021', 'Active2020', 'Active2019']

    # Create Checksum for years 
    z['Active2021'] = z[C2021].sum(axis=1)
    z['Active2020'] = z[C2020].sum(axis=1)
    z['Active2019'] = z[C2019].sum(axis=1)

    # Replace 2020 stats with 2021 stats for learning model 
    z.loc[z["Active2020"] == 0, '2020 Games'] = z['2021 Games']
    z.loc[z["Active2020"] == 0, '2020 FantasyPoints'] = z['2021 FantasyPoints']
    z.loc[z["Active2020"] == 0, '2020 GS'] = z['2021 GS']
    z.loc[z["Active2020"] == 0, '2020 Tgt'] = z['2021 Tgt']
    z.loc[z["Active2020"] == 0, '2020 Rec'] = z['2021 Rec']
    z.loc[z["Active2020"] == 0, '2020 RushingYds'] = z['2021 RushingYds']
    z.loc[z["Active2020"] == 0, '2020 RushingAtt'] = z['2021 RushingAtt']
    z.loc[z["Active2020"] == 0, '2020 ReceivingYds'] = z['2021 ReceivingYds']
    z.loc[z["Active2020"] == 0, '2020 ReceivingTD'] = z['2021 ReceivingTD']

    # Replace 2019 stats with 2020 stats for learning model 
    z.loc[z["Active2019"] == 0, '2019 Games'] = z['2020 Games']
    z.loc[z["Active2019"] == 0, '2019 FantasyPoints'] = z['2020 FantasyPoints']
    z.loc[z["Active2019"] == 0, '2019 GS'] = z['2020 GS'] 
    z.loc[z["Active2019"] == 0, '2019 Tgt'] = z['2020 Tgt']
    z.loc[z["Active2019"] == 0, '2019 Rec'] = z['2020 Rec']
    z.loc[z["Active2019"] == 0, '2019 RushingTD'] = z['2020 RushingTD']
    z.loc[z["Active2019"] == 0, '2019 RushingAtt'] = z['2020 RushingAtt']
    z.loc[z["Active2019"] == 0, '2019 ReceivingYds'] = z['2020 ReceivingYds']
    z.loc[z["Active2019"] == 0, '2019 ReceivingTD'] = z['2020 ReceivingTD']

    # Drop Check Sum columns from DataFrame 
    z.drop(columns=CKS, inplace=True)

    return z

#--------------------------------------------------
#       Function : inactive_fix_qb         
#     Argument: Veteran Quaterback df  
#--------------------------------------------------
# Backfill Features for players who were inactive in prior years
# for the prescribed testing period - Quarterback Position
def inactive_fix_qb(z):
    # # Variables for year substitution 
    CKS = ['Active2021', 'Active2020', 'Active2019']
    C2021 = ['2021 PassingYds', '2021 PassingTD','2021 PassingAtt', '2021 RushingTD',
            '2021 RushingYds', '2021 RushingTD', '2021 Games']
    C2020 = ['2020 PassingYds', '2020 PassingTD','2020 PassingAtt', '2020 RushingTD',
            '2020 RushingYds', '2020 RushingTD', '2020 Games']
    C2019 = ['2019 PassingYds', '2019 PassingTD','2019 PassingAtt', '2019 RushingTD',
            '2019 RushingYds', '2019 RushingTD', '2019 Games']

    # Create Checksum for years 
    z['Active2021'] = z[C2021].sum(axis=1)
    z['Active2020'] = z[C2020].sum(axis=1)
    z['Active2019'] = z[C2019].sum(axis=1)

    # Drop any player with no combined stats for 2021
    z.drop(z[(z['Active2021'] == 0)].index)

    # Replace 2020 stats with 2021 stats for learning model 
    z.loc[z["Active2020"] == 0, '2020 Games'] = z['2021 Games']
    z.loc[z["Active2020"] == 0, '2020 FantasyPoints'] = z['2021 FantasyPoints']
    z.loc[z["Active2020"] == 0, '2020 PassingYds'] = z['2021 PassingYds']
    z.loc[z["Active2020"] == 0, '2020 PassingTD'] = z['2021 PassingTD']
    z.loc[z["Active2020"] == 0, '2020 PassingAtt'] = z['2021 PassingAtt']
    z.loc[z["Active2020"] == 0, '2020 RushingTD'] = z['2021 RushingTD']
    z.loc[z["Active2020"] == 0, '2020 RushingYds'] = z['2021 RushingYds']


    # Replace 2019 stats with 2020 stats for learning model 
    z.loc[z["Active2019"] == 0, '2019 Games'] = z['2020 Games']
    z.loc[z["Active2019"] == 0, '2019 FantasyPoints'] = z['2020 FantasyPoints']
    z.loc[z["Active2019"] == 0, '2019 PassingYds'] = z['2020 PassingYds']
    z.loc[z["Active2019"] == 0, '2019 PassingTD'] = z['2020 PassingTD']
    z.loc[z["Active2019"] == 0, '2019 PassingAtt'] = z['2020 PassingAtt']
    z.loc[z["Active2019"] == 0, '2019 RushingTD'] = z['2020 RushingTD']
    z.loc[z["Active2019"] == 0, '2019 RushingYds'] = z['2020 RushingYds']

    # Drop Check Sum columns from DataFrame 
    z.drop(columns=CKS, inplace=True)

    return z