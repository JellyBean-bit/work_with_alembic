from orm import User, Address, Product, Order
from database import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy import text


def insert_users_and_addresses(session):
    for i in range(5):        
        user = User(
            username=f"Alex_{i}", 
            email=f"alex_{i}@example.com"
        )
    
        address = Address(
            street=f"Street_{i}",
            city=f"City_{i}",
            state=f"State_{i}",
            zip_code=f"1234{i}",
            country=f"Country_{i}",
            is_primary=True,
            user=user  
        )
        session.add(user)
        session.add(address)
    session.commit()
    

def insert_products(session):
    products = [
        Product(
            name=f"Product_{i}", 
            price=10.0 * (i + 1), 
            description=f"Описание продукта {i}"
        )
        for i in range(5)
    ]
    session.add_all(products)
    session.commit()
    return products


def get_users_with_addresses(session):
    stmt = select(User).options(selectinload(User.addresses))
    users = session.scalars(stmt).all()
    print(f"📋 Найдено пользователей: {len(users)}")
    return users


def insert_orders(session, users, products):
    for i, user in enumerate(users[:5]):  
        address = user.addresses[0] if user.addresses else None
        product = products[i]

        if not address:
            continue

        order = Order(
            user_id=user.id,
            address_id=address.id,
            product_id=product.id,
            quantity=i + 1,
            total_price=product.price * (i + 1),
        )
        session.add(order)

    session.commit()


def main():   
    session_factory = sessionmaker(engine)
    with session_factory() as session:
        insert_users_and_addresses(session)
        users = get_users_with_addresses(session)

        products = insert_products(session)
        insert_orders(session, users, products)


if __name__ == "__main__":
    main()
