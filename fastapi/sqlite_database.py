
import sqlite3
from pathlib import Path
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

DB_PATH = Path(__file__).resolve().parent / "database.db"


def criar_banco():
    with sqlite3.connect(DB_PATH) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                ticket_text TEXT NOT NULL,
                predicted_category TEXT NOT NULL,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)

        # Usuários de demonstração.
        # As senhas reais serão definidas e armazenadas
        # como hashes ao integrar a autenticação.
        usuarios = [
            ("usuario1", password_hash.hash("Teste123!Usuario1")),
            ("usuario2", password_hash.hash("Teste123!Usuario2"))
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO users
            (username, hashed_password)
            VALUES (?, ?)
        """, usuarios)

        cursor.execute(
            "SELECT id, username FROM users"
        )
        ids = {
            username: id_usuario
            for id_usuario, username in cursor.fetchall()
        }

        cursor.execute(
            "SELECT COUNT(*) FROM predictions"
        )

        if cursor.fetchone()[0] == 0:
            previsoes = [
                (
                    ids["usuario1"],
                    "Preciso de ajuda com meu pagamento",
                    "Billing"
                ),
                (
                    ids["usuario1"],
                    "Não consigo acessar minha conta",
                    "Technical Issue"
                ),
                (
                    ids["usuario2"],
                    "Gostaria de solicitar um reembolso",
                    "Refund request"
                )
            ]

            cursor.executemany("""
                INSERT INTO predictions
                (owner_id, ticket_text, predicted_category)
                VALUES (?, ?, ?)
            """, previsoes)

        for username, hashed_password in usuarios:
            cursor.execute("""
                UPDATE users
                SET hashed_password = ?
                WHERE username = ?
            """, (hashed_password, username))

        conexao.commit()

    print("Banco de dados criado e populado com sucesso!")


if __name__ == "__main__":
    criar_banco()
