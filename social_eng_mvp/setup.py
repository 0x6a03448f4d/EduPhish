import os
import subprocess
import sys

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr}")
        sys.exit(1)
    return result.stdout

print("Configurando o projeto EduPhish...")
# Criar ambiente virtual
if not os.path.exists('venv'):
    print("Criando ambiente virtual...")
    run_command(f"{sys.executable} -m venv venv")

# Ativar ambiente virtual e instalar dependências
print("Instalando dependências...")
if sys.platform.startswith('win'):
    run_command('venv\\Scripts\\activate && pip install flask')
else:
    run_command('source venv/bin/activate && pip install flask')

print("Configuração concluída! Para executar:")
print("1. Ative o ambiente virtual:")
print("   Windows: venv\\Scripts\\activate")
print("   Linux/Mac: source venv/bin/activate")
print("2. Execute: python phishing_mvp.py")