import pandas as pd

def main(team, team_id):
    # Read text player info
    with open('src/raw_data/player_info/{}Players.txt'.format(team), 'r') as file:
        lines = file.readlines()

    # Define headers
    infoHeaders = [
        "first_name",
        "last_name",
        "team_id",
        "pos",
        "cls",
        "jersey_number",
        "height",
        "weight"
    ]

    # Iterate over text lines, add to DataFrame
    playerList = []
    for line in lines:
        line = line.replace('   ', ' ')
        line = line.split()
        newEntry = [
            line[1],
            line[2],
            team_id,
            line[3],
            line[6],
            line[0],
            line[4],
            line[5]
        ]
        playerList.append(pd.Series(newEntry, index=infoHeaders))

    playerDF = pd.DataFrame(playerList)

    # Iterate over rows, making changes as needed
    def format_row(row):
        row['first_name'] = row['first_name'].replace('?', ' ')
        row['last_name'] = row['last_name'].replace('?', ' ')
        row['pos'] = row['pos'].replace('/P', '')
        row['pos'] = row['pos'].replace('/WR', '')
        row['cls'] = row['cls'].replace('RFr.', 'Fr.')
        row['cls'] = row['cls'].replace('R-Fr.', 'Fr.')
        row['cls'] = row['cls'].replace('R-So.', 'So.')
        row['cls'] = row['cls'].replace('R-Jr.', 'Jr.')
        row['cls'] = row['cls'].replace('R-Sr.', 'Sr.')
        heightList = row['height'].split('-')
        row['height'] = "{}'{}″".format(heightList[0], heightList[1])
        return row

    playerDF = playerDF.apply(format_row, axis=1)

    # Define filter position values
    positions = {'QB', 'RB', 'WR', 'TE', 'K'}

    # Filter out rows where pos is not in positions
    playerDF = playerDF[playerDF['pos'].isin(positions)]

    playerDF.to_csv('src/raw_data/player_info/{}Players.csv'.format(team), index=False)

if __name__ == "__main__":
    main('Team', 0)
