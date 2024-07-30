import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    return pd.read_csv(file_path, sep=';', encoding='utf-8')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def apply_css_and_favicon():
    local_css("style.css")
    st.markdown(
        """
        <head>
            <link rel="icon" href="assets/favicon.ico" type="image/x-icon">
        </head>
        """,
        unsafe_allow_html=True
    )

def add_header():
    st.markdown(
        """
        <div class="header">
            <h1 style="text-align: center;">Estudo de dash</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def plot_pie_chart(data):
    if 'Beneficio Fiscal' in data.columns:
        fig_pie = px.pie(data, names='Beneficio Fiscal', title='Distribuição de Benefício Fiscal', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

def plot_bar_chart(data):
    if 'UF' in data.columns:
        fig_bar = px.bar(data, x='UF', title='Distribuição por UF', labels={'UF': 'UF', 'count': 'Contagem'}, color='UF')
        st.plotly_chart(fig_bar, use_container_width=True)

def plot_line_chart(data):
    st.markdown("<h3 style='text-align: center;'>Gráfico de Linha - Início da Habilitação:</h3>", unsafe_allow_html=True)
    if 'Inicio Habilitacao' in data.columns:
        data['Inicio Habilitacao'] = pd.to_datetime(data['Inicio Habilitacao'], errors='coerce')
        data_sorted = data.dropna(subset=['Inicio Habilitacao']).sort_values('Inicio Habilitacao')

        min_year = data_sorted['Inicio Habilitacao'].dt.year.min()
        max_year = data_sorted['Inicio Habilitacao'].dt.year.max()
        selected_years = st.slider(
            "Escolha o intervalo de anos",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        data_filtered = data_sorted[
            (data_sorted['Inicio Habilitacao'].dt.year >= selected_years[0]) &
            (data_sorted['Inicio Habilitacao'].dt.year <= selected_years[1])
        ]
        
        fig_line = px.line(data_filtered, x='Inicio Habilitacao', y=data_filtered.index)
        st.plotly_chart(fig_line, use_container_width=True)

def plot_scatter_chart(data):
    if 'CNPJ' in data.columns and 'Codigo CNAE' in data.columns:
        fig_scatter = px.scatter(data, x='CNPJ', y='Codigo CNAE', title='Gráfico de Dispersão entre CNPJ e Código CNAE')
        st.plotly_chart(fig_scatter, use_container_width=True)

def plot_histogram(data):
    if 'Codigo CNAE' in data.columns:
        fig_histogram = px.histogram(data, x='Codigo CNAE', title='Distribuição do Código CNAE')
        st.plotly_chart(fig_histogram, use_container_width=True)

def plot_heatmap(data):
    if 'Codigo CNAE' in data.columns and 'Municipio' in data.columns:
        fig_heatmap = px.density_heatmap(data, x='Codigo CNAE', y='Municipio', title='Distribuição de Código CNAE por Município')
        st.plotly_chart(fig_heatmap, use_container_width=True)

def plot_box_chart(data):
    if 'Codigo CNAE' in data.columns and 'Beneficio Fiscal' in data.columns:
        fig_box = px.box(data, x='Beneficio Fiscal', y='Codigo CNAE', title='Distribuição do Código CNAE por Benefício Fiscal')
        st.plotly_chart(fig_box, use_container_width=True)

def plot_choropleth(data):
    if 'UF' in data.columns:
        # Contar a frequência de ocorrências por estado (UF)
        uf_counts = data['UF'].value_counts().reset_index()
        uf_counts.columns = ['UF', 'count']

        # Criar o mapa coroplético
        fig_choropleth = px.choropleth(
            uf_counts,
            geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
            locations="UF",
            featureidkey="properties.sigla",
            color="count",
            hover_name="UF",
            color_continuous_scale="Viridis",
            title="Mapa de Calor por Estado"
        )

        fig_choropleth.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_choropleth, use_container_width=True)

def main():
    st.set_page_config(page_title="Estudo de Dash", page_icon="assets/favicon.ico")
    apply_css_and_favicon()
    add_header()

    data = load_data('dados_ficticios.csv')

    col1, col2 = st.columns(2)
    with col1:
        plot_pie_chart(data)
    with col2:
        plot_bar_chart(data)

    plot_line_chart(data)

    col3, col4 = st.columns(2)
    with col3:
        plot_scatter_chart(data)
    with col4:
        plot_histogram(data)

    plot_heatmap(data)
    plot_box_chart(data)
    plot_choropleth(data)

if __name__ == "__main__":
    main()