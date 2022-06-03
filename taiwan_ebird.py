import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from pydeck.types import String
from PIL import Image
import datetime


top_species = ('五色鳥', '八哥', '冠羽畫眉', '南亞夜鷹', '喜鵲', '埃及聖䴉', '夜鷺', 
'大冠鷲', '大卷尾', '大彎嘴', '大白鷺', '太平洋金斑鴴', '家八哥', '家燕', 
'小卷尾', '小啄木', '小彎嘴', '小水鴨', '小燕鷗', '小環頸鴴', '小白鷺', '小雲雀', '小青足鷸', '小鸊鷉', 
'巨嘴鴉', '斑文鳥', '斯氏繡眼', '東方環頸鴴', '東方黃鶺鴒', '棕扇尾鶯', '棕沙燕', '棕背伯勞', '棕面鶯', '樹鵲', '洋燕', '灰喉山椒鳥', '灰頭鷦鶯', '灰鶺鴒', '烏頭翁', '環頸雉', '田鷸', 
'白冠雞', '白尾八哥', '白尾鴝', '白環鸚嘴鵯', '白耳畫眉', '白腰文鳥', '白腹秧雞', '白腹鶇', '白頭翁', '白鶺鴒', 
'磯鷸', '紅冠水雞', '紅嘴黑鵯', '紅尾伯勞', '紅胸濱鷸', '紅隼', '紅頭山雀', '紅鳩', '綠畫眉', '繡眼畫眉', '翠鳥', 
'臺灣紫嘯鶇', '臺灣藍鵲', '蒼鷺', '藍磯鶇', '褐頭鷦鶯', '赤腰燕', '赤腹鶇', '赤足鷸', '野鴿', '金背鳩', '青背山雀', '青足鷸', 
'高蹺鴴', '魚鷹', '鳳頭蒼鷹', '鵲鴝', '鷹斑鷸', '鸕鷀', '麻雀', '黃尾鴝', '黃胸藪眉', '黃頭鷺', 
'黑冠麻鷺', '黑枕藍鶲', '黑翅鳶', '黑腹濱鷸', '黑腹燕鷗', '黑臉鵐', '黑面琵鷺', '黑領椋鳥', '黑鳶')

week_end_dict = dict()
for i in range(1,53):
    week_end_dict[i] = datetime.datetime.strptime("2013-W" + str(i) + "-1", "%Y-W%W-%w").strftime('%m-%d')


week_dict = {1: '01-01', 2: '01-08', 3: '01-15', 4: '01-22', 5: '01-29', 6: '02-05', 7: '02-12', 8: '02-19', 9: '02-26', 10: '03-05', 11: '03-12', 12: '03-19', 13: '03-26', 14: '04-02', 15: '04-09', 16: '04-16', 17: '04-23', 18: '04-30', 19: '05-07', 20: '05-14', 21: '05-21', 22: '05-28', 23: '06-04', 24: '06-11', 25: '06-18', 26: '06-25', 27: '07-02', 28: '07-09', 29: '07-16', 30: '07-23', 31: '07-30', 32: '08-06', 33: '08-13', 34: '08-20', 35: '08-27', 36: '09-03', 37: '09-10', 38: '09-17', 39: '09-24', 40: '10-01', 41: '10-08', 42: '10-15', 43: '10-22', 44: '10-29', 45: '11-05', 46: '11-12', 47: '11-19', 48: '11-26', 49: '12-03', 50: '12-10', 51: '12-17', 52: '12-24'}
week_end_dict = {1: '01-07', 2: '01-14', 3: '01-21', 4: '01-28', 5: '02-04', 6: '02-11', 7: '02-18', 8: '02-25', 9: '03-04', 10: '03-11', 11: '03-18', 12: '03-25', 13: '04-01', 14: '04-08', 15: '04-15', 16: '04-22', 17: '04-29', 18: '05-06', 19: '05-13', 20: '05-20', 21: '05-27', 22: '06-03', 23: '06-10', 24: '06-17', 25: '06-24', 26: '07-01', 27: '07-08', 28: '07-15', 29: '07-22', 30: '07-29', 31: '08-05', 32: '08-12', 33: '08-19', 34: '08-26', 35: '09-02', 36: '09-09', 37: '09-16', 38: '09-23', 39: '09-30', 40: '10-07', 41: '10-14', 42: '10-21', 43: '10-28', 44: '11-04', 45: '11-11', 46: '11-18', 47: '11-25', 48: '12-02', 49: '12-09', 50: '12-16', 51: '12-23', 52: '12-30'}

