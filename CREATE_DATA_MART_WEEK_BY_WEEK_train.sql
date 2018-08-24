-- training set -- 2014, target 2015 week by week scores
SELECT 
    -- SETUP PREDICTION INFO
    --p_2014.playerid -- covered in fypt
    sched_2015.week
    --,p_2014.team -- covered in fypt
    ,CASE 
        WHEN sched_2015.week = 1 THEN cbs_2015.WEEK_1
        WHEN sched_2015.week = 2 THEN cbs_2015.WEEK_2
        WHEN sched_2015.week = 3 THEN cbs_2015.WEEK_3
        WHEN sched_2015.week = 4 THEN cbs_2015.WEEK_4
        WHEN sched_2015.week = 5 THEN cbs_2015.WEEK_5 
        WHEN sched_2015.week = 6 THEN cbs_2015.WEEK_6 
        WHEN sched_2015.week = 7 THEN cbs_2015.WEEK_7
        WHEN sched_2015.week = 8 THEN cbs_2015.WEEK_8
        WHEN sched_2015.week = 9 THEN cbs_2015.WEEK_9
        WHEN sched_2015.week = 10 THEN cbs_2015.WEEK_10
        WHEN sched_2015.week = 11 THEN cbs_2015.WEEK_11
        WHEN sched_2015.week = 12 THEN cbs_2015.WEEK_12
        WHEN sched_2015.week = 13 THEN cbs_2015.WEEK_13
        WHEN sched_2015.week = 14 THEN cbs_2015.WEEK_14
        WHEN sched_2015.week = 15 THEN cbs_2015.WEEK_15 
        WHEN sched_2015.week = 16 THEN cbs_2015.WEEK_16 
        WHEN sched_2015.week = 17 THEN cbs_2015.WEEK_17
    END as 'target'

    ,sched_2015.opp
    ,sched_2015.is_home
    ,sched_2015.month
    ,sched_2015.wday

    --PREVIOUS YEAR FEATURES
    ,fypt_2014.*
    ,tps_2014.*


    -- Previous meeting performance
    ,prev_meeting_stats.defense_ast
    ,prev_meeting_stats.defense_ffum
    ,prev_meeting_stats.defense_int
    ,prev_meeting_stats.defense_sk
    ,prev_meeting_stats.defense_tkl
    ,prev_meeting_stats.fumbles_lost
    ,prev_meeting_stats.fumbles_rcv
    ,prev_meeting_stats.fumbles_tot
    ,prev_meeting_stats.fumblestrcv
    ,prev_meeting_stats.fumbles_yds
    ,prev_meeting_stats.kicking_fga
    ,prev_meeting_stats.kicking_fgm
    ,prev_meeting_stats.kicking_fgyds
    ,prev_meeting_stats.kicking_totpfg
    ,prev_meeting_stats.kicking_xpa
    ,prev_meeting_stats.kicking_xpb
    ,prev_meeting_stats.kicking_xpmade
    ,prev_meeting_stats.kicking_xpmissed
    ,prev_meeting_stats.kicking_xptot
    ,prev_meeting_stats.kickret_avg
    ,prev_meeting_stats.kickret_lng
    ,prev_meeting_stats.kickret_lngtd
    ,prev_meeting_stats.kickret_ret
    ,prev_meeting_stats.kickret_tds
    ,prev_meeting_stats.punting_avg
    ,prev_meeting_stats.punting_i20
    ,prev_meeting_stats.punting_lng
    ,prev_meeting_stats.punting_pts
    ,prev_meeting_stats.punting_yds
    ,prev_meeting_stats.puntret_avg
    ,prev_meeting_stats.puntret_lng
    ,prev_meeting_stats.puntret_lngtd
    ,prev_meeting_stats.puntret_ret
    ,prev_meeting_stats.puntret_tds
    ,prev_meeting_stats.receiving_lng
    ,prev_meeting_stats.receiving_lngtd
    ,prev_meeting_stats.receiving_rec
    ,prev_meeting_stats.receiving_tds
    ,prev_meeting_stats.receiving_twopta
    ,prev_meeting_stats.receiving_twoptm
    ,prev_meeting_stats.receiving_yds
    ,prev_meeting_stats.rushing_att
    ,prev_meeting_stats.rushing_lng
    ,prev_meeting_stats.rushing_lngtd
    ,prev_meeting_stats.rushing_tds
    ,prev_meeting_stats.rushing_twopta
    ,prev_meeting_stats.rushing_twoptm
    ,prev_meeting_stats.rushing_yds
    ,prev_meeting_stats.passing_att
    ,prev_meeting_stats.passing_cmp
    ,prev_meeting_stats.passing_ints
    ,prev_meeting_stats.passing_tds
    ,prev_meeting_stats.passing_twopta
    ,prev_meeting_stats.passing_twoptm
    ,prev_meeting_stats.passing_yds

        
FROM CBS_YEAR_2015 as cbs_2015

-- SETUP TABLES
INNER JOIN PLAYER_WEEKLY_STATS_YEAR_2014 as p_2014
ON
    p_2014.playerid = cbs_2015.playerid
INNER JOIN SCHED_YEAR_2015 as sched_2015
ON
    p_2014.team = sched_2015.team
    AND sched_2015.week = sched_2015.week

-- PREVIOUS YEAR FEATURES
LEFT OUTER JOIN FULL_YEAR_PLAYER_AND_TEAM_STATS_2014 as fypt_2014 
ON
    fypt_2014.playerid = cbs_2015.playerid
LEFT OUTER JOIN TEAM_POSITION_STATS_2014 as tps_2014 
ON
    tps_2014.team = sched_2015.opp

    -- make sure the recent team changes doesn't affect this


-- PREVIOUS MEETING
LEFT OUTER JOIN SCHED_YEAR_2014 as prev_meeting_sched
ON
    prev_meeting_sched.team = p_2014.team 
    AND prev_meeting_sched.opp = sched_2015.opp
    AND prev_meeting_sched.week = (SELECT MAX(week) FROM SCHED_YEAR_2014 
                            WHERE team = p_2014.team and opp = sched_2015.opp)
LEFT OUTER JOIN PLAYER_WEEKLY_STATS_2014 as prev_meeting_stats
ON
    prev_meeting_stats.week = prev_meeting_sched.week
    AND p_2014.playerid = prev_meeting_stats.playerid
