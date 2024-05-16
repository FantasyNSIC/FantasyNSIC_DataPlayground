import pandas as pd

def main():
    # Read text player info
    with open('src/raw_data/player_info/examplePlayers.txt', 'r') as file:
        lines = file.readlines()

    # Define team ID for extracted players
    team_id = 0

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
        row['cls'] = row['cls'].replace('RFr.', 'Fr.')
        heightList = row['height'].split('-')
        row['height'] = "{}'{}″".format(heightList[0], heightList[1])
        return row

    playerDF = playerDF.apply(format_row, axis=1)

    # Define filter position values
    positions = {'QB', 'RB', 'WR', 'K'}

    # Filter out rows where pos is not in positions
    playerDF = playerDF[playerDF['pos'].isin(positions)]

    playerDF.to_csv('src/raw_data/player_info/examplePlayers.csv', index=False)

if __name__ == "__main__":
    main()
