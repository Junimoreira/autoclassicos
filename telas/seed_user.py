from database.usuarios_db import inserir_usuario

inserir_usuario(
    nome="Administrador",
    usuario="admin",
    senha="auto123",
    perfil="admin"
)

print("Usuário criado com sucesso!")