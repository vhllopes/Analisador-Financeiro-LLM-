import ofxparse
import pandas as pd
import os
import io
from datetime import datetime

# Imports do LangChain/Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

# Carregar variáveis de ambiente (.env)
_ = load_dotenv(find_dotenv())

# Inicializar DataFrame vazio
df = pd.DataFrame()

# Defina o diretório dos extratos
pasta_extratos = "extratos"

# Verificar se a pasta existe antes de tentar listar
if os.path.exists(pasta_extratos):
    print(f"Lendo arquivos da pasta: {pasta_extratos}...")
    
    for extrato in os.listdir(pasta_extratos):
        # Filtrar apenas arquivos .ofx
        if not extrato.lower().endswith('.ofx'):
            continue
            
        file_path = os.path.join(pasta_extratos, extrato)
        
        try:
            # 1. Ler o arquivo como texto bruto (latin-1 evita erros de leitura)
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()

            # 2. CORREÇÃO: Remover espaços extras no cabeçalho de encoding
            content = content.replace("ENCODING: UTF - 8", "ENCODING:UTF-8")

            # 3. Parse do conteúdo corrigido
            ofx = ofxparse.OfxParser.parse(io.StringIO(content))

            transactions_data = []
            for account in ofx.accounts:
                if hasattr(account, 'statement') and account.statement:
                    for transaction in account.statement.transactions:
                        transactions_data.append({
                            "Data": transaction.date,
                            "Valor": transaction.amount,
                            "Descricao": transaction.memo,
                            "ID": transaction.id,
                        })

            if transactions_data:
                df_temp = pd.DataFrame(transactions_data)
                df_temp["Valor"] = df_temp["Valor"].astype(float)
                df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
                
                df = pd.concat([df, df_temp])
                print(f"Arquivo '{extrato}' processado com sucesso.")
        
        except Exception as e:
            print(f"Erro ao processar o arquivo '{extrato}': {e}")

    # Resetar o índice
    df = df.reset_index(drop=True)
    print(f"Total de transações importadas: {len(df)}")

else:
    print(f"A pasta '{pasta_extratos}' não foi encontrada.")

# =================================================================
# LLM - Classificação
# =================================================================

if not df.empty:
    template = """Você é um assistente contábil rigoroso. Sua tarefa é categorizar transações bancárias.

    LISTA DE CATEGORIAS PERMITIDAS (Use EXATAMENTE como escrito):
    - Alimentação
    - Receitas
    - Saúde
    - Mercado
    - Educação
    - Compras
    - Transporte
    - Investimento
    - Transferências para terceiros
    - Telefone
    - Moradia
    - Outros

    REGRAS OBRIGATÓRIAS:
    1. Responda APENAS com uma das palavras da lista acima.
    2. NÃO escreva frases, apenas a categoria.
    3. REGRA DE OURO PARA APPS:
       - Se contiver "IFD", "IFOOD", "RAPPI" ou "UBER EATS" -> Categoria é SEMPRE "Alimentação", mesmo que tenha nomes de pessoas depois.
       - Se contiver "UBER" ou "99APP" (sem ser eats) -> Categoria é "Transporte".
    4. Se a descrição for apenas um nome de pessoa (sem IFD antes) -> "Transferências para terceiros".
    
    EXEMPLOS DE TREINAMENTO:
    Entrada: UBER *VIAGEM
    Saída: Transporte

    Entrada: IFD*BRUNO MARQUES RODR
    Saída: Alimentação

    Entrada: IFD*GRECCO DEMAZI ALIM
    Saída: Alimentação

    Entrada: IFOOD CLUB
    Saída: Alimentação

    Entrada: RAUL BURIM DE CARVALHO
    Saída: Transferências para terceiros

    Entrada: PAGAMENTO DE SALARIO
    Saída: Receitas

    AGORA CLASSIFIQUE:
    Entrada: {text}"""

    prompt = PromptTemplate.from_template(template=template)

    # Certifique-se de que a GROQ_API_KEY está no .env
    chat = ChatGroq(model="llama-3.1-8b-instant")
    chain = prompt | chat

    print("Iniciando classificação com IA (isso pode demorar um pouco)...")
    
    category_list = []
    
    # Loop de classificação
    for i, transaction in enumerate(df["Descricao"].values):
        try:
            # Feedback visual simples para saber que está rodando
            print(f"Processando item {i+1}/{len(df)}: {transaction[:20]}...", end='\r')
            
            response = chain.invoke(transaction)
            category_list.append(response.content)
        except Exception as e:
            print(f"\nErro ao classificar '{transaction}': {e}")
            category_list.append("Erro na Classificação")

    df["Categoria"] = category_list

    print("\n--- Classificação Finalizada ---")
    print(df.head())
    
    # SALVAR ARQUIVO CSV
    nome_arquivo = "extrato_classificado.csv"
    # utf-8-sig garante que o Excel leia os acentos corretamente
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f"\nSucesso! Dados salvos em '{nome_arquivo}'")

else:
    print("Nenhuma transação foi processada.")