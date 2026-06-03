import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

data = {
    "Team":['Custom','Birmingham Panthers','Cardiff Dragons','Leeds Rhinos','London Mavs','London Pulse','Loughborough Lightning','Manchester Thunder','Nottingham Forest'],
    "Points Per Possession (Normal Play)":[0,0.57,0.70,0.55,0.60,0.66,0.79,0.68,0.66],
    "Points Per Possession (Supershot Play)":[0,0.71,0.82,0.85,0.91,0.84,1.13,0.99,0.90],
    "Points Against Per Possession (Normal Play)":[0,0.72,0.66,0.66,0.62,0.57,0.67,0.65,0.64],
    "Points Against Per Possession (Supershot Play)":[0,0.97,0.96,0.87,0.91,0.86,0.93,0.77,0.87],
    "Attacking Possession Length":[1,26.57,28.53,27.92,28.66,26.23,28.31,27.72,26.23],
    "Defending Possession Length":[1,28.04,27.47,27.67,27.01,28.57,27.30,27.26,26.84],
    "Def Reb Attack length":[1,36,38,37,36,31,43,35,32],
    "Def Reb Defend length":[1,33,33,39,38,46,45,38,31]
}
teamdata = pd.DataFrame(data)
st.title("Super Shot Decision Model")
st.write(
    "This app provides data based recomendations on super shot strategy or match outcome probabilities"
)

mode = st.selectbox("Select Mode",["Supershot","Prediction"])

col1, col2 = st.columns(2)
team = col1.selectbox(
    "Select a team",
    (teamdata),
)
opp = col2.selectbox(
    "Select an opposition",
    (teamdata),
)

teamdf = teamdata[teamdata.Team == team]
oppdf = teamdata[teamdata.Team == opp]

st.write(
    "Game Conditions:"
)
Quarter = st.number_input('Quarter',min_value=1,max_value=4) #Quarter
col1, col2 = st.columns(2)
if mode == "Supershot":
    TimeLeftMin = col1.number_input('Minutes Remaining in Quarter',min_value=0,max_value=5,value=5) #Minutes Left in quarter
    TimeLeftSec = col2.number_input('Seconds Remaining in Quarter',min_value=0,max_value=59)  #Seconds Left in quarter
if mode == "Prediction":
    TimeLeftMin = col1.number_input('Minutes Remaining in Quarter',min_value=0,max_value=15,value=15) #Minutes Left in quarter
    TimeLeftSec = col2.number_input('Seconds Remaining in Quarter',min_value=0,max_value=59)  #Seconds Left in quarter
col1, col2 = st.columns(2)
TeamPoints = col1.number_input(':violet[Team Points]',min_value=0,max_value=100)  #Current team points
OppPoints = col2.number_input(':red[Opp Points]',min_value=0,max_value=100)  #Current opposition points

