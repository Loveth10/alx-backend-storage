-- This SQL script that ranks country origins of bands, ordered by 
-- nb_fans `metal_bands`
-- Your script can be executed on any database
SELECT origin, SUM(fans) AS nb_fans
    FROM metal_bands
    GROUP BY origin
    ORDER BY nb_fans DESC;

