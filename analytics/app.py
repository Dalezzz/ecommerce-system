import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/ecommerce")


@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)


@st.cache_data(ttl=300)
def run_query(query: str) -> pd.DataFrame:
    return pd.read_sql(query, get_engine())


def safe_currency(value: float) -> str:
    return f"${value:,.2f}"

st.set_page_config(page_title="Dashboard Analítico", layout="wide")
st.title("Análisis de E-commerce")

with st.sidebar:
    st.header("Configuracion")
    st.caption("Fuente de datos")
    st.code(DATABASE_URL, language="text")

try:
    # Cargar datos de ordenes y clientes
    df_ordenes = run_query("SELECT * FROM ordenes")
    df_items = run_query("SELECT * FROM items_orden")
    df_usuarios = run_query("SELECT * FROM usuarios")
    df_productos = run_query(
        "SELECT p.*, c.nombre as categoria FROM productos p JOIN categorias c ON p.categoria_id = c.id"
    )
except SQLAlchemyError as exc:
    st.error("No fue posible conectarse a la base de datos para analytics.")
    st.exception(exc)
    st.stop()

if df_ordenes.empty:
    st.warning("No hay ordenes disponibles para mostrar analitica.")
    st.stop()

df_ordenes["fecha_creacion"] = pd.to_datetime(df_ordenes["fecha_creacion"], errors="coerce")

# KPIs
ventas_hoy = df_ordenes[df_ordenes["fecha_creacion"].dt.date == pd.Timestamp.today().date()]["total"].sum()
ticket_promedio = float(df_ordenes["total"].mean() or 0)
productos_unicos = int(df_items["producto_id"].nunique()) if not df_items.empty else 0
usuarios_registrados = int(df_usuarios["id"].nunique()) if not df_usuarios.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas del dia", safe_currency(float(ventas_hoy or 0)))
col2.metric("Ticket promedio", safe_currency(ticket_promedio))
col3.metric("Productos unicos vendidos", productos_unicos)
col4.metric("Usuarios registrados", usuarios_registrados)

# Tendencia diaria de ventas
df_sales = (
    df_ordenes.dropna(subset=["fecha_creacion"])
    .assign(fecha=lambda frame: frame["fecha_creacion"].dt.date)
    .groupby("fecha", as_index=False)["total"]
    .sum()
)

fig_sales = px.line(
    df_sales,
    x="fecha",
    y="total",
    title="Evolucion de ventas por dia",
    markers=True,
)
st.plotly_chart(fig_sales, use_container_width=True)

# Distribucion por categoria
if not df_productos.empty:
    fig_categoria = px.pie(df_productos, names="categoria", title="Distribucion de productos por categoria")
    st.plotly_chart(fig_categoria, use_container_width=True)

# Analisis RFM basico
ahora = pd.Timestamp.now()
rfm = (
    df_ordenes.groupby("usuario_id")
    .agg(
        Recencia=("fecha_creacion", lambda x: (ahora - x.max()).days),
        Frecuencia=("id", "count"),
        Monetario=("total", "sum"),
    )
    .sort_values(by="Monetario", ascending=False)
)

st.subheader("Top clientes por valor monetario")
st.dataframe(rfm.head(20), use_container_width=True)