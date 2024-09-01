import pandas as pd
import numpy as np
import re

def main(week_num, team_name):
    # Read the file
    with open(f'src/raw_data/weekly_stats/week{week_num}/{team_name}{week_num}.txt', 'r') as file:
        lines = re.split(r'\n\n', file.read())

    # Initialize Header Lists
    rushingHeader = [
        "first_name",
        "last_name",
        "rush_att",
        "rush_yds",
        "rush_avg",
        "rush_td",
    ]

    passingHeader = [
        "first_name",
        "last_name",
        "pass_comp",
        "pass_att",
        "pass_yds",
        "pass_td",
        "pass_int",
    ]

    recievingHeader = [
        "first_name",
        "last_name",
        "recieve_rec",
        "recieve_yds",
        "recieve_avg",  # "recieve_avg" is not in the data, so it is not included in the header.
        "recieve_td",
    ]

    # Seperate sections in respective lists.
    rushingStats = lines[0].split('\n')
    passingStats = lines[1].split('\n')
    recievingStats = lines[2].split('\n')

    # Iterate over rushing stats, add to DataFrame
    rushingNewEntries = []
    for line in rushingStats[1:]:
        line = line.replace(',', ' ')
        line = line.split()
        newEntry = [
            line[1],    # first_name
            line[0],    # last_name
            line[2],    # rush_att
            line[5],    # rush_yds
            line[8],    # rush_avg
            line[6]     # rush_td
        ]

        rushingNewEntries.append(pd.Series(newEntry, index=rushingHeader))

    rushing_df = pd.DataFrame(rushingNewEntries)

    # Iterate over passing stats, add to DataFrame
    passingNewEntries = []
    for line in passingStats[1:]:
        line = line.replace(',', ' ')
        line = line.replace('-', ' ')
        line = line.split()
        newEntry = [
            line[1],    # first_name
            line[0],    # last_name
            line[2],    # pass_comp
            line[3],    # pass_att
            line[4],    # pass_yds
            line[5],    # pass_td
            line[6]     # pass_int
        ]

        passingNewEntries.append(pd.Series(newEntry, index=passingHeader))

    passing_df = pd.DataFrame(passingNewEntries)

    # Iterate over recieving stats, add to DataFrame
    recievingNewEntries = []
    for line in recievingStats[1:]:
        line = line.replace(',', ' ')
        line = line.replace('NaN', '0.0')
        line = line.split()
        # Calculate recieve_avg
        recieve_avg = 0.0
        if int(line[2]) != 0:
            recieve_avg = round(float(line[3]) / int(line[2]), 1)
        newEntry = [
            line[1],    # first_name
            line[0],    # last_name
            line[2],    # recieve_rec
            line[3],    # recieve_yds
            str(recieve_avg),    # recieve_avg (calculated from recieve_yds/recieve_rec)
            line[4]     # recieve_td
        ]

        recievingNewEntries.append(pd.Series(newEntry, index=recievingHeader))

    recieving_df = pd.DataFrame(recievingNewEntries)

    semi_merged = pd.merge(rushing_df, passing_df, on=["first_name", "last_name"], how='outer')
    final_df = pd.merge(semi_merged, recieving_df, on=["first_name", "last_name"], how='outer')

    final_df.to_csv(f'src/raw_data/weekly_stats/week{week_num}/{team_name}{week_num}.csv', index=False)

if __name__ == "__main__":
    main(1, 'Augustana')
