UPDATE player_stats_{current_week}
SET 
    rush_att = %s,
    rush_yds = %s,
    rush_avg = %s,
    rush_td = %s,
    pass_comp = %s,
    pass_att = %s,
    pass_yds = %s,
    pass_td = %s,
    pass_int = %s,
    recieve_rec = %s,
    recieve_yds = %s,
    recieve_avg = %s,
    recieve_td = %s
WHERE player_id = %s;