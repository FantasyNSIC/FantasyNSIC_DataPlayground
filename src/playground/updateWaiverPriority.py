from connection import connect_to_fantasyDB
import json

def update_waiver_priority(league_id):
    
    # Connect to database
    conn = connect_to_fantasyDB()
    cur = conn.cursor()

    try:
        # Grab all user records by league.
        cur.execute("""
            SELECT team_records.*
            FROM team_records
            JOIN user_team ON team_records.user_team_id = user_team.user_team_id
            WHERE user_team.league_id = %s
            """, (league_id,))
        results = cur.fetchall()

        # Sort records by fewest losses, then by wins, then by points scored
        sorted_records = sorted(results, key=lambda x: (x[2], -x[1], -x[3]))

        # Create JSON and update waiver priority.
        new_priority = [{"priority": i, "user_team_id": record[0]} for i, record in enumerate(sorted_records, start=1)]
        priority_json = json.dumps(new_priority)
        
        # Store new waiver priority in database
        cur.execute("""
            UPDATE waiver_wire_priority
            SET waiver_order = %s
            WHERE league_id = %s
            """, (priority_json, league_id))
        
        conn.commit()
        print("Updated waiver priority for league_id: ", league_id)

    except Exception as e:
        print(e)
        conn.close()
        cur.close()

    conn.close()
    cur.close()

if __name__ == "__main__":
    update_waiver_priority(12345)
