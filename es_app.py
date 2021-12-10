import pandas as pd
import streamlit as st
import os
import json
import altair as alt
from pathlib import Path



def load_data():
    path_ = "./data/Input_criterion_weights_and_drug_scores_Mulit_lan.xlsx"
    dataset = pd.read_excel(path_, sheet_name=2)
    descriptions = pd.read_excel(path_, sheet_name=3).to_dict("series")
    categories = {descriptions[x][0]:[descriptions[x][1], x]for x in descriptions}

    return dataset.drop(16).T, categories

transposed_2, categories=load_data()
transposed_2.columns = transposed_2.iloc[0]
transposed_2.columns.name = "Category"
transposed_2.drop('Unnamed: 0', inplace=True)
transposed_2.drop('peso', inplace=True)
#create stacked bar chart
drug_list=sorted(transposed_2.index.tolist())
categories_list = sorted(transposed_2.columns.tolist()[1:])


def create_plot(sel_substances, sel_categories):

    plot_selection = transposed_2.loc[sel_substances, sel_categories]
    melted_df=pd.melt(plot_selection.reset_index(), id_vars=['index'])
    return melted_df

def main():

    intro_markdown = Path("es_info.md").read_text()
    st.markdown(intro_markdown, unsafe_allow_html=True)

    st.write("##")
    col1, col2 = st.columns(2)

    end_drug_list = drug_list
    end_categories_list = categories_list

    with col1:
        st.markdown("###  ① ** Elije algunas Drogas: **")
        st.text("Selecciona por lo menos dos sustancias")
        substances = st.multiselect("", drug_list, [])
        st.markdown("#####  :pill: :candy: :broccoli: :tea: :mushroom: :snowflake: :smoking: :horse_racing::syringe: :wine_glass:")

    with col2:
        st.markdown("### ② **Selecciona categorías de Riesgos:**")
        sel_categories = st.multiselect("",categories.keys(), [])

    if substances and len(substances)>1:
        end_drug_list = substances
    if sel_categories:
        end_categories_list = [categories[x][1] for x in sel_categories]

        descripts= "\n\n".join([f"**{cat}** \n {categories[cat][0]}" for cat in sel_categories])

        descr_placeholder = st.empty()
        descr_placeholder.info(descripts)



    fig = alt.Chart(create_plot(end_drug_list, end_categories_list)).mark_bar().encode(
        x=alt.X('index', sort='-y', title=None),
        y=alt.Y('sum(value)', title=None),
        color=alt.Color('Category', scale=alt.Scale(scheme='dark2')
         )
        ).configure_legend(orient='bottom', columns=5, labelFontSize=10)


    # st.altair_chart(fig, use_container_width=True)
    chart_placeholder = st.empty()
    chart_placeholder.altair_chart(fig, use_container_width=True)


    foot = '#### Un proyecto desarrollado por [<img src="https://pbs.twimg.com/media/FGE5sFPX0AY6TtV?format=png&name=small"  alt="drawing" width="50"/>](https://mybrainmychoice.de/) [<img src="https://pbs.twimg.com/media/FGGjxH-XIAc101E?format=jpg&name=small" alt="drawing" width="50"/>](https://youthrise.org/) & [<img src="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png" alt="drawing" width="50"/> ViewsOnDrugs](https://twitter.com/ViewsOnDrugsBot/)'
    st.markdown(foot, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
