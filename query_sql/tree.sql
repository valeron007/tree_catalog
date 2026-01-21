-- Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры
WITH RECURSIVE cat AS (
   SELECT id, parent_id, name, 1 AS level
   FROM catalogs
   WHERE parent_id IS NOT NULL

   UNION

   SELECT catalogs.id, catalogs.parent_id, catalogs.name, cat.level + 1 AS level
   FROM catalogs
      JOIN cat
          ON catalogs.parent_id = cat.id
)

SELECT DISTINCT * FROM cat WHERE level = 1;

--
-- Топ-5 самых покупаемых товаров за
-- последний месяц» (по количеству штук в заказах)

CREATE VIEW product_sales (name, catalog_name, count_product) AS
WITH RECURSIVE cat AS (
   SELECT id, parent_id, name,
   1 AS level,
   cast (id as varchar (100)) as path,
   id as root
   FROM catalogs
   WHERE parent_id IS NULL

   UNION

	SELECT ct.id, ct.parent_id,
   		ct.name,
   		cat.level + 1 AS level,
   		cast (cat.path || '->' || ct.id as varchar(100)) AS path,
		cat.root
	FROM catalogs ct
	JOIN cat
          ON ct.parent_id = cat.id
)

SELECT
    prod.name, catalogs.name,
    SUM(quantity) AS total_sales_count -- Считаем количество заказов для каждого товара
FROM
    order_items
JOIN products as prod ON order_items.product_id = prod.id
JOIN cat ON prod.catalog_id = cat.id
JOIN catalogs ON cat.root = catalogs.id
WHERE order_items.created_at >= current_date - interval '1 month'
GROUP BY
    prod.name, catalogs.name -- Группируем по названию товара
ORDER BY
    total_sales_count DESC -- Сортируем по убыванию количества продаж
LIMIT 5;

--

-- не делал тригерные функции для вычисления total_price в таблице orders
-- trigger function before delete

CREATE OR REPLACE FUNCTION deleted_order_item()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products as pr
	SET count = pr.count + OLD.quantity
	WHERE pr.id = OLD.product_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_order_item_deletion_trigger
BEFORE DELETE ON order_items
FOR EACH ROW
EXECUTE FUNCTION deleted_order_item();

-- trigger function after insert order items

CREATE OR REPLACE FUNCTION update_products_after_insert_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products as pr
	SET count = pr.count - NEW.quantity
	WHERE pr.id = NEW.product_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_order_item_insert_trigger
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_products_after_insert_count();

-- before update
CREATE OR REPLACE FUNCTION after_update_products()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products as pr
	SET count = pr.count - NEW.quantity
	WHERE pr.id = NEW.product_id;
	NEW.quantity := NEW.quantity + OLD.quantity;
	-- RAISE NOTICE 'NEW quantity: "%" OLD quantity "%"', NEW.quantity, OLD.quantity;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_order_item_update_trigger
BEFORE UPDATE ON order_items
FOR EACH ROW
EXECUTE FUNCTION after_update_products();

