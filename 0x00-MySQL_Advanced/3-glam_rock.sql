-- Script that ranks the longevity bands
-- That is their main style is 'Glam rock'

SELECT band_name, IF(split IS NULL, 2022 - formed, split - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
