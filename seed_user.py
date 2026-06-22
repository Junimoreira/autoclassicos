from database.usuarios_db import inserir_usuario

inserir_usuario(
    nome="Administrador",
    usuario="admin",
    senha="123456",
    perfil="admin"
)

print("Admin criado com senha criptografada!")