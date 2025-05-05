import sqlite3
from datetime import datetime

def view_db():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print("\n=== Cliques Registrados ===")
        c.execute("SELECT * FROM clicks")
        clicks = c.fetchall()
        if clicks:
            for click in clicks:
                print(f"User ID: {click[0]}")
                print(f"IP: {click[1]}")
                print(f"Navegador: {click[2]}")
                print(f"Data/Hora: {click[3]}")
                print("-" * 50)
        else:
            print("Nenhum clique registrado.")
        
        print("\n=== Tentativas de Login ===")
        c.execute("SELECT * FROM logins")
        logins = c.fetchall()
        if logins:
            for login in logins:
                print(f"User ID: {login[0]}")
                print(f"Usuário: {login[1]}")
                print(f"Senha: {login[2]}")
                print(f"IP: {login[3]}")
                print(f"Data/Hora: {login[4]}")
                print("-" * 50)
        else:
            print("Nenhuma tentativa de login registrada.")
        
        conn.close()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {str(e)}")

if __name__ == "__main__":
    view_db()