
    SELECT 
        MAKER_SID, 
        CHECKER_SID, 
        COUNT(*) AS TotalRecords,
        SUM(CASE WHEN MAKER_ANSWER IS NOT NULL THEN 1 ELSE 0 END) AS MakerAnswered,
        SUM(CASE WHEN CHECKER_ANSWER IS NOT NULL THEN 1 ELSE 0 END) AS CheckerAnswered
    FROM 
        TBL_AUDIT
    WHERE PIPE_ID = 1
    GROUP BY 
        MAKER_SID, 
        CHECKER_SID
