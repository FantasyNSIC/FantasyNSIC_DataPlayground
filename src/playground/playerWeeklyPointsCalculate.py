from connection import connect_to_fantasyDB

def calculate_player_weekly_points(week_num):

    # Connect to database
    conn = connect_to_fantasyDB()
    cur = conn.cursor()

    try:
        # Grab player stats from database
        cur.execute("""
            SELECT player_id, rush_yds, rush_td, pass_yds, pass_td, pass_int, recieve_rec, recieve_yds, recieve_td, fg_made
            FROM player_stats_week_{week_num}""".format(week_num=week_num))

        results = cur.fetchall()

        # Iterate over results, calculate points
        for result in results:
            player_id = result[0]
            rush_yds = result[1]
            rush_td = result[2]
            pass_yds = result[3]
            pass_td = result[4]
            pass_int = result[5]
            recieve_rec = result[6]
            recieve_yds = result[7]
            recieve_td = result[8]
            fg_made = result[9]

            # Calculate points
            rush_points = (rush_yds * 0.1) + (rush_td * 6)
            pass_points = (pass_yds * 0.03) + (pass_td * 4) + (pass_int * -2)
            recieve_points = recieve_rec + (recieve_yds * 0.1) + (recieve_td * 6)
            kicking_points = fg_made * 3

            total_points = rush_points + pass_points + recieve_points + kicking_points

            # Update player stats in database
            cur.execute("""
                UPDATE player_points_scored
                SET week_{week_num} = %s,
                    total_points = total_points + %s
                WHERE player_id = %s
            """.format(week_num=week_num), (total_points, total_points, player_id))

            print(f"Player {player_id} weekly points updated")

        conn.commit()
        print("Player weekly points calculated and updated in database!")

    except Exception as e:
        print(e)
        conn.close()
        cur.close()

    conn.close()
    cur.close()

if __name__ == "__main__":
    calculate_player_weekly_points(1)
