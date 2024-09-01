from connection import connect_to_fantasyDB
import json

def create_user_team_history(league_id, week_num):

    try:
        # Connect to database
        conn = connect_to_fantasyDB()

        # Initialize cursor
        cur = conn.cursor()

        # Get all user teams in league
        cur.execute("""
            SELECT user_team_id
            FROM user_team
            WHERE league_id = %s
        """, (league_id,))

        user_teams = cur.fetchall()

        # Fetch rosters for each user team and store in json format
        for user_team in user_teams:
            cur.execute("""
                SELECT player_id, status
                FROM team_roster
                WHERE user_team_id = %s
            """, (user_team[0],))

            roster = cur.fetchall()
            roster_list = [{"player_id": player[0], "status": player[1]} for player in roster]
            roster_json = json.dumps(roster_list)

            # Insert roster into user_roster_history
            cur.execute("""
                UPDATE user_roster_history
                    SET week_%s = %s
                WHERE user_team_id = %s
            """, (week_num, roster_json, user_team[0]))

        conn.commit()
    
    except Exception as e:
        print(e)
        conn.close()
        cur.close()
        return
    
    conn.close()
    cur.close()
    print("Successfully created user team history")

if __name__ == "__main__":
    create_user_team_history(00000, 1)
