-- Script that create an INDEX on a name
-- Index that points on the first letter of name from 'names' table

CREATE INDEX idx_name_first ON names(name(1));
