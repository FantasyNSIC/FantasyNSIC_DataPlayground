from connection import connect_to_fantasyDB

def update_user_weekly_points(week_num):

    # Connect to database
    conn = connect_to_fantasyDB()
    cur = conn.cursor()

    try:
        # grab all user_team_ids
        cur.execute("""
            SELECT user_team_id
            FROM user_team
            """)
        user_team_ids = cur.fetchall()

        # grab all roster players
        cur.execute("""
            SELECT user_team_id, player_id
            FROM team_roster
            WHERE status = 'active'
            """)
        roster_res = cur.fetchall()

        # iterate over all user_team_ids and enter weekly points
        for user_team_id in user_team_ids:
            id = user_team_id[0]
            points = 0

            # filter players by user_team_id
            user_players = [player for player in roster_res if player[0] == id]

            # iterate over players, filter by user_team_id
            for player in user_players:
                cur.execute("""
                    SELECT week_{week_num}
                    FROM player_points_scored
                    WHERE player_id = %s
                    """.format(week_num=week_num), (player[1],))
                player_points = cur.fetchone()

                if player_points is not None:
                    points += player_points[0]

            # insert weekly points into user_points_scored
            cur.execute("""
                UPDATE user_points_scored
                SET week_{week_num} = %s,
                    total_points = total_points + %s
                WHERE user_team_id = %s
                """.format(week_num=week_num), (points, points, id))
            print(f"Updated user_team_id: {id} with {points} points")
            
        conn.commit()

    except Exception as e:
        print(e)
        conn.close()
        cur.close()

    conn.close()
    cur.close()

if __name__ == "__main__":
    update_user_weekly_points(1)
