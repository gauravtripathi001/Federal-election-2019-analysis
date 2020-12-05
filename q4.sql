SELECT winning, 
       Count(winning) AS value_occurrence 
FROM   (SELECT v.riding_number, 
               CASE 
                 WHEN m.maxcol = v.conservative_vote_share THEN 'conservative' 
                 WHEN m.maxcol = v.liberal_vote_share THEN 'liberal' 
                 WHEN m.maxcol = v.ndp_vote_share THEN 'NDP' 
                 WHEN m.maxcol = v.green_vote_share THEN 'green' 
                 WHEN m.maxcol = v.bloc_quebecois_vote_share THEN 'bloc_quebecois' 
                 WHEN m.maxcol = v.peoples_party_vote_share THEN 'peoples_party' 
               end AS winning 
        FROM   vote_share AS v 
               JOIN (SELECT riding_number, 
                            Max(colname) AS maxcol 
                     FROM   (SELECT riding_number, 
                                    conservative_vote_share AS colName, 
                                    conservative_vote_share AS value 
                             FROM   vote_share 
                             UNION ALL 
                             SELECT riding_number, 
                                    liberal_vote_share AS colName, 
                                    liberal_vote_share AS value 
                             FROM   vote_share 
                             UNION ALL 
                             SELECT riding_number, 
                                    ndp_vote_share AS colName, 
                                    ndp_vote_share AS value 
                             FROM   vote_share 
                             UNION ALL 
                             SELECT riding_number, 
                                    green_vote_share AS colName, 
                                    green_vote_share AS value 
                             FROM   vote_share 
                             UNION ALL 
                             SELECT riding_number, 
                                    bloc_quebecois_vote_share AS colName, 
                                    bloc_quebecois_vote_share AS value 
                             FROM   vote_share 
                             UNION ALL 
                             SELECT riding_number, 
                                    peoples_party_vote_share AS colName, 
                                    peoples_party_vote_share AS value 
                             FROM   vote_share) AS subquery 
                     GROUP  BY subquery.riding_number 
                     ORDER  BY subquery.riding_number) AS m 
                 ON v.riding_number = m.riding_number) AS result 
GROUP  BY winning 
ORDER  BY value_occurrence 
LIMIT  1; 