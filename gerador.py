import pandas as pd
from faker import Faker
import random

# Inicialize o gerador de dados fictícios
fake = Faker()

# Funções auxiliares para gerar dados fictícios
def generate_cnpj():
    return f'{fake.random_int(min=10**13, max=10**14-1)}'

def generate_cnae():
    return f'{fake.random_int(min=1000, max=9999)}'

def generate_uf():
    ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    return random.choice(ufs)

def generate_beneficio_fiscal():
    beneficios = ['Isenção', 'Redução de Alíquota', 'Suspensão', 'Outros']
    return random.choice(beneficios)

def generate_base_legal():
    return f'Lei {fake.random_int(min=1, max=10000)}'

# Lista para armazenar os dados
data = []

for _ in range(500):
    item = {
        "CNPJ": generate_cnpj(),
        "Razao Social": fake.company(),
        "Nome Fantasia": fake.company_suffix(),
        "Codigo CNAE": generate_cnae(),
        "CNAE": f'CNAE {fake.random_int(min=1000, max=9999)}',
        "Municipio": fake.city(),
        "UF": generate_uf(),
        "Beneficio Fiscal": generate_beneficio_fiscal(),
        "Base Legal": generate_base_legal(),
        "Descricao": fake.sentence(),
        "Inicio Habilitacao": fake.date_this_decade(before_today=True, after_today=False).strftime('%d/%m/%Y'),
        "Fim Habilitacao": fake.date_this_decade(before_today=False, after_today=True).strftime('%d/%m/%Y')
    }
    data.append(item)

# Cria um DataFrame e salva como CSV
df = pd.DataFrame(data)
df.to_csv('dados_ficticios.csv', sep=';', index=False, encoding='utf-8')

print("CSV 'dados_ficticios.csv' gerado com sucesso!")
