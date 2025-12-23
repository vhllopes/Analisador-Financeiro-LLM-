import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.title("💰 Dashboard de Finanças Pessoais")
st.markdown("---")

# ==============================================================================
# CARREGAMENTO E TRATAMENTO DE DADOS
# ==============================================================================
# O @st.cache_data faz com que o Streamlit não recarregue o CSV a cada clique, deixando o dashboard muito mais rápido.
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("extrato_classificado.csv")
        # Converte a coluna 'Data' para o formato de data real
        df['Data'] = pd.to_datetime(df['Data'])
        return df
    except FileNotFoundError:
        return None

df = carregar_dados()

if df is None:
    st.error("Arquivo 'extrato_classificado.csv' não encontrado. Rode o analisador.py primeiro!")
    st.stop() 

# ==============================================================================
# BARRA LATERAL (FILTROS)
# ==============================================================================
st.sidebar.header("Filtros")

# Filtro de Mês/Ano
df['Mes_Ano'] = df['Data'].dt.to_period('M').astype(str)
lista_meses = sorted(df['Mes_Ano'].unique(), reverse=True)

mes_selecionado = st.sidebar.selectbox("Selecione o Mês:", lista_meses)

# Filtro de Categorias
lista_categorias = df['Categoria'].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    "Filtrar Categorias:", 
    options=lista_categorias, 
    default=lista_categorias # Por padrão, marca todas
)

# ==============================================================================
# APLICANDO OS FILTROS AOS DADOS
# ==============================================================================
# Criamos um novo DataFrame (df_filtrado) apenas com o que o usuário escolheu
df_filtrado = df[
    (df['Mes_Ano'] == mes_selecionado) & 
    (df['Categoria'].isin(categorias_selecionadas))
]

# ==============================================================================
# CÁLCULO DE MÉTRICAS
# ==============================================================================
receitas = df_filtrado[df_filtrado['Valor'] > 0]['Valor'].sum()
despesas = df_filtrado[df_filtrado['Valor'] < 0]['Valor'].sum()
saldo = receitas + despesas

# Exibe as métricas em colunas lado a lado
col1, col2, col3 = st.columns(3)
col1.metric("Receitas", f"R$ {receitas:,.2f}")
col2.metric("Despesas", f"R$ {despesas:,.2f}", delta_color="inverse") # Vermelho se negativo
col3.metric("Saldo do Mês", f"R$ {saldo:,.2f}")

st.markdown("---")

# ==============================================================================
# VISUALIZAÇÃO GRÁFICA
# ==============================================================================

# Prepara os dados para o gráfico: Agrupar por categoria e somar
df_despesas = df_filtrado[df_filtrado['Valor'] < 0].copy()
# Convertemos para positivo para o gráfico de pizza não quebrar
df_despesas['Valor_Abs'] = df_despesas['Valor'].abs()

gastos_por_categoria = df_despesas.groupby('Categoria')['Valor_Abs'].sum().sort_values(ascending=False)


col_grafico, col_tabela = st.columns([2, 3]) 

with col_grafico:
    st.subheader("Distribuição de Gastos")
    
    if not gastos_por_categoria.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        
        wedges, texts, autotexts = ax.pie(
            gastos_por_categoria, 
            labels=gastos_por_categoria.index, 
            autopct='%1.1f%%', 
            startangle=90,
            colors=plt.cm.Pastel1.colors,
            wedgeprops={"edgecolor":"k", 'linewidth': 1, 'antialiased': True}
        )
        
        plt.setp(texts, color="white", fontsize=12, weight="bold")
        
        plt.setp(autotexts, size=10, weight="bold", color="#333333")
        
        ax.axis('equal') 
        
        # Garante que o fundo do gráfico seja transparente
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        
        st.pyplot(fig)
    else:
        st.info("Sem despesas para exibir neste período.")

with col_tabela:
    st.subheader("Extrato Detalhado")
    # Mostramos apenas colunas relevantes
    st.dataframe(
        df_filtrado[['Data', 'Descricao', 'Categoria', 'Valor']].sort_values(by='Data'),
        hide_index=True,
        use_container_width=True,
        height=400
    )