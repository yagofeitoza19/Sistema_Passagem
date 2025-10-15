from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
# ATUALIZAÇÃO: Importar APIRoute
from fastapi.routing import APIRoute
from app.routes import auth, voos, reservas, admin
from app.auth import get_current_user
from app.schemas import User as UserSchema

app = FastAPI()

# Incluindo as rotas com tags para organizar a documentação
app.include_router(auth.router, tags=["Authentication"])
app.include_router(voos.router, tags=["Flights"])
app.include_router(reservas.router, tags=["Reservations"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/users/me", response_model=UserSchema, tags=["Users"])
def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    """
    Endpoint de teste para verificar as informações do usuário logado.
    """
    return current_user

# --- FUNÇÃO PARA CORRIGIR A TELA "AUTHORIZE" ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Sistema de Passagens Aéreas API",
        version="1.0.0",
        description="API para o sistema de compra de passagens aéreas.",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # ATUALIZAÇÃO: A lógica do loop foi corrigida para evitar o erro.
    # Agora, ela aplica a segurança apenas em rotas de API, ignorando as internas.
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.path not in ["/login", "/signup"]:
                for method in route.methods:
                    # Adiciona a trava de segurança no schema
                    openapi_schema["paths"][route.path][method.lower()]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# --- FIM DA CORREÇÃO ---