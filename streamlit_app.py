
import streamlit as st

st.set_page_config(
     page_title="Drug Risks / Riesgos de las Drogas",
     page_icon="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png",
     layout="centered", #centered wide
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/franasal/MCDA-drug-harms',
         'Report a bug': "https://github.com/franasal/MCDA-drug-harms",
         'About': "### Author: [franasa](https://twitter.com/franarsa/). \n @ViewsOnDrugsBot "
     }
 )

#app.py
import en_app
import es_app

PAGES = {
    "English": en_app,
    "Español": es_app
}
vod_icon=' [<img src="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png" alt="drawing" width="50"/>ViewsOnDrugsBot<img src="https://pbs.twimg.com/media/E1_0586WQAYCNym?format=png&name=small" alt="drawing" width="50"/>](https://twitter.com/ViewsOnDrugsBot/)'
st.sidebar.markdown(vod_icon,  unsafe_allow_html=True)
st.sidebar.markdown("### Language \ Idioma")
selection = st.sidebar.radio("",list(PAGES.keys()))
page = PAGES[selection]
page.main()
