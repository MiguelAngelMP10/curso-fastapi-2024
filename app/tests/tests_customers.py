from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"api/v1/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "Jhon Doe"


def test_update_customer(client):
    # Crear un cliente
    response = client.post(
        "api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    customer_id = response.json()["id"]

    # Actualizar el cliente
    response_update = client.patch(
        f"api/v1/customers/{customer_id}",
        json={"name": "Jhon Updated", "email": "jhon_updated@example.com"}
    )
    assert response_update.status_code == status.HTTP_201_CREATED
    assert response_update.json()["name"] == "Jhon Updated"


def test_delete_customer(client):
    # Crear un cliente
    response = client.post(
        "api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    customer_id = response.json()["id"]

    # Eliminar el cliente
    response_delete = client.delete(f"api/v1/customers/{customer_id}")
    assert response_delete.status_code == status.HTTP_200_OK
    assert response_delete.json() == {"detail": "ok"}

    # Intentar leer el cliente eliminado
    response_read = client.get(f"api/v1/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND


def test_list_customers(client):
    # Crear un cliente
    client.post(
        "api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )

    # Listar clientes
    response = client.get("api/v1/customers")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Debe devolver una lista de clientes


def test_subscribe_customer_to_plan(client):
    # Crear cliente
    customer_response = client.post(
        "api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    customer_id = customer_response.json()["id"]

    # Crear plan (suponiendo que tienes un plan con id=1)
    plan_id = 1  # Debes tener un plan con este ID en tu base de datos

    # Suscribir al cliente al plan
    response = client.post(f"api/v1/customers/{customer_id}/plans/{plan_id}", params={"plan_status": "active"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
   # assert response.json()["customer_id"] == customer_id
   # assert response.json()["plan_id"] == plan_id

def test_get_customer_plans(client):
    # Crear cliente
    customer_response = client.post(
        "api/v1/customers",
        json={
            "name": "Jhon Doe",
            "email": "jhon@example.com",
            "age": 33,
        },
    )
    customer_id = customer_response.json()["id"]

    # Crear un plan y suscribirlo al cliente
    plan_id = 1  # Asegúrate de que este plan exista en tu base de datos
    client.post(f"api/v1/customers/{customer_id}/plans/{plan_id}", params={"plan_status": "active"})

    # Obtener los planes del cliente
    response = client.get(f"api/v1/customers/{customer_id}/plans", params={"plan_status": "active"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Debe devolver una lista de planes
