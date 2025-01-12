import pytest
from app import create_app, db
from app.models import TaskManager, Task
from datetime import datetime

@pytest.fixture
def app():
    return create_app('testing')

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def task_manager(app):
    with app.app_context():
        return TaskManager(db) 

# Teste 1: Listar tarefas quando não há nenhuma
def test_list_tasks_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.get_json() == []

# Teste 2: Adicionar uma nova tarefa
def test_add_task_e2e(client): 
    task_data = {
        "description": "Estudar Python",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    response_get = client.get("/tasks/")
    assert response_get.status_code == 200
    tasks = response_get.get_json()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Estudar Python"
    assert tasks[0]["category"] == "Pessoal"
    assert tasks[0]["deadline"] == "2024-12-31"
    assert tasks[0]["completed"] is False


# Teste 3: Listar tarefas após adicionar uma
def test_list_tasks_after_adding(client):
    task_data = {
        "description": "Estudar Python",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_data)
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1


# Teste 4: Editar uma tarefa existente
def test_edit_task(client):
    task_data = {
        "description": "Estudar Python",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.get_json()
    task_id = created_task["id"]
    assert task_id == 1

    edited_task_data = {
        "description": "Tarefa Editada",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    put_response = client.put(f"/tasks/{task_id}", json=edited_task_data)
    assert put_response .status_code == 200
    edited_task = put_response.get_json()
    assert edited_task["description"] == "Tarefa Editada"


# Teste 5: Marcar uma tarefa como concluída
def test_mark_task_completed(client):
    task_data = {
        "description": "Estudar Python",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_data)
    response = client.patch("/tasks/1/complete")
    assert response.status_code == 200
    task = response.get_json()
    assert task["completed"] is True


# Teste 6: Editar tarefa inexistente
def test_edit_nonexistent_task(client):
    task_data = {
        "description": "Inexistente",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    response = client.put("/tasks/999", json=task_data)
    assert response.status_code == 404


# Teste 7: Deletar uma tarefa existente
def test_delete_task(client):
    client.post("/tasks/", json={"description": "Tarefa 1"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task 1 deleted"


# Teste 8: Deletar tarefa inexistente
def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 200  # O sistema trata como sucesso


# Teste 9: Marcar tarefa inexistente como concluída
def test_mark_nonexistent_task_completed(client):
    response = client.patch("/tasks/999/complete")
    assert response.status_code == 404


# Teste 10: Listar tarefas pendentes
def test_list_pending_tasks(client):
    client.delete("/tasks/clear")
    task_1_data = {
        "description": "Tarefa 1",
        "category": "Pessoal",
        "deadline": "2024-12-30",
    }
    task_2_data = {
        "description": "Tarefa 2",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_1_data)
    client.post("/tasks/", json=task_2_data)
    client.patch("/tasks/1/complete")  # Concluir a primeira tarefa
    response = client.get("/tasks/?completed=false")
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Tarefa 2"


# Teste 11: Listar tarefas concluídas
def test_list_completed_tasks(client):
    client.delete("/tasks/clear")
    response_before = client.get("/tasks/?completed=true")
    tasks_before = response_before.get_json()
    num_completed_before = len(tasks_before)

    task_data = {
        "description": "Tarefa 3",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_data)
    client.patch("/tasks/1/complete")

    response_after = client.get("/tasks/?completed=true")
    tasks_after = response_after.get_json()
    num_completed_after = len(tasks_after)

    assert num_completed_after == num_completed_before + 1
    assert any(task["description"] == "Tarefa 3" for task in tasks_after)


# Teste 12: Adicionar tarefa sem descrição
def test_add_task_without_description(client):
    response = client.post("/tasks/", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Description is required"


# Teste 13: Adicionar tarefa com categoria personalizada
def test_add_task_with_category(client):
    client.delete("/tasks/clear")
    task_data = {
        "description": "Ler um livro",
        "category": "Lazer",
    }  # Categoria inválida
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 400  # Espera o código de status 400
    assert response.get_json()["error"] == "Categoria inválida"


# Teste 14: Persistência de dados entre requisições
def test_task_persistence(client):
    client.delete("/tasks/clear")
    task_data = {
        "description": "Estudar Python",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_data)
    response = client.get("/tasks/")
    assert len(response.get_json()) == 1


# Teste 15: Validação de id único para tarefas
def test_unique_task_ids(client):
    client.delete("/tasks/clear")
    task_1_data = {
        "description": "Tarefa 1",
        "category": "Pessoal",
        "deadline": "2024-12-30",
    }
    task_2_data = {
        "description": "Tarefa 2",
        "category": "Pessoal",
        "deadline": "2024-12-31",
    }
    client.post("/tasks/", json=task_1_data)
    client.post("/tasks/", json=task_2_data)
    tasks = client.get("/tasks/").get_json()
    assert tasks[0]["id"] != tasks[1]["id"]
