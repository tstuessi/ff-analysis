-- Let's take a look at creating some targets
DROP TABLE FULL_YEAR_DATA_MART_2014;
CREATE TABLE FULL_YEAR_DATA_MART_2014 as 
SELECT
    p.playerid
    ,p.name
    ,p.position
    ,p.team
    ,team_stats.QB
    ,team_stats.RB
    ,team_stats.WR
    ,team_stats.TE
    ,team_stats.K
    ,team_stats.C 
    ,team_stats.DB 
    ,team_stats.DE 
    ,team_stats.DT 
    ,team_stats.FB
    ,team_stats.LB 
    ,team_stats.LS 
    ,team_stats.NT 
    ,team_stats.OG
    ,team_stats.OT 
    ,team_stats.P 
    ,CASE WHEN SUM(rushing_att) != 0
        THEN 
            SUM(rushing_yds) / SUM(rushing_att)
        ELSE 0 
        END as 'ypc'
    ,CASE WHEN SUM(passing_att) != 0
        THEN
            SUM(passing_cmp) / SUM(passing_att)
        ELSE 0
        END as 'pass_cmp_ratio'
    ,CASE WHEN SUM(receiving_rec) != 0
        THEN 
            SUM(receiving_yds) / SUM(receiving_rec)
        ELSE 0
        END as 'ypr'
    ,CASE WHEN SUM(passing_att) != 0
        THEN
            (((((SUM(passing_cmp) / SUM(passing_att)) - .3) * 5) +
            (((SUM(passing_yds) / SUM(passing_att)) -  3) * .25) +
            (((SUM(passing_tds) / SUM(passing_att))) * 20) +
            (2.375 - ((SUM(passing_ints) / SUM(passing_att)) * 25))) / 6) * 100
        ELSE 0
        END as 'passer_rating'
    ,SUM(defense_ast) as 'defense_ast'
    ,SUM(defense_ffum) as 'defense_ffum'
    ,SUM(defense_int) as 'defense_int'
    ,SUM(defense_sk) as 'defense_sk'
    ,SUM(defense_tkl) as 'defense_tkl'
    ,SUM(fumbles_lost) as 'fumbles_lost'
    ,SUM(fumbles_rcv) as 'fumbles_rcv'
    ,SUM(fumbles_tot) as 'fumbles_tot'
    ,SUM(fumbles_trcv) as 'fumbles_trcv'
    ,SUM(fumbles_yds) as 'fumbles_yds'
    ,SUM(kicking_fga) as 'kicking_fga'
    ,SUM(kicking_fgm) as 'kicking_fgm'
    ,SUM(kicking_fgyds) as 'kicking_fgyds'
    ,SUM(kicking_totpfg) as 'kicking_totpfg'
    ,SUM(kicking_xpa) as 'kicking_xpa'
    ,SUM(kicking_xpb) as 'kicking_xpb'
    ,SUM(kicking_xpmade) as 'kicking_xpmade'
    ,SUM(kicking_xpmissed) as 'kicking_xpmissed'
    ,SUM(kicking_xptot) as 'kicking_xptot'
    ,SUM(kickret_avg) as 'kickret_avg'
    ,SUM(kickret_lng) as 'kickret_lng'
    ,SUM(kickret_lngtd) as 'kickret_lngtd'
    ,SUM(kickret_ret) as 'kickret_ret'
    ,SUM(kickret_tds) as 'kickret_tds'
    ,SUM(passing_att) as 'passing_att'
    ,SUM(passing_cmp) as 'passing_cmp'
    ,SUM(passing_ints) as 'passing_ints'
    ,SUM(passing_tds) as 'passing_tds'
    ,SUM(passing_twopta) as 'passing_twopta'
    ,SUM(passing_twoptm) as 'passing_twoptm'
    ,SUM(passing_yds) as 'passing_yds'
    ,SUM(punting_avg) as 'punting_avg'
    ,SUM(punting_i20) as 'punting_i20'
    ,SUM(punting_lng) as 'punting_lng'
    ,SUM(punting_pts) as 'punting_pts'
    ,SUM(punting_yds) as 'punting_yds'
    ,SUM(puntret_avg) as 'puntret_avg'
    ,SUM(puntret_lng) as 'puntret_lng'
    ,SUM(puntret_lngtd) as 'puntret_lngtd'
    ,SUM(puntret_ret) as 'puntret_ret'
    ,SUM(puntret_tds) as 'puntret_tds'
    ,SUM(receiving_lng) as 'receiving_lng'
    ,SUM(receiving_lngtd) as 'receiving_lngtd'
    ,SUM(receiving_rec) as 'receiving_rec'
    ,SUM(receiving_tds) as 'receiving_tds'
    ,SUM(receiving_twopta) as 'receiving_twopta'
    ,SUM(receiving_twoptm) as 'receiving_twoptm'
    ,SUM(receiving_yds) as 'receiving_yds'
    ,SUM(rushing_att) as 'rushing_att'
    ,SUM(rushing_lng) as 'rushing_lng'
    ,SUM(rushing_lngtd) as 'rushing_lngtd'
    ,SUM(rushing_tds) as 'rushing_tds'
    ,SUM(rushing_twopta) as 'rushing_twopta'
    ,SUM(rushing_twoptm) as 'rushing_twoptm'
    ,SUM(rushing_yds) as 'rushing_yds'
FROM   
    PLAYER_WEEKLY_STATS_YEAR_2014 as p
INNER JOIN TEAM_POSITION_STATS_2014 as team_stats 
ON
    p.team = team_stats.team 
GROUP BY 
    p.playerid, p.name;