#-------------------------------------------------------------------#
# Blurb                                                             #
#-------------------------------------------------------------------#
# Project: FPL: Building an algorithm to maximise FPL performance   #
# Data Scientist(s): Rad Siddiqui, Fahid Rahman                     #
# Filename: basic_23_24.py (to be renamed, to '01 - Cleaning data') #
# Aim: To clean the "cleaned_merged_seasons_team_aggregated" file   #
#-------------------------------------------------------------------#
# Steps taken                                                       #
#-------------------------------------------------------------------#
# [1A] Setting up: Importing packages and files                     #
# [1B] Setting up: Retaining relevant data only                     #
# [2] Creating a player-ID                                          #
# [3] Creating new variables                                        #
# [4] Creating a player-level DF                                    #
# [5] Deriving PPM                                                  #
#-------------------------------------------------------------------#

#-----------------------------------------------#
# [1A] Setting up: Importing packages and files #
#-----------------------------------------------#

# Importing appropriate Python packages.

import pandas as pd

# Importing all merged data from seasons XX-XX to 24-25.

original_DF = pd.read_csv("G:/My Drive/personal projects/fpl/FPL/cleaned_merged_seasons_team_aggregated.csv")

original_DF.info()

#-----------------------------------------------#
# [1B] Setting up: Retaining relevant data only #
#-----------------------------------------------#

# Only need the following variables for now (subject to change).

df = original_DF[(original_DF['season_x'] != "2023-24")]

df = df[["season_x", "team_x", "name", "position", "total_points", "value", "GW"]]

#--------------------------#
# [2] Creating a player-ID #
#--------------------------#

df = df.copy()
df["player_ID"] = (df.groupby(["name", "position"]).ngroup())

df.sort_values(by = "player_ID", ascending = True)

#----------------------------#
# [3] Creating new variables #
#----------------------------#

# 'total_points': Creating a 'total_points' column, for the total # ...
# ... points accumulated per player over the season.

df['season_total_points'] = df.groupby(['player_ID', 'season_x'])['total_points'].transform('sum')

print(df[df["name"] == "Cole Palmer"])

# value: amending 'value' column to be in millions.

df["value"] = df["value"] / 10

#--------------------------------#
# [4] Creating a player-level DF #
#--------------------------------#

df = df[(df['GW'] == 38)]

#------------------#
# [5] Deriving PPM #
#------------------#

# PPM

# Creating a 'PPM' column, for the total # points per million ...
# ... (i.e., points gained per cost of player) accumulated per player ...
# ... over the season; e.g., if Cole Palmer accumulates 200 points by ...
# ... the end of the season, and he cost £10M at GW38, then his ...
# ... 'PPM' = 200 / 10 = 2.

df = df.copy()
df["PPM"] = df["season_total_points"] / df["value"]

df = df[["player_ID", "season_x", "team_x", "name", "position", "season_total_points", "PPM"]]

print(df[df["name"] == "Cole Palmer"])
print(df[df["name"] == "Mohamed Salah"])