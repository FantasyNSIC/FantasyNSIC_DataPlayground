import pandas as pd
import numpy as np
import re

def main(team):
    # Read the file
    with open('src/raw_data/2023_stats/{}2023.txt'.format(team), 'r') as file:
        lines = re.split(r'\n\n', file.read())

    # Initialize Header Lists
    rushingHeader = [
        "first_name",
        "last_name",
        "gp",
        "rush_att",
        "rush_yds",
        "rush_avg",
        "rush_td",
    ]

    passingHeader = [
        "first_name",
        "last_name",
        "gp",
        "pass_comp",
        "pass_att",
        "pass_yds",
        "pass_td",
        "pass_int",
    ]

    recievingHeader = [
        "first_name",
        "last_name",
        "gp",
        "recieve_rec",
        "recieve_yds",
        "recieve_avg",
        "recieve_td",
    ]

    # Seperate sections in respective lists.
    rushingStats = lines[0].split('\n')
    passingStats = lines[1].split('\n')
    recievingStats = lines[2].split('\n')

    # Iterate over rushing stats, add to DataFrame
    rushingNewEntries = []
    for line in rushingStats[1:]:
        line = line.replace(',', '')
        line = line.split()
        newEntry = [
            line[1],
            line[0],
            line[2],
            line[3],
            line[6],
            line[7],
            line[8]
        ]

        rushingNewEntries.append(pd.Series(newEntry, index=rushingHeader))

    rushing_df = pd.DataFrame(rushingNewEntries)

    # Iterate over passing stats, add to DataFrame
    passingNewEntries = []
    for line in passingStats[1:]:
        line = line.replace(',', '')
        line = line.replace('-', ' ')
        line = line.split()
        newEntry = [
            line[1],
            line[0],
            line[2],
            line[4],
            line[5],
            line[8],
            line[9],
            line[6]
        ]

        passingNewEntries.append(pd.Series(newEntry, index=passingHeader))

    passing_df = pd.DataFrame(passingNewEntries)

    # Iterate over recieving stats, add to DataFrame
    recievingNewEntries = []
    for line in recievingStats[1:]:
        line = line.replace(',', '')
        line = line.replace('NaN', '0.0')
        line = line.split()
        newEntry = [
            line[1],
            line[0],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6]
        ]

        recievingNewEntries.append(pd.Series(newEntry, index=recievingHeader))

    recieving_df = pd.DataFrame(recievingNewEntries)

    semi_merged = pd.merge(rushing_df, passing_df, on=["first_name", "last_name", "gp"], how='outer')
    final_df = pd.merge(semi_merged, recieving_df, on=["first_name", "last_name", "gp"], how='outer')

    final_df.to_csv('src/raw_data/2023_stats/{}2023.csv'.format(team), index=False)

if __name__ == "__main__":
    main('Team')
