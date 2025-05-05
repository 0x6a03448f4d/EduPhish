EduPhish - Simulação Educacional de Phishing
Este projeto simula um ataque de phishing para fins educacionais, permitindo que empresas testem a conscientização de seus funcionários sobre segurança online. Não use para fins maliciosos.
Pré-requisitos

Python 3.6+
Navegador web (Chrome, Firefox, etc.)
Conta Outlook (opcional, para envio de e-mails reais)

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
Clique em "Configurar Campanha" para inserir e-mails dos funcionários e escolher o método de envio (simulação ou e-mail real).
Para envio real, forneça credenciais de uma conta Outlook.
Clique nos links gerados para testar a página de login (use dados fictícios).
Acesse http://127.0.0.1:5000/admin (usuário: admin, senha: admin123) para ver o dashboard.
Para visualizar dados no terminal, execute:python view_db.py



Configurando uma Conta Outlook para Envio Real

Crie uma conta em https://outlook.live.com/.
Acesse https://account.live.com/security e ative a verificação em duas etapas (se necessário).
Gere uma senha de aplicativo em https://account.live.com/security (se a autenticação padrão falhar).
Use o e-mail e a senha de aplicativo no formulário de campanha.

Estrutura

phishing_mvp.py: Servidor Flask.
view_db.py: Script para visualizar dados no terminal.
config.py: Configurações SMTP (para e-mails reais).
static/style.css: Estilos realistas inspirados no Office 365.
templates/: Páginas HTML (index.html, campaign.html, login.html, result.html, admin.html, admin_login.html, email.html).
database.db: Banco de dados SQLite para cliques e logins.
simulated_emails.txt: Links de e-mails simulados.

Solução de Problemas

Erro no banco de dados: Exclua database.db e reinicie o servidor.
Erro 404 style.css: Confirme que static/style.css existe.
Erro no envio de e-mails: Verifique as credenciais Outlook e autorize logins em https://account.live.com/security.
Erro TemplateNotFound: Confirme que templates/campaign.html e templates/email.html existem.
Dashboard vazio: Execute python view_db.py para verificar os dados.

Notas Éticas
Este é um projeto educacional. Obtenha consentimento dos funcionários antes de realizar testes. Informe que se trata de uma simulação educacional.
