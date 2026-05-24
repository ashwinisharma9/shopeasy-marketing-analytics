SELECT
    *
FROM dbo.customers

SELECT
    *
FROM dbo.geography

-- SQL statement to join dim_customers with dim_geography
-- to enrich customer data with geographic information

SELECT
    c.CustomerID,      -- Selects the unique identifier for each customer
    c.CustomerName,    -- Selects the name of each customer
    c.Email,           -- Selects the email of each customer
    c.Gender,          -- Selects the gender of each customer
    c.Age,             -- Selects the age of each customer
    g.Country,         -- Selects the country from the geography table
    g.City             -- Selects the city from the geography table

FROM
    dbo.customers AS c     -- Alias 'c' for customers table

LEFT JOIN
-- RIGHT JOIN
-- INNER JOIN
-- FULL OUTER JOIN
    dbo.geography g        -- Alias 'g' for geography table

ON
    c.GeographyID = g.GeographyID;