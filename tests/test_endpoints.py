# Teste para o endpoint de registro (signup)
def test_signup(client):
    response = client.post("/signup", json={
        "name": "New User",
        "email": "newuser@example.com",
        "cpf": "11122233344",
        "password": "newpassword123"
    })
    assert response.status_code == 201
    assert response.json()["msg"] == "User created successfully"

# Teste para o endpoint de login
def test_login(client, test_user):
    # CORREÇÃO: Usar `json=` em vez de `data=` e a chave "email" em vez de "username"
    response = client.post("/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Teste para uma rota pública (listar voos)
def test_get_flights(client):
    response = client.get("/flights")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste para uma rota protegida por autenticação (ver perfil do usuário)
def test_read_users_me(client, test_user):
    # Primeiro, faz login para obter o token
    # CORREÇÃO: Usar `json=` em vez de `data=` e a chave "email" em vez de "username"
    login_response = client.post("/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    assert login_response.status_code == 200 # Adicionado para garantir que o login funcionou
    token = login_response.json()["access_token"]
    
    # Usa o token para acessar a rota protegida
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == "Test User"

# Teste para uma rota que não existe
def test_not_found(client):
    response = client.get("/some/nonexistent/route")
    assert response.status_code == 404