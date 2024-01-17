-- Script that summats the fans of origin
-- Of origin and fans column

SELECT origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
