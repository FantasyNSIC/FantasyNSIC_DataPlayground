from connection import connect_to_fantasyDB

def update_user_records(week_num):

    # Connect to database
    conn = connect_to_fantasyDB()
    cur = conn.cursor()

    with open('src/queries/increase_user_record_wins.sql', 'r') as query:
        win_sql = query.read()
    with open('src/queries/increase_user_record_losses.sql', 'r') as query:
        loss_sql = query.read()

    try:
        # Grab all matchups for that week.
        cur.execute("""
            SELECT league_id, user_team_id, week_{week_num}
            FROM user_team_matchups
            """.format(week_num=week_num))
        results = cur.fetchall()

        # Filter out duplicate matchups
        matchups = []
        for res in results:
            if res[1] != any(match[2] for match in matchups):
                matchups.append(res)

        # Iterate over matchups, update user records
        for matchup in matchups:
            team_1_id = matchup[1]
            team_2_id = matchup[2]

            # Grab points scored for that week
            # team_1
            cur.execute("""
                SELECT week_{week_num}
                FROM user_points_scored
                WHERE user_team_id = %s
            """.format(week_num=week_num), (team_1_id,))
            team_1_points = cur.fetchone()[0]

            # team_2
            cur.execute("""
                SELECT week_{week_num}
                FROM user_points_scored
                WHERE user_team_id = %s
            """.format(week_num=week_num), (team_2_id,))
            team_2_points = cur.fetchone()[0]

            # Determine winner and set records
            if team_1_points > team_2_points:
                cur.execute(win_sql, (team_1_id,))
                cur.execute(loss_sql, (team_2_id,))
            elif team_2_points > team_1_points:
                cur.execute(win_sql, (team_2_id,))
                cur.execute(loss_sql, (team_1_id,))
            else:
                print("Tie game")

        conn.commit()

    except Exception as e:
        print(e)
        conn.close()
        cur.close()

    conn.close()
    cur.close()

if __name__ == "__main__":
    update_user_records(1)
