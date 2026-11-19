
"""
População inicial do banco de dados SQLite.

Este script reutiliza a função criar_banco() do módulo
sqlite_database.py, responsável por criar as tabelas
e inserir os dados iniciais de demonstração.

Projeto de Bloco - TP3
"""

from sqlite_database import criar_banco


def popular_banco():
    """
    Executa a criação e a população inicial do banco.

    A função criar_banco() utiliza CREATE TABLE IF NOT EXISTS,
    INSERT OR IGNORE para usuários e verifica se a tabela
    de previsões está vazia antes de inserir exemplos.
    """
    criar_banco()
    print("Script sqlite_populate.py executado com sucesso!")


if __name__ == "__main__":
    popular_banco()
