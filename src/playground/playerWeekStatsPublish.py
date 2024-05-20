from connection import connect_to_fantasyDB
import pandas as pd

def main(week_num, team_name):

    # Read in player stats from 2023 season
    with open(f'src/raw_data/2023_stats/week{week_num}/{team_name}{week_num}.csv', 'r') as file:
        stats_df = pd.read_csv(file)
    
    # Connect to database
    conn = connect_to_fantasyDB()

    # Initialize cursor
    cur = conn.cursor()

    try: 
        # Iterate rows, grab player_is
        for index, row in stats_df.iterrows():
            cur.execute("""
                SELECT player_id 
                FROM nsic_players 
                WHERE REPLACE(first_name, ' ', '') = %s 
                AND REPLACE(last_name, ' ', '') = %s
            """, (row['first_name'].replace(' ', ''), row['last_name'].replace(' ', '')))
            result = cur.fetchone()
            if result is None:
                print(f"Player not found: {row['first_name']} {row['last_name']}")
            else:
                player_id = result[0]
                stats_df.at[index, 'player_id'] = player_id

        # Move player_id column to front
        player_id = stats_df.pop('player_id')
        stats_df.insert(0, 'player_id', player_id)

        # Filter out rows where player_id is NaN
        stats_df = stats_df.dropna(subset=['player_id'])

        # Convert rows to integers/floats, add kicking, drop names
        stats_df['player_id'] = stats_df['player_id'].astype(int)
        stats_df.drop(columns=['first_name', 'last_name'], inplace=True)
        stats_df['rush_att'] = stats_df['rush_att'].fillna(0).astype(int)
        stats_df['rush_yds'] = stats_df['rush_yds'].fillna(0).astype(int)
        stats_df['rush_avg'] = stats_df['rush_avg'].fillna(0).astype(float).round(1)
        stats_df['rush_td'] = stats_df['rush_td'].fillna(0).astype(int)
        stats_df['pass_comp'] = stats_df['pass_comp'].fillna(0).astype(int)
        stats_df['pass_att'] = stats_df['pass_att'].fillna(0).astype(int)
        stats_df['pass_yds'] = stats_df['pass_yds'].fillna(0).astype(int)
        stats_df['pass_td'] = stats_df['pass_td'].fillna(0).astype(int)
        stats_df['pass_int'] = stats_df['pass_int'].fillna(0).astype(int)
        stats_df['recieve_rec'] = stats_df['recieve_rec'].fillna(0).astype(int)
        stats_df['recieve_yds'] = stats_df['recieve_yds'].fillna(0).astype(int)
        stats_df['recieve_td'] = stats_df['recieve_td'].fillna(0).astype(int)

        print(stats_df)

        # Write DataFrame to database
        # TODO: Will have to change this writing to database to account for the new table structure
        with open('src/queries/stats_insert_week.sql', 'r') as query:
            sql = query.read()
        for index, row in stats_df.iterrows():
            cur.execute("SELECT player_id FROM player_stats_2023 WHERE player_id = %s", (row['player_id'],))
            if cur.fetchone() is None:
                cur.execute(sql, tuple(row))
            else:
                print(f"Player already in database: {row['player_id']}")

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
    main(1, "Augustana")
