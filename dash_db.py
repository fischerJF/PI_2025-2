import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
    

conexao = pymysql.connect(
   host="localhost",
   user="root",
   password="",
   database="dashboard_db",
)

query = "SELECT * FROM produto"
df = pd.read_sql(query, con=conexao)

# Fechando a conexão com o banco
conexao.close()

st.set_page_config(layout="wide", page_title="Meu primeiro dashboard")

st.title('Dashboard com dados de um base de produtos')

###> Formatando um campo do tipo data
df['Date'] = pd.to_datetime(df['data'], format='%Y%m%d')

###> Calculando o Valor Faturado
df["valor_faturado"] = df["valor"] * df["quantidade"]

df = df.sort_values("Date")

###> Selecionando / agrupando por Ano-Mes (AAAA-MM)
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]
st.dataframe(df_filtered)

###> Montando o mosaico do dashboard:
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

###> Gráfico de Barras:
fig_date = px.bar(df_filtered, x="produto", y="quantidade", title="Quantidade Vendida", color="produto")
col1.plotly_chart(fig_date)

###> Gráfico de Dispersão:
fig_date3 = px.scatter(df_filtered, x="produto", y="valor_faturado", title="Valor Faturado", color="produto")
col2.plotly_chart(fig_date3)

###> Gráfico de Linha:
fig_date4 = px.line(df_filtered, x="Date", y="valor_faturado", title="Valor Faturado", color="produto")
col3.plotly_chart(fig_date4)

###> Gráfico de Pizza:
fig_date5 = px.pie(df_filtered, values="valor_faturado", names="produto", title="Percentual Vendido")
col4.plotly_chart(fig_date5)