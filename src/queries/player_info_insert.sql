INSERT INTO nsic_players (
    player_id,
    first_name,
    last_name,
    team_id,
    pos,
    cls,
    jersey_number,
    height,
    weight)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    );