import bcrypt
from database.connection import conectar

# =========================
# VALIDAR LOGIN
# =========================
def validar_login(usuario, senha):
    conn = conectar()

    if conn is None:
        return None

    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, usuario, senha, perfil, ativo
        FROM usuarios
        WHERE usuario = %s
    """, (usuario,))

    user = cur.fetchone()
    conn.close()

    if not user:
        return None

    senha_bd = user[3]

    if bcrypt.checkpw(senha.encode('utf-8'), senha_bd.encode('utf-8')):
        return user

    return None


# =========================
# INSERIR USUÁRIO
# =========================
def inserir_usuario(nome, usuario, senha, perfil="usuario"):
    conn = conectar()

    if conn is None:
        return

    cur = conn.cursor()

    hash_senha = bcrypt.hashpw(
        senha.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    cur.execute("""
        INSERT INTO usuarios (nome, usuario, senha, perfil)
        VALUES (%s, %s, %s, %s)
    """, (nome, usuario, hash_senha, perfil))

    conn.commit()
    conn.close()

#==============================
#LISTAR USUARIOS
#=============================
def listar_usuarios():
    conn = conectar()

    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, usuario, perfil, ativo, created_at
        FROM usuarios
        ORDER BY id DESC
    """)

    dados = cur.fetchall()
    conn.close()
    return dados


# =========================
# ATUALIZAR USUÁRIO
# =========================
def atualizar_usuario(id, nome, usuario, perfil, ativo):
    conn = conectar()

    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET nome=%s,
            usuario=%s,
            perfil=%s,
            ativo=%s
        WHERE id=%s
    """, (nome, usuario, perfil, ativo, id))

    conn.commit()
    conn.close()


# =========================
# DELETAR USUÁRIO
# =========================
def deletar_usuario(id):
    conn = conectar()

    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        DELETE FROM usuarios
        WHERE id=%s
    """, (id,))

    conn.commit()
    conn.close()