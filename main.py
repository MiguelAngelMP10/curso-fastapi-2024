from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import EmailStr, AnyUrl

from models import Customer, CustomerCreate, CustomerUpdate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from fastapi.openapi.models import Contact, License

app = FastAPI(
    title="Mi API de Ejemplo",
    description="Esta es una API de ejemplo construida con FastAPI",
    version="1.0.0",
    docs_url="/docs",  # URL donde estará la documentación Swagger
    redoc_url="/redoc",  # URL donde estará la documentación ReDoc
    contact=Contact(name="Miguel Ángel Muñoz Pozos", email="mmunozpozos@gmail.com"),
    license=License(name="MIT", url=AnyUrl("https://opensource.org/licenses/MIT")),
    lifespan=create_all_tables
)

countries = {
    "MX": {"iso_code": "MX", "time_zone": "America/Mexico_City"},
    "US": {"iso_code": "US", "time_zone": "America/New_York"},
    "GB": {"iso_code": "GB", "time_zone": "Europe/London"},
    "FR": {"iso_code": "FR", "time_zone": "Europe/Paris"},
    "DE": {"iso_code": "DE", "time_zone": "Europe/Berlin"},
    "IN": {"iso_code": "IN", "time_zone": "Asia/Kolkata"},
    "CN": {"iso_code": "CN", "time_zone": "Asia/Shanghai"},
    "JP": {"iso_code": "JP", "time_zone": "Asia/Tokyo"},
    "BR": {"iso_code": "BR", "time_zone": "America/Sao_Paulo"},
    "CA": {"iso_code": "CA", "time_zone": "America/Toronto"},
    "AU": {"iso_code": "AU", "time_zone": "Australia/Sydney"},
    "IT": {"iso_code": "IT", "time_zone": "Europe/Rome"},
    "RU": {"iso_code": "RU", "time_zone": "Europe/Moscow"},
    "ZA": {"iso_code": "ZA", "time_zone": "Africa/Johannesburg"},
    "KR": {"iso_code": "KR", "time_zone": "Asia/Seoul"},
    "SE": {"iso_code": "SE", "time_zone": "Europe/Stockholm"},
    "NG": {"iso_code": "NG", "time_zone": "Africa/Lagos"},
    "AE": {"iso_code": "AE", "time_zone": "Asia/Dubai"},
    "EG": {"iso_code": "EG", "time_zone": "Africa/Cairo"},
    "SG": {"iso_code": "SG", "time_zone": "Asia/Singapore"},
    "NL": {"iso_code": "NL", "time_zone": "Europe/Amsterdam"},
    "ES": {"iso_code": "ES", "time_zone": "Europe/Madrid"},
    "PT": {"iso_code": "PT", "time_zone": "Europe/Lisbon"},
    "AR": {"iso_code": "AR", "time_zone": "America/Argentina/Buenos_Aires"},
    "CL": {"iso_code": "CL", "time_zone": "America/Santiago"},
    "PE": {"iso_code": "PE", "time_zone": "America/Lima"},
    "CO": {"iso_code": "CO", "time_zone": "America/Bogota"},
    "MY": {"iso_code": "MY", "time_zone": "Asia/Kuala_Lumpur"},
    "TH": {"iso_code": "TH", "time_zone": "Asia/Bangkok"},
    "RO": {"iso_code": "RO", "time_zone": "Europe/Bucharest"},
    "BG": {"iso_code": "BG", "time_zone": "Europe/Sofia"},
    "KE": {"iso_code": "KE", "time_zone": "Africa/Nairobi"},
    "TW": {"iso_code": "TW", "time_zone": "Asia/Taipei"},
    "TR": {"iso_code": "TR", "time_zone": "Europe/Istanbul"},
    "PK": {"iso_code": "PK", "time_zone": "Asia/Karachi"},
    "VN": {"iso_code": "VN", "time_zone": "Asia/Ho_Chi_Minh"},
    "ID": {"iso_code": "ID", "time_zone": "Asia/Jakarta"},
    "UA": {"iso_code": "UA", "time_zone": "Europe/Kiev"},
    "GR": {"iso_code": "GR", "time_zone": "Europe/Athens"},
    "PL": {"iso_code": "PL", "time_zone": "Europe/Warsaw"},
}


@app.get("/")
async def root():
    return {"messege": "Hola, Mundo!"}


@app.get("/time")
async def time():
    hour_actually = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"time": hour_actually}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    country_code = iso_code.upper()
    iso_code = countries[country_code]["iso_code"]
    time_zone = countries[country_code]["time_zone"]

    hour_actually = datetime.now(ZoneInfo(time_zone)).strftime("%Y-%m-%d %H:%M:%S")
    return {"time": hour_actually}


@app.post("/customers", response_model=Customer, tags=["Customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    return customer_db


@app.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["Customers"],
)
async def read_customer(
        customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@app.delete("/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@app.get("/customers", response_model=list[Customer], tags=["Customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post('/invoices')
async def create_invoices(invoice_data: Invoice):
    return invoice_data
