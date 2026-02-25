import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson 

st.title("Super Shot Decision Model")
st.write(
    "This app provides data based recommendations on super shot strategy."
)
st.write(
    "Game Conditions:"
)
Quarter = st.number_input('Quarter',min_value=1,max_value=4) #Quarter
col1, col2 = st.columns(2)
TimeLeftMin = col1.number_input('Minutes Remaining in Quarter',min_value=0,max_value=4) #Minutes Left in quarter
TimeLeftSec = col2.number_input('Seconds Remaining in Quarter',min_value=0,max_value=59)  #Seconds Left in quarter
col1, col2 = st.columns(2)
TeamPoints = col1.number_input(':violet[Team Points]',min_value=0,max_value=150)  #Current team points
OppPoints = col2.number_input(':red[Opposition Points]',min_value=0,max_value=150)  #Current opposition points

st.write(
    ":violet[Team Attacking Metrics:]"
)
col1, col2 = st.columns(2)
TeamPPPNorm = col1.number_input('Team Points Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Team Points per possesion in normal play
TeamPPPSuper = col2.number_input('Team Points Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Team Points per possesion in supershot play

st.write(
    ":violet[Team Defending Metrics:]"
)
col1, col2 = st.columns(2)
TeamDefPPPNorm = col1.number_input('Team Points Against Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Team Points agaimst per possesion in normal play
TeamDefPPPSuper = col2.number_input('Team Points Against Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Team Points against per possesion in supershot play

st.write(
    ":red[Opposition Attacking Metrics:]"
)
col1, col2 = st.columns(2)
OppPPPNorm = col1.number_input('Opp Points Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Opposition Points per possesion in normal play
OppPPPSuper = col2.number_input('Opp Points Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Opposition Points per possesion in supershot play

st.write(
    ":red[Opposition Defending Metrics:]"
)
col1, col2 = st.columns(2)
OppDefPPPNorm = col1.number_input('Opp Points Against Per Possession (Normal Play)',min_value=0.00,max_value=1.00) #Opposition Points against per possesion in normal play
OppDefPPPSuper = col2.number_input('Opp Points Against Per Possession :green[(Supershot Play)]',min_value=0.00,max_value=2.00) #Opposition Points against per possesion in supershot play

st.write(
    ":violet[Pulse Shooting Metrics:]"
)
col1, col2 = st.columns(2)
GS1P = col1.number_input('Goal Shooter 1 Point %', min_value=0,max_value=100) #Goal Shooter 1 pointer %
GS2P = col1.number_input(':green[Goal Shooter 2 Point %]', min_value=0,max_value=100) #Goal Shooter 2 pointer %
GA1P = col2.number_input('Goal Attack 1 Point %', min_value=0,max_value=100) #Goal Attack 1 pointer %
GA2P = col2.number_input(':green[Goal Attack 2 Point %]', min_value=0,max_value=100) #Goal Attack 2 pointer %

st.write(
    "Pace Metrics:"
)
col1, col2 = st.columns(2)
AvgTeamPossLength = col1.number_input(':violet[Average Team Attacking Possession Length in Seconds]', min_value=1,max_value=100) #Average team possession length
AvgTeamPossAgainstLength = col2.number_input(':violet[Average Team Defending Possession Length in Seconds]', min_value=1,max_value=100) #Average team possession against length
col1, col2 = st.columns(2)
AvgOppPossLength = col1.number_input(':red[Average Opp Attacking Possession Length in Seconds]', min_value=1,max_value=100) #Average opposition possession length
AvgOppPossAgainstLength = col2.number_input(':red[Average Opp Defending Possession Length in Seconds]', min_value=1,max_value=100) #Average opposition possession against length
col1, col2 = st.columns(2)
AvgOppTOLength = col1.number_input(':violet[Average Team Defending TO Possession Length in Seconds]', min_value=1,max_value=100) #Average Opp turnover possession length
AvgTeamTOAgainstLength = col2.number_input(':red[Average Opp Attacking TO Possession Length in Seconds]', min_value=1,max_value=100) #Average team turnover possession against length

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
    col1.write('**Goal Shooter should look for the easiest shot**')
if GSOutcome == 0:
    col1.write('**Goal Shooter has equal outcomes**')
if GAOutcome > 0:
    col2.write('**Goal Attack should look for a :green[supershot]**')
if GAOutcome < 0:
    col2.write('**Goal Attack should look for the easiest shot**')
if GAOutcome == 0:
    col2.write('**Goal Attack has equal outcomes**')

col1, col2 = st.columns(2)
col1.write(f'Win Probability with GS 2: {GS2PWin.round(2)}%')
col1.write(f'Win Probability with GS 1: {GS1PWin.round(2)}%')
col2.write(f'Win Probability with GA 2: {GA2PWin.round(2)}%')
col2.write(f'Win Probability with GA 1: {GA1PWin.round(2)}%')