if team=="Custom":
    st.write(
        ":violet[Normal Attacking Metrics:]"
    )
    col1, col2 = st.columns(2)
    TeamPPPNorm = col1.number_input('Team Points Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Team Points per possesion in normal play
    OppPPPNorm = col2.number_input('Opp Points Per Possession (Normal Play)', min_value=0.00,max_value=1.00) #Team Points per possesion in supershot play

    st.write(
        ":violet[Supershot Attacking Metrics:]"
    )
    col1, col2 = st.columns(2)
    TeamPPPSuper = col1.number_input('Team Points Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Team Points agaimst per possesion in normal play
    OppPPPNorm = col2.number_input('Opp Points Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Team Points against per possesion in supershot play

if team!="Custom":
    TeamPPPNorm = teamdf.iloc[0]['Points Per Possession (Normal Play)']
    TeamPPPSuper = teamdf.iloc[0]['Points Per Possession (Supershot Play)']
    OppPPPNorm = oppdf.iloc[0]['Points Against Per Possession (Normal Play)']
    OppPPPSuper = oppdf.iloc[0]['Points Against Per Possession (Supershot Play)']
    
    st.write(
        ":violet[Normal Attacking Metrics:]"
    )
    col1, col2 = st.columns(2)
    col1.write(f"Team Normal Points Per Possesion: {TeamPPPNorm}")
    col2.write(f"Opp Normal Points Per Possesion: {OppPPPNorm}")

    st.write(
        ":violet[Supershot Attacking Metrics:]"
    )
    col1, col2 = st.columns(2)
    col1.write(f"Team Supershot Points Per Possesion: :green[{TeamPPPSuper}]")
    col2.write(f"Opp Supershot Points Per Possesion: :green[{OppPPPSuper}]")

if opp=="Custom":
    st.write(
        ":red[Normal Defending Metrics:]"
    )
    col1, col2 = st.columns(2)
    TeamDefPPPNorm = col1.number_input('Team Points Against Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Opposition Points per possesion in normal play
    OppDefPPPNorm = col2.number_input('Opp Points Against Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Opposition Points per possesion in supershot play

    st.write(
        ":red[Supershot Defending Metrics:]"
    )
    col1, col2 = st.columns(2)
    TeamDefPPPSuper = col1.number_input('Team Points Against Per Possession :red[(Supershot Play)]',min_value=0.00,max_value=2.00) #Opposition Points against per possesion in normal play
    OppDefPPPSuper = col2.number_input('Opp Points Against Per Possession :red[(Supershot Play)]',min_value=0.00,max_value=2.00) #Opposition Points against per possesion in supershot play

if opp!="Custom":
    TeamDefPPPNorm = teamdf.iloc[0]['Points Against Per Possession (Normal Play)']
    TeamDefPPPSuper = teamdf.iloc[0]['Points Against Per Possession (Supershot Play)']
    OppDefPPPNorm = oppdf.iloc[0]['Points Against Per Possession (Normal Play)']
    OppDefPPPSuper = oppdf.iloc[0]['Points Against Per Possession (Supershot Play)']
    st.write(
        ":red[Normal Defending Metrics:]"
    )
    col1, col2 = st.columns(2)
    col1.write(f"Team Normal Points Against Per Possesion: {TeamDefPPPNorm}")
    col2.write(f"Opp Normal Points Against Per Possesion: {OppDefPPPNorm}")

    st.write(
        ":red[Supershot Defending Metrics:]"
    )
    col1, col2 = st.columns(2)
    col1.write(f"Team Supershot Points Against Per Possesion: :red[{TeamDefPPPSuper}]")
    col2.write(f"Opp Supershot Points Against Per Possesion: :red[{OppDefPPPSuper}]")

st.write(
    "Pace Metrics:"
)

if team=="Custom":
    col1, col2 = st.columns(2)
    AvgTeamPossLength = col1.number_input(':violet[Average Team Attacking Possession Length in Seconds]', min_value=1,max_value=100) #Average team possession length
    AvgOppPossLength = col2.number_input(':violet[Average Opp Attacking Possession Length in Seconds]', min_value=1,max_value=100) #Average team possession against length

if team!="Custom":
    AvgTeamPossLength = teamdf.iloc[0]['Attacking Possession Length']
    AvgOppPossLength = oppdf.iloc[0]['Attacking Possession Length']
    col1, col2 = st.columns(2)
    col1.write(f"Team Average Attacking Possession Length: {AvgTeamPossLength}")
    col2.write(f"Opp Average Attacking Possession Length: {AvgOppPossLength}")



if opp=="Custom":
    col1, col2 = st.columns(2)
    AvgTeamPossAgainstLength = col1.number_input(':red[Average Team Defending Possession Length in Seconds]', min_value=1,max_value=100) #Average opposition possession length
    AvgOppPossAgainstLength = col2.number_input(':red[Average Opp Defending Possession Length in Seconds]', min_value=1,max_value=100) #Average opposition possession against length

if opp!="Custom":
    AvgTeamPossAgainstLength = teamdf.iloc[0]['Defending Possession Length']
    AvgOppPossAgainstLength = oppdf.iloc[0]['Defending Possession Length']
    col1, col2 = st.columns(2)
    col1.write(f"Team Average Defensive Possession Length: {AvgTeamPossAgainstLength}")
    col2.write(f"Opp Average Defensive Possession Length: {AvgOppPossAgainstLength}")

col1, col2 = st.columns(2)
if team=="Custom":
    AvgTeamTOAgainstLength = col1.number_input(':violet[Average team full defensive transition length in seconds]', min_value=1,max_value=100) #Average Opp turnover possession length
if opp=="Custom":
    AvgOppTOLength = col2.number_input(':red[Average opp full attacking transition length in seconds]', min_value=1,max_value=100) #Average team turnover possession against length

if team!="Custom":
    AvgTeamTOAgainstLength = oppdf.iloc[0]['Def Reb Defend length']
    col1.write(f"Team average full defending transition length: {AvgTeamTOAgainstLength}")

if opp!="Custom":
    AvgOppTOLength = oppdf.iloc[0]['Def Reb Attack length']
    col2.write(f"Opp average full attacking transition length: {AvgOppTOLength}")

if mode=="Supershot":
    st.write(
        ":violet[Team Shooting Metrics:]"
    )
    col1, col2 = st.columns(2)
    GS1P = col1.number_input('Goal Shooter 1 Point %', min_value=0,max_value=100) #Goal Shooter 1 pointer %
    GS2P = col1.number_input(':green[Goal Shooter 2 Point %]', min_value=0,max_value=100) #Goal Shooter 2 pointer %
    GA1P = col2.number_input('Goal Attack 1 Point %', min_value=0,max_value=100) #Goal Attack 1 pointer %
    GA2P = col2.number_input(':green[Goal Attack 2 Point %]', min_value=0,max_value=100) #Goal Attack 2 pointer %

TimeLeft = (((4-Quarter)*15)*60)+(TimeLeftMin*60)+TimeLeftSec
if TimeLeftMin >= 5:
    TimeLeftNormal = (((4-Quarter)*10)*60)+((TimeLeftMin-5)*60)+TimeLeftSec
if TimeLeftMin < 5:
    TimeLeftNormal = (((4-Quarter)*10)*60)
if TimeLeftMin >= 5:
    TimeLeftSuper = (((4-Quarter)*5)*60)
if TimeLeftMin < 5:
    TimeLeftSuper = (((4-Quarter)*5)*60)+((TimeLeftMin)*60)+TimeLeftSec

GameTeamPosLength = (AvgTeamPossLength+AvgOppPossAgainstLength)/2 #Team adjusted team possession lenght
GameTeamPPPNorm = (TeamPPPNorm+OppDefPPPNorm)/2 #Team adjusted points per possession in normal play
GameTeamPPPSuper = (TeamPPPSuper+OppDefPPPSuper)/2 #Team adjusted points per possession in supershot play

GameOppPosLength = (AvgOppPossLength+AvgTeamPossAgainstLength)/2 #Opposition adjusted team possession lenght
GameOppPPPNorm = (OppPPPNorm+TeamDefPPPNorm)/2 #Opposition adjusted points per possession in normal play
GameOppPPPSuper = (OppPPPSuper+TeamDefPPPSuper)/2 #Opposition adjusted points per possession in supershot play

def netball_win_probabilities(GameTeamPPPNorm,GameTeamPPPSuper,GameOppPPPNorm,GameOppPPPSuper,GameTeamPosLength,GameOppPosLength,TimeLeftNormal,TimeLeftSuper,TeamPoints,OppPoints):
    
    ScoreDiff = TeamPoints-OppPoints #Score Difference
    
    PossesionsLeftNorm = TimeLeftNormal/(GameTeamPosLength+GameOppPosLength) #Normal possessions left 
    TeamExpectedPointsNorm = PossesionsLeftNorm*TeamPPPNorm #Expected team points in normal time
    OppEXpectedPointsNorm = PossesionsLeftNorm*OppPPPNorm #Expected opposition points in normal time
    
    PossesionsLeftSuper = TimeLeftSuper/(GameTeamPosLength+GameOppPosLength) #Supershot possessions left
    TeamExpectedPointsSuper = PossesionsLeftSuper*TeamPPPSuper #Expected team points in supershot time
    OppExpectedPointsSuper = PossesionsLeftSuper*OppPPPSuper #Expected opposition points in supershot time
    
    TeamExpectedPoints = TeamExpectedPointsNorm+TeamExpectedPointsSuper #Total team expected points
    OppExpectedPoints = OppEXpectedPointsNorm+OppExpectedPointsSuper #Total opposition expected points

    max_goals = 100 #Goal limit

    TeamPointsProb = poisson.pmf(np.arange(max_goals), TeamExpectedPoints) #Team point matrix
    OppPointsProb = poisson.pmf(np.arange(max_goals), OppExpectedPoints) #Opposition point matrix
    prob_matrix = np.outer(TeamPointsProb, OppPointsProb) #Full matrix

    TeamWinProb = 0.0 #Reset win probs
    DrawProb = 0.0
    OppWinProb = 0.0

    for TeamExpectedPoints in range(max_goals):
        for OppExpectedPoints in range(max_goals):
            FinalDiff = ScoreDiff + TeamExpectedPoints - OppExpectedPoints #Adjust win conditions based on current score
            p = prob_matrix[TeamExpectedPoints, OppExpectedPoints]
            if FinalDiff > 0:
                TeamWinProb += p
            elif FinalDiff == 0:
                DrawProb += p
            else:
                OppWinProb += p
                
    TeamWinProb = TeamWinProb+(DrawProb)/2 #Add half draw probability to each team for ease of not having to add overtime for few use cases
    OppWinProb = OppWinProb+(DrawProb)/2
    
    return TeamWinProb, OppWinProb

TeamWinProb,OppWinProb = netball_win_probabilities(GameTeamPPPNorm,GameTeamPPPSuper,GameOppPPPNorm,GameOppPPPSuper,GameTeamPosLength,GameOppPosLength,TimeLeftNormal,TimeLeftSuper,TeamPoints,OppPoints)

def apply_win_probs_2_made():
    TeamWinProb, OppWinProb = netball_win_probabilities(
        GameTeamPPPNorm,
        GameTeamPPPSuper,
        GameOppPPPNorm, GameOppPPPSuper,
        GameTeamPosLength,
        GameOppPosLength,
        TimeLeftNormal,
        TimeLeftSuper,
        TeamPoints + 2,
        OppPoints
    )
    
    TeamWin2P = TeamWinProb
    OppWin2P = OppWinProb
    
    return TeamWin2P, OppWin2P

TeamWin2P,OppWin2P = apply_win_probs_2_made()

def apply_win_probs_1_made():
    TeamWinProb,OppWinProb = netball_win_probabilities(
        GameTeamPPPNorm,
        GameTeamPPPSuper,
        GameOppPPPNorm,GameOppPPPSuper,
        GameTeamPosLength,
        GameOppPosLength,
        TimeLeftNormal,
        TimeLeftSuper,
        TeamPoints+1,
        OppPoints
    )
    
    TeamWin1P = TeamWinProb
    OppWin1P = OppWinProb
    
    return TeamWin1P,OppWin1P

TeamWin1P,OppWin1P = apply_win_probs_1_made()

def apply_win_probs_miss():
    TeamWinProb,OppWinProb = netball_win_probabilities(
        GameTeamPPPNorm,
        GameTeamPPPSuper,
        GameOppPPPNorm,
        GameOppPPPSuper,
        GameTeamPosLength,
        GameOppPosLength,
        TimeLeftNormal,
        TimeLeftSuper-(AvgOppTOLength+AvgTeamTOAgainstLength)/2,
        TeamPoints,
        OppPoints+GameOppPPPSuper
    )
    
    TeamWinMiss = TeamWinProb
    OppWinMiss = OppWinProb  
    
    return TeamWinMiss,OppWinMiss
    
TeamWinMiss,OppWinMiss = apply_win_probs_miss()

if mode=="Supershot":
    GS2PWin = ((GS2P*TeamWin2P)+((100-GS2P)*TeamWinMiss))
    GS1PWin = ((GS1P*TeamWin1P)+((100-GS1P)*TeamWinMiss))
    GA2PWin = ((GA2P*TeamWin2P)+((100-GA2P)*TeamWinMiss))
    GA1PWin = ((GA1P*TeamWin1P)+((100-GA1P)*TeamWinMiss))
    
    col1, col2 = st.columns(2)
    GSOutcome = GS2PWin-GS1PWin
    GAOutcome = GA2PWin-GA1PWin
    if GSOutcome > 0:
        col1.write('**Goal Shooter should look for a :green[supershot]**')
    if GSOutcome < 0:
        col1.write('**Goal Shooter should look for the :red[easiest shot]**')
    if GSOutcome == 0:
        col1.write('**Goal Shooter has equal outcomes**')
    if GAOutcome > 0:
        col2.write('**Goal Attack should look for a :green[supershot]**')
    if GAOutcome < 0:
        col2.write('**Goal Attack should look for the :red[easiest shot]**')
    if GAOutcome == 0:
        col2.write('**Goal Attack has equal outcomes**')
    
    col1, col2 = st.columns(2)
    col1.write(f'Win Probability with GS 2: {GS2PWin.round(2)}%')
    col1.write(f'Win Probability with GS 1: {GS1PWin.round(2)}%')
    col2.write(f'Win Probability with GA 2: {GA2PWin.round(2)}%')
    col2.write(f'Win Probability with GA 1: {GA1PWin.round(2)}%')
    
    M1PWin = TeamWin1P*100
    M2PWin = TeamWin2P*100
    MissWin = TeamWinMiss*100
    
    col1, col2 = st.columns(2)
    col1.write(f'Win Probability with a made 1: {M1PWin.round(2)}%')
    col2.write(f'Win Probability with a made 2: {M2PWin.round(2)}%')
    st.write(f'Win Probability with a miss: {MissWin.round(2)}%')

if mode=="Prediction":
    TeamWinProb=TeamWinProb*100
    OppWinProb=OppWinProb*100
    st.write(
    "Win Probabilities:"
    )
    if TeamWinProb > 50:
        colour = 'green'
    col1, col2 = st.columns(2)
    col1.write(f'Team Win Probability: {TeamWinProb.round(2)}%')
    col2.write(f'Opp Win Probability: {OppWinProb.round(2)}%')
    
