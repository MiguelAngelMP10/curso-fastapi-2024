from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)
customer = Customer(
    name="Miguel Angel Muñoz Pozos",
    description="",
    email="mmunozpozos@gmail.com",
    age=30,
)
session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            description=f"Test number {x}",
            amount=10 * x,
        )
    )
session.commit()