st.set_page_config(layout="wide")

# LOAD DATA ONCE
@st.experimental_singleton(show_spinner=False)
def load_data():
    data = pd.read_csv(
        "./taiwan_ebird_simple.csv.gz",
        names=[
            "lon",
            "lat",
            "species_name",
            "date",
            "day_of_year"
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        parse_dates=[
            "date"
        ],  # set as datetime instead of converting after the fact
        sep='\t'
    )

    data['week_of_year'] = data["date"].dt.isocalendar().week
    data = data[data['week_of_year']!=53]
    data['week_date'] = data['week_of_year'].apply(lambda i: week_dict[i])        
    return data


@st.experimental_singleton(show_spinner=False)
def group_by_species_week(data):
    df_group = data.groupby(['species_name','week_of_year'])
    return df_group


@st.experimental_singleton(show_spinner=False)
def group_by_species(data):
    df_group = data.groupby(['species_name'])
    return df_group


# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/outdoors-v11",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 0,
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    auto_highlight=True,
                    get_radius=1200,          # Radius is given in meters
                    get_fill_color=[255, 10, 51, 180],  # Set an RGBA value for fill
                    pickable=True),
            ],
        )
    )


# FILTER DATA BY WEEK / SPECIES
def filtered_data_specie_week(_df_group, specie, week):
    if specie in species_week_dict:
        if week in species_week_dict[specie]:
            return species_week_dict[specie][week]
    else:
        species_week_dict[specie] = dict()
    try:
        species_week_dict[specie][week] = _df_group.get_group((specie, week))
    except KeyError:
        species_week_dict[specie][week] = []
    return species_week_dict[specie][week]


@st.experimental_memo(show_spinner=False)
def filtered_data_specie(_df_group, specie):
    sdf = _df_group.get_group(specie)
    cnt_df = sdf.groupby('week_of_year', as_index=False)[['lon']].count() 
    cnt_df.columns = ['week_of_year', 'observations']
    return cnt_df


# STREAMLIT APP LAYOUT
data = load_data()
data_group = group_by_species_week(data)
species_week_dict = dict()

data_species = group_by_species(data)
taiwan_center = (23.6978, 120.9605)
zoom_level = 6.5
st.title("Taiwan eBird Data")
row1_1, row1_2, row1_3 = st.columns((10, 12, 16))


with row1_1:    
    specie_selected = st.selectbox(
        'Species',
        top_species)
    week_selected = st.slider('Week of year', 1, 52)
    date_range_str = week_dict[week_selected] + ' ~ ' + week_end_dict[week_selected]

    st.text(date_range_str)
with row1_2:
    image = Image.open('./bird_images/' + specie_selected + '.jpg')
    st.image(image, caption='Sunrise by the mountains')

with row1_3:
    specie_week_df = filtered_data_specie_week(data_group, specie_selected, week_selected)
    if len(specie_week_df) > 0:
        map(specie_week_df[['lat', 'lon']], taiwan_center[0], taiwan_center[1], zoom_level)


cnt_df = filtered_data_specie(data_species, specie_selected)

#### Plot volume chart
c = alt.Chart(cnt_df).mark_line().encode(x="week_of_year", y="observations")
mark_week_df = pd.DataFrame({'week_of_year':[week_selected], 'end': [week_selected+1]})
rect = alt.Chart(mark_week_df).mark_rect(opacity=0.5).encode(
    x='week_of_year',
    x2='end',
)

annotation_layer = (
    alt.Chart(pd.DataFrame({'week_of_year':[week_selected+2], 'y': [0]}))
    .mark_text(size=18, text=date_range_str, dx=0, dy=-5, align="center")
    .encode(
        x="week_of_year",
        y=alt.Y("y:Q"),
    )
)
st.altair_chart(
    (c + rect + annotation_layer).interactive(),
    use_container_width=True
)

# https://www.gbif.org/citation-guidelines
st.text('GBIF.org (01 June 2022) GBIF Occurrence Download https://doi.org/10.15468/dl.b4bmm5')
st.text('台灣鳥類網路圖鑑 https://today.to/tw/index-pc.html')
st.text('中華民國野鳥學會 https://www.bird.org.tw')
