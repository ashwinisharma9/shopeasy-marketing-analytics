SELECT 
*
FROM dbo.customer_journey

-- Common Table Expression (CTE) to identify and tag duplicate records

WITH DuplicateRecords AS (

    SELECT
        JourneyID,   
        CustomerID,  
        ProductID,   
        VisitDate,   
        Stage,       
        Action,      
        Duration,

        -- Assign row numbers to duplicate groups
        ROW_NUMBER() OVER (

            PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action
            ORDER BY JourneyID

        ) AS row_num

    FROM dbo.customer_journey

)

-- Show duplicate records
SELECT *
FROM DuplicateRecords
WHERE row_num > 1
ORDER BY JourneyID;