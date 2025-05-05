EduPhish - Simulação Educacional de Phishing
Este projeto simula um ataque de phishing para fins educacionais, ensinando sobre segurança online. Não use para fins maliciosos.
Pré-requisitos

Python 3.6+
Navegador web (Chrome, Firefox, etc.)

Configuração

Clone o repositório:git clone https://github.com/seu-usuario/EduPhish.git
cd EduPhish/social_eng_mvp


Execute o script de configuração:python setup.py


Ative o ambiente virtual:
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate


Execute o servidor:python phishing_mvp.py



Uso

Acesse http://127.0.0.1:5000/ para a página inicial.
Clique em "Gerar E-mail Simulado" ou acesse http://127.0.0.1:5000/send_email?email=teste@exemplo.com para criar um link.
O link gerado é salvo em simulated_emails.txt. Clique para testar a página de login.
Preencha o formulário de login (use dados fictícios).
Acesse http://127.0.0.1:5000/admin (usuário: admin, senha: admin123) para ver o dashboard.

Estrutura

phishing_mvp.py: Servidor Flask.
static/style.css: Estilos realistas inspirados no Office 365.
templates/: Páginas HTML (index.html, login.html, result.html, admin.html, admin_login.html).
database.db: Banco de dados SQLite para cliques e logins.
simulated_emails.txt: Links de e-mails simulados.

Solução de Problemas

Erro no banco de dados: Exclua database.db e reinicie o servidor.
Erro 404 style.css: Confirme que static/style.css existe.
E-mails reais: Configure config.py com credenciais Outlook (opcional).

Notas Éticas
Este é um projeto educacional. Use apenas para aprendizado e com consentimento dos usuários testados.
