UPDATE team_records
SET wins = wins + 1,
    points_for = points_for + %s
    points_against = points_against + %s
WHERE user_team_id = %s;