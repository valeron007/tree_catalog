from sqlalchemy import select

from src.db.database import db
from src.db.models.models import Catalog, Product, OrderItem, Order, OrderStatus, Client


def create_catalog() -> None:
    home_appliances = Catalog(name="Бытовая техника")
    home_appliances.append("Встраиваемая техника")
    home_appliances.append("Техника для дома")
    home_appliances.append("Техника для кухни")
    db.add(home_appliances)

    notebooks = Catalog(name="ПК, ноутбуки, периферия")
    notebooks.append("Hоутбуки")
    notebooks.append("Периферия и аксессуары")
    notebooks.append("Компьютеры и ПО")
    pc = notebooks["Компьютеры и ПО"]
    pc.append("Моноблоки")
    pc.append("Персональные компьютеры")
    pc.append("Платформы")

    periphery = notebooks["Периферия и аксессуары"]
    periphery.append("Мониторы")
    periphery.append("Клавиатуры")
    periphery.append("Мыши")

    db.add(notebooks)
    db.commit()

def createproducts() -> None:
    data = [ Product(name="'17.3' Ноутбук ARDOR GAMING NEO N17-I5ND414 черный", price=74999, catalog_id=6),
                Product(name="'17.3' Ноутбук MSI Katana 17 HX B14WGK-053XRU черный", price=79999, catalog_id=6),
                Product(name="'16' Ноутбук HUAWEI MateBook D 16 2024 MCLG-X серый16", price=79999, catalog_id=6),
                Product(name="'16' Ноутбук HONOR MagicBook X16 AMD 2025 серый", price=59999, catalog_id=6),
                Product(name="'17.3' Ноутбук MSI Cyborg 17 B2RWEKG-034XRU черный", price=29999, catalog_id=6),
                Product(name="'17.3' Ноутбук ASUS TUF Gaming FX707VJ-HX015 серый", price=39999, catalog_id=6),
                Product(name="16 Ноутбук GIGABYTE GAMING A16 черный", price=49999, catalog_id=6),
                Product(name="'17.3' Ноутбук MSI Katana GF76 B12UCR-821XRU черный17.3", price=49999, catalog_id=6),
                Product(name="'16' Ноутбук ASUS TUF Gaming F16 FX607VJ-RL047 серый", price=49999, catalog_id=6),
                Product(name="'16' Ноутбук HONOR MagicBook Pro 16 2025 белый", price=49999, catalog_id=6),
                Product(name="'17.3' Ноутбук ASUS TUF Gaming F17 FX707ZC4-HX014 серый", price=49999, catalog_id=6),
                Product(name="27 Монитор Xiaomi G27Qi черный", price=37000, catalog_id=9),
                Product(name="27 Монитор MSI PRO MP273A черный", price=25000, catalog_id=9),
                Product(name="27 Монитор ARDOR GAMING INFINITY PRO AQ27H1 черный", price=25000, catalog_id=9),
                Product(name="34 Монитор Xiaomi Curved Gaming Monitor G34WQi черный", price=25000, catalog_id=9),
                Product(name="27 Монитор Samsung Odyssey OLED G6 S27FG602SI серебристый", price=25000, catalog_id=9),
                Product(name="23.8 Монитор MSI PRO MP2412 черный", price=25000, catalog_id=9),
                Product(name="23.8 Монитор ARDOR GAMING PORTAL AF24H1 черный", price=25000, catalog_id=9),
                Product(name="24.5 Монитор TCL 25G64 серый", price=25000, catalog_id=9),
                Product(name="27 Моноблок MSI PRO AP272P 14M-1019XRU [9S6-AF8322-1019]", price=75000, catalog_id=12),
                Product(name="27 Моноблок ASUS V470VAK-WPE0330 [90PT03W1-M00HU0]", price=75000, catalog_id=12),
                Product(name="27 Моноблок MSI Modern AM273QP AI 1UM-094XRU [9S6-AF0112-094]", price=75000, catalog_id=12),
                Product(name="23.8 Моноблок MSI Modern AM242P 12M-1879XRU [9S6-AE0711-1879]", price=75000, catalog_id=12),
                Product(name="27 Моноблок Acer Aspire C27-2G [DQ.BPQCD.002]", price=75000, catalog_id=12),
                Product(name="Клавиатура беспроводная Logitech MX Keys S [Bluetooth, радиоканал, цвет белая]", price=75000, catalog_id=10),
                Product(
                name="Клавиатура беспроводная Logitech MX Keys S [Bluetooth, радиоканал, цвет черный]",
                price=5000, catalog_id=10),
                Product(
                name="Клавиатура проводная + беспроводная AULA F75 [Bluetooth, USB Type-A, радиоканал, цвет белый]",
                price=3000, catalog_id=10),
                Product(
                name="Клавиатура проводная Дарк Проджект KD87A [клавиш - 87, USB Type-A, цвет черный]",
                price=2000, catalog_id=10),
                Product(
                name="Клавиатура проводная Logitech K120 [USB Type-A, цвет черный]",
                price=2500, catalog_id=10),
        ]

    db.add_all(data)
    db.commit()


def create_order_items() -> None:
    order_id = 2
    product_id = 77
    quantity = 10
    try:
        # get order by id
        order = db.query(Order).where(Order.id == order_id).scalar()
        # get product by id
        product = db.query(Product).where(Product.id == product_id).scalar()
        product.count -= quantity
        # check exists order
        if order == None:
            print("Order not found")
            exit(1)

        # check exists product
        if product == None:
            print("Product not found")
            exit(1)

        # get order_item by order id and product id
        order_item = db.query(OrderItem).where(OrderItem.product_id == product_id).where(OrderItem.order_id == order_id).scalar()

        if order_item == None:
            order.order_items.append(OrderItem(order_id=order_id, product_id=product_id, quantity=quantity))
        else:
            order_item.quantity += quantity
        
        print(order_item)
    except Exception as e:
        print(e)
        db.rollback()
    else:
        db.commit()


    """Create orders."""
    # db.add_all(order.order_items)
    # db.commit()

def create_orders() -> None:
    """Create orders."""
    orders = [Order(client_id=1, status=OrderStatus.PENDING),
              Order(client_id=2, status=OrderStatus.PENDING),
              Order(client_id=3, status=OrderStatus.PENDING)]
    db.add_all(orders)
    db.commit()


def create_clients() -> None:
    clients = [
        Client(name="Valeron", address="Lenina 112"),
        Client(name="Semen", address="gadyukina 3"),
        Client(name="Vasya", address="stalina 5"),
    ]
    db.add_all(clients)
    db.commit()

if __name__=='__main__':
    # create_catalog()
    # createproducts()
    create_order_items()
    # create_orders()
    # create_clients()

