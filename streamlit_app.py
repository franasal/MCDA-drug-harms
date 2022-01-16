
import streamlit as st

st.set_page_config(
     page_title="Drug Risks / Riesgos de las Drogas",
     page_icon="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png",
     layout="wide", #centered wide
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/franasal/MCDA-drug-harms',
         'Report a bug': "https://github.com/franasal/MCDA-drug-harms",
         'About': "**App Author: [Francisco Arcila](https://twitter.com/franarsal/)** \n\nConcept design: Philine Edbauer, Francisco Arcila. \n\nTranslations: Philine Edbauer, Lukas Basedow."
     }
 )

#app.py
import en_app, es_app, de_app

PAGES = {
    "Deutsch": de_app,
    "English": en_app,
    "Español": es_app
}
vod_icon=' <img src="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png" alt="drawing" width="50"/>   -Know your Drugs-  <img src="https://pbs.twimg.com/media/E1_0586WQAYCNym?format=png&name=small" alt="drawing" width="50"/>'
st.sidebar.markdown(vod_icon,  unsafe_allow_html=True)
selection = st.sidebar.radio("",list(PAGES.keys()))
page = PAGES[selection]
page.main()
