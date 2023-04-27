import os
import streamlit as st
from PIL import Image
from io import BytesIO
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
from xlsxwriter import Workbook


logo_icon = Image.open("lib/images/logo.ico")
BACKGROUND_COLOR = 'white'
COLOR = 'black'


def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {color};
                    background-color: {background_color};
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )


def set_page_details():
    """
    Change Streamlit Page Settings 
    Hide MainMenu and footer, and reduce padding
    """
    st.set_page_config(page_title='AIction Hunter', page_icon=logo_icon)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    padding = 0
    st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


@st.cache
def convert_df(df):
    """
    Pandas dataframe to excel converter
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data


#def get_data_btw_dates(data, start_date end_date):
    


def search_btw_dates(data):
    """
    Search by store between dates logic
    """
    data_filtrada = None
    start_date = st.sidebar.date_input("Fecha inicio", st.session_state['start_date'])
    end_date = st.sidebar.date_input("Fecha fin", st.session_state['end_date'])
    if (end_date - start_date).days < 0:
        st.sidebar.error('La fecha de inicio deber ser menor o igual a la fecha fin')
    
    buscar_btw_dates = st.sidebar.button('Buscar por fechas')

    if buscar_btw_dates:
        st.session_state['b_pressed'] = True
        st.session_state['df_btw_dates'] = None

    if st.session_state['b_pressed']:
        st.session_state['start_date'] = start_date
        st.session_state['end_date'] = end_date

        with st.spinner(f"Buscando información de remates entre **{start_date}** y **{end_date}**. \nPor favor espere..."):
            data_filtrada = data[(data['date']>=start_date) & (data['date']<=end_date)]
            st.session_state['df_btw_dates'] = data_filtrada
    if  st.session_state['df_btw_dates'] is not None:
        st.subheader(f"Remates entre {st.session_state['start_date']} y {st.session_state['end_date']}")
        st.markdown('#')
        data_show = (
            data_filtrada[['Rol','Acreedor','Juzgado','Ciudad','Placa',
            'Marca','Modelo','Año','Color','Combustible','Martillero 1',
            'Martillero 2','Fecha Remate','Lugar Exhibición',
            'Fecha Exhibición','Lugar Remate','Comuna Remate','Garantía',
            'Sitio Web','Email','Fono 1','Fono 2']]
            .style
            .highlight_null(props="color: transparent;")  # hide NaNs
        )
        st.dataframe(data_show)
        
        if isinstance(data_filtrada, pd.DataFrame) and len(data_filtrada)>0:
            excel = convert_df(data_filtrada)
            st.download_button("Descargar data", excel, f"Remates_entre_{start_date}_y_{end_date}.xlsx", key='download-excel')


def main():
    
    set_page_details()
    set_page_container_style()
    st.markdown('# AIction Hunter (Demo)')

    data = pd.read_csv('lib/data.csv')
    data['Juzgado'] = data['Juzgado'].fillna(0)
    data = data.astype({'Juzgado':'int64', 'Garantía': 'Int64'})
    data['date'] = pd.to_datetime(data['Fecha Remate'].astype(str)).dt.date

    if 'b_pressed' not in st.session_state:
        st.session_state['b_pressed'] = False
    if 'df_btw_dates' not in st.session_state:
        st.session_state['df_btw_dates'] = None
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = datetime.now().date()
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = datetime.now().date() + timedelta(days=7)

    with st.sidebar:
        img_logo = Image.open("lib/images/logo.png")
        st.sidebar.image(img_logo)
        st.sidebar.markdown('#')
        st.sidebar.markdown("""---""")
        st.sidebar.header('Panel de búsqueda')
    
    search_btw_dates(data)
        

if __name__ ==  "__main__":
    main()
