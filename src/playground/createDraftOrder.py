from connection import connect_to_fantasyDB

def create_draft_order(start, league_id, teams, reverse = False):

    try:
        # Connect to database
        conn = connect_to_fantasyDB()

        # Initialize cursor
        cur = conn.cursor()

        if reverse:
            teams = teams[::-1]

        # Create draft order
        for team in teams:
            cur.execute("""
                INSERT INTO draft_order (draft_pick, league_id, user_team_id)
                VALUES (%s, %s, %s)
            """, (start, league_id, team))
            start += 1

        conn.commit()
    
    except Exception as e:
        print(e)
        conn.close()
        cur.close()
        return
    
    conn.close()
    cur.close()
    print("Successfully created draft order")

if __name__ == "__main__":
    create_draft_order(131, 56507, [816690, 328761, 638674, 762943, 800833, 86431, 544377, 719632, 917456, 207140], True)
