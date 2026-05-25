# Bibliotecas
import os
import streamlit as st
import pandas as pd

# Carregando e processando dados
st.set_page_config(layout="centered")
st.header('Filtro de pesquisa de dados com paginação')
@st.cache_data(show_spinner=False)
def load_data(file_path):
    dataset = pd.read_csv(file_path)
    return dataset
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

# Interface de paginação
file_path = st.file_uploader("Selecione o arquivo CSV para upload", type=["csv"])
if file_path:
    dataset = load_data(file_path)
    top_menu = st.columns(3)
    with top_menu[0]:
        sort = st.radio("Classificar dados", options=["Sim", "Não"], horizontal=1, index=1)
    if sort == "Sim":
        with top_menu[1]:
            sort_field = st.selectbox("Classificar por", options=dataset.columns)
        with top_menu[2]:
            sort_direction = st.radio(
                "Direcão", options=["⬆️", "⬇️"], horizontal=True
            )
        dataset = dataset.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Tamanho", options=[10, 20, 50])
    with bottom_menu[1]:
        total_pages = (
            int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Página", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Página **{current_page}** de **{total_pages}** ")

    pages = split_frame(dataset, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)