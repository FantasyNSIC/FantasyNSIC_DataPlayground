INSERT INTO player_stats_2023 (
    player_id,
    rush_att,
    rush_yds,
    rush_avg,
    rush_td,
    pass_comp,
    pass_att,
    pass_yds,
    pass_td,
    pass_int,
    recieve_rec,
    recieve_yds,
    recieve_td)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s);