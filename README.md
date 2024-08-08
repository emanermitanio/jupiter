WITH TotalCounts AS (
    SELECT 
        REVIEWTYPE, 
        MAKER_SID, 
        CHECKER_SID, 
        COUNT(*) AS TotalRecords
    FROM 
        your_table
    GROUP BY 
        REVIEWTYPE, 
        MAKER_SID, 
        CHECKER_SID
),
AnsweredCounts AS (
    SELECT 
        REVIEWTYPE, 
        MAKER_SID, 
        CHECKER_SID, 
        SUM(CASE WHEN MAKER_ANSWER IS NOT NULL AND MAKER_ANSWER != 'None' THEN 1 ELSE 0 END) AS MakerAnswered,
        SUM(CASE WHEN CHECKER_ANSWER IS NOT NULL AND CHECKER_ANSWER != 'None' THEN 1 ELSE 0 END) AS CheckerAnswered
    FROM 
        your_table
    GROUP BY 
        REVIEWTYPE, 
        MAKER_SID, 
        CHECKER_SID
)
SELECT 
    t.REVIEWTYPE, 
    t.MAKER_SID, 
    printf("%.0f%%", (a.MakerAnswered * 100.0) / t.TotalRecords) AS MAKER_COMPLETION,
    t.CHECKER_SID, 
    printf("%.0f%%", (a.CheckerAnswered * 100.0) / t.TotalRecords) AS CHECKER_COMPLETION
FROM 
    TotalCounts t
JOIN 
    AnsweredCounts a ON t.REVIEWTYPE = a.REVIEWTYPE 
                     AND t.MAKER_SID = a.MAKER_SID 
                     AND t.CHECKER_SID = a.CHECKER_SID;
