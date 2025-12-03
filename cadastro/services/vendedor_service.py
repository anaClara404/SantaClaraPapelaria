import psycopg2
from db import get_connection
from cadastro.utils.criptografia_bcrypt_helper import CriptografiaBcryptHelper


class VendedorService:
    def inserir():
        matricula = input("Matrícula (8 caracteres): ").strip()
        if len(matricula) != 8:
            print("Erro: A matrícula deve conter exatamente 8 caracteres.")
            return
        nome = input("Nome do vendedor: ")
        comissao = input("Comissão (opcional, deixe vazio se não quiser): ")
        senha = input("Senha: ")

        senha_criptografada = CriptografiaBcryptHelper.hash_senha(senha)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO cadastro.vendedor (matricula, nome, comissao, senha) VALUES (%s, %s, %s, %s)',
            (matricula, nome, comissao if comissao else None, senha_criptografada)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Vendedor cadastrado com sucesso!")

    def alterar():
        matricula = input("Matrícula do vendedor para alterar: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
        vendedor = cur.fetchone()

        if not vendedor:
            print("Vendedor não encontrado.")
            cur.close()
            conn.close()
            return

        print(f"Vendedor atual: Nome: {vendedor[1]}, Comissão: {vendedor[2]}")

        novo_nome = input(f"Novo nome ({vendedor[1]}): ") or vendedor[1]
        nova_comissao = input(f"Nova comissão ({vendedor[2]}): ") or vendedor[2]
        nova_senha = input("Nova senha (deixe vazio para manter a atual): ")

        if nova_senha:
            senha_criptografada = CriptografiaBcryptHelper.hash_senha(nova_senha)
        else:
            senha_criptografada = vendedor[3]

        cur.execute(
            'UPDATE cadastro.vendedor SET nome = %s, comissao = %s, senha = %s WHERE matricula = %s',
            (novo_nome, nova_comissao if nova_comissao else None, senha_criptografada, matricula)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Vendedor alterado com sucesso!")

    def pesquisar_por_nome():
        nome = input("Nome para pesquisa: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE nome ILIKE %s', (f'%{nome}%',))
        vendedores = cur.fetchall()
        
        if vendedores:
            for v in vendedores:
                print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
        else:
            print("Nenhum vendedor encontrado.")
        
        cur.close()
        conn.close()

    def remover():
        matricula = input("Matrícula do vendedor para remover: ").strip()

        if not matricula:
            print("Erro: Matrícula não pode ser vazia.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
            if cur.rowcount == 0:
                print("Vendedor não encontrado.")
                conn.rollback()
            else:
                conn.commit()
                print("Vendedor removido com sucesso.")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "foreign key" in str(e).lower():
                print("Erro: Este vendedor não pode ser removido porque está sendo referenciado em outra tabela.")
            else:
                print(f"Erro ao remover vendedor: {e}")
        finally:
            cur.close()
            conn.close()

    def listar_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor')
        vendedores = cur.fetchall()
        
        if vendedores:
            for v in vendedores:
                print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
        else:
            print("Nenhum vendedor cadastrado.")
        
        cur.close()
        conn.close()

    @staticmethod
    def exibir_um():
        matricula = input("Matrícula do vendedor: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
        v = cur.fetchone()
        
        if v:
            print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
        else:
            print("Vendedor não encontrado.")
        
        cur.close()
        conn.close()