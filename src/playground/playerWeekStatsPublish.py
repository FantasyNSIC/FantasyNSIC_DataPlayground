from connection import connect_to_fantasyDB
import pandas as pd

def main(week_num, team_name):

    # Read in player stats from 2023 season
    with open(f'src/raw_data/weekly_stats/week{week_num}/{team_name}{week_num}.csv', 'r') as file:
        stats_df = pd.read_csv(file)
    
    # Connect to database
    conn = connect_to_fantasyDB()

    # Initialize cursor
    cur = conn.cursor()

    try: 
        # Iterate rows, grab player_ids
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
        stats_df['recieve_avg'] = stats_df['recieve_avg'].fillna(0).astype(float).round(1)
        stats_df['recieve_td'] = stats_df['recieve_td'].fillna(0).astype(int)
        stats_df['fg_att'] = 0
        stats_df['fg_made'] = 0

        print(stats_df)

        # Write DataFrame to database
        current_week = f'week_{week_num}'
        with open('src/queries/stats_insert_week.sql', 'r') as query:
            sql_temp = query.read()
        sql = sql_temp.format(current_week=current_week)
        for index, row in stats_df.iterrows():
            cur.execute("SELECT player_id FROM player_stats_week_%s WHERE player_id = %s", (week_num, row['player_id'],))
            if cur.fetchone() is not None:
                cur.execute(sql, (row['rush_att'], row['rush_yds'], row['rush_avg'], row['rush_td'],
                            row['pass_comp'], row['pass_att'], row['pass_yds'], row['pass_td'],
                            row['pass_int'], row['recieve_rec'], row['recieve_yds'], row['recieve_avg'],
                            row['recieve_td'], row['player_id']))
                print(f"Player added to weekly stats: {row['player_id']}")
            else:
                print(f"Player already in weekly stats: {row['player_id']}")

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
