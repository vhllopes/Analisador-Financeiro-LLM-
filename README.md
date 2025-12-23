# 💰 Gestão Financeira com IA

![Status](https://img.shields.io/badge/Status-Finalizado-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![AI](https://img.shields.io/badge/AI-Llama%203-purple)

Um sistema automatizado para análise de finanças pessoais. O projeto lê extratos bancários brutos (arquivos `.ofx`), utiliza Inteligência Artificial (LLM Llama 3 via Groq) para categorizar cada transação e apresenta os resultados em um Dashboard interativo.

## 🚀 Funcionalidades

- **Leitura de Extratos:** Suporte para arquivos `.ofx` (padrão bancário) com tratamento automático de erros de codificação (UTF-8/Latin-1).
- **Classificação Inteligente:**
  - Uso do modelo **Llama 3.1-8b** para entender contextos de gastos.
  - Regras de "Few-Shot Learning" para alta precisão.
  - Tratamento específico para aplicativos (iFood, Uber, Rappi) para evitar erros comuns.
- **Dashboard Interativo:**
  - Visualização de KPIs (Receitas, Despesas, Saldo).
  - Filtros dinâmicos por Mês e Categoria.
  - Gráficos de Pizza (Matplotlib) com design otimizado para Dark Mode.
  - Tabela detalhada de transações.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface (Frontend):** Streamlit
- **IA / LLM:** LangChain + Groq API (Llama 3)
- **Manipulação de Dados:** Pandas
- **Gráficos:** Matplotlib
- **Parsing Bancário:** Ofxparse

## 📂 Estrutura do Projeto

```text
📁 gestao-financeira/
│
├── 📂 extratos/              # Coloque seus arquivos .ofx aqui
├── 📄 analisador.py          # Script de processamento e classificação (Backend)
├── 📄 dashboard.py           # Script do Dashboard visual (Frontend)
├── 📄 .env                   # Arquivo de variáveis de ambiente (API Key)
├── 📄 requirements.txt       # Lista de dependências
└── 📄 extrato_classificado.csv # Arquivo gerado automaticamente (Base de dados)
```
## ⚙️ Instalação e Configuração
**1. Clone o repositório**
```bash
git clone https://github.com/vhllopes/Analisador-Financeiro-LLM-
cd gestao-financeira-ia
```
**2. Instale as dependências**

*Certifique-se de ter o Python instalado.*
```bash
pip install -r requirements.txt
```
*Caso não tenha o arquivo requirements.txt, instale manualmente:*  
```bash
pip install streamlit pandas matplotlib langchain-groq langchain-core python-dotenv ofxparse
```
**3. Configure a API Key**

*Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave da Groq:*
```bash
GROQ_API_KEY=sua_chave_aqui_
```

## ▶️ Como Usar
**Passo 1: Processar os Dados**

Coloque seus arquivos `.ofx` na pasta `extratos/` e execute o analisador. Isso vai ler os arquivos, conectar com a IA e gerar o CSV classificado.

```bash
python analisador.py
```

**Passo 2: Abrir o Dashboard**

Com o CSV gerado, inicie o dashboard visual:
```bash
streamlit run dashboard.py
```
*O navegador abrirá automaticamente no endereço http://localhost:8501.*

## 📊 Exemplo do Dashboard

`![Dashboard Screenshot](screenshot/image.png)`

## 👨‍💻 Autor

Feito por **Vitor Lopes**.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vhllopes)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vhllopes)