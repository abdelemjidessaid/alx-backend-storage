-- Script that creates a trigger named reduce_quantity
-- The trigger reduces of an item in items table after every insert operation

-- drop the trigger if it is exists
DROP TRIGGER IF EXISTS reduce_quantity;
-- create the trigger
-- the start of delimiter
DELIMITER $$
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
-- loop over each row and update items with reducing the quantity
-- by the new item inserted
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$
-- end of loop
DELIMITER ;
-- the end of the delimiter
