import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santaclara.settings')
django.setup()

from cadastro.models.vendedor import Vendedor
from cadastro.utils.criptografia_bcrypt_helper import CriptografiaBcryptHelper


def migrar_senhas():
    print("=" * 60)
    print("INICIANDO MIGRAÇÃO DE SENHAS DE VENDEDORES")
    print("=" * 60)
    
    vendedores = Vendedor.objects.all()
    total = vendedores.count()
    migrados = 0
    ja_migrados = 0
    
    if total == 0:
        print("\n⚠️  Nenhum vendedor encontrado no banco de dados.")
        return
    
    print(f"\n📊 Total de vendedores encontrados: {total}\n")
    
    for vendedor in vendedores:
        if vendedor.senha.startswith(('$2a$', '$2b$', '$2y$')):
            print(f"✓ {vendedor.nome} (matrícula: {vendedor.matricula}) - Senha já migrada")
            ja_migrados += 1
            continue
        
        try:
            senha_antiga = vendedor.senha
            vendedor.senha = CriptografiaBcryptHelper.hash_senha(senha_antiga)
            vendedor.save()
            
            print(f"✓ {vendedor.nome} (matrícula: {vendedor.matricula}) - Senha migrada com sucesso!")
            migrados += 1
            
        except Exception as e:
            print(f"✗ ERRO ao migrar {vendedor.nome} (matrícula: {vendedor.matricula}): {str(e)}")
    
    print("\n" + "=" * 60)
    print("MIGRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"✓ Senhas migradas: {migrados}")
    print(f"✓ Já estavam migradas: {ja_migrados}")
    print(f"📊 Total processado: {total}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        migrar_senhas()
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {str(e)}")
        print("Verifique se o Django está configurado corretamente.")