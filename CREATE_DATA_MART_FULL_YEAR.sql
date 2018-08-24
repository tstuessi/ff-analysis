-- Let's take a look at creating some targets
SELECT
    p.*
    ,cbs.total as 'target'
    ,CASE WHEN rushing_att != 0
        THEN 
            rushing_yds / rushing_att
        ELSE 0 
        END as 'ypc'
    ,CASE WHEN passing_att != 0
        THEN
            passing_cmp / passing_att
        ELSE 0
        END as 'pass_cmp_ratio'
    ,CASE WHEN receiving_rec != 0
        THEN 
            receiving_yds / receiving_rec
        ELSE 0
        END as 'ypr'
    ,CASE WHEN passing_att != 0
        THEN
            (((((passing_cmp / passing_att) - .3) * 5) +
            (((passing_yds / passing_att) -  3) * .25) +
            (((passing_tds / passing_att) * 20)) +
            (2.375 - ((passing_ints / passing_att) * 25)) / 6) * 100)
        ELSE 0
        END as 'passer_rating'
FROM   
    FULL_YEAR_PLAYER_AND_TEAM_STATS_2015 as p
INNER JOIN CBS_YEAR_2016 as cbs
ON 
    cbs.playerid = p.playerid
GROUP BY 
    p.playerid, cbs.total;