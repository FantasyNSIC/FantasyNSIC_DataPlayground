from connection import connect_to_fantasyDB
import pandas as pd

def main():
    
    # Read in new player info
    with open('src/raw_data/player_info/examplePlayers.csv', 'r') as file:
        player_info_df = pd.read_csv(file)

    # Connect to database
    conn = connect_to_fantasyDB()

    # Initialize cursor
    cur = conn.cursor()

    try:
        # Determine if player exists in db
        for index, row in player_info_df.iterrows():
            cur.execute("""
                SELECT player_id 
                FROM nsic_players 
                WHERE first_name = %s 
                AND last_name = %s
            """, (row['first_name'], row['last_name']))
            result = cur.fetchone()
            if result is not None:
                print(f"Player already exists: {row['first_name']} {row['last_name']}")
                player_info_df.drop(index, inplace=True)

        # Grab largest player_id in db
        cur.execute("""
            SELECT MAX(player_id) 
            FROM nsic_players
        """)
        result = cur.fetchone()
        if result is None:
            player_id = 1
        else:
            player_id = result[0] + 1

        # iterate rows, insert new ids
        for index, row in player_info_df.iterrows():
            player_info_df.at[index, 'player_id'] = player_id
            player_id += 1

        # Move player_id column to front
        player_id = player_info_df.pop('player_id')
        player_info_df.insert(0, 'player_id', player_id)

        player_info_df['player_id'] = player_info_df['player_id'].astype(int)

        # Insert new players into db
        with open('src/queries/player_info_insert.sql', 'r') as file:
            sql = file.read()
        for row in player_info_df.itertuples(index=False):
            cur.execute(sql, row)

        conn.commit()

        print("Successfully wrote to database")
    
    except Exception as e:
        print(e)
        conn.close()
        cur.close()

    # Close connections
    conn.close()
    cur.close()
    print("Connection closed")

if __name__ == '__main__':
    main()
