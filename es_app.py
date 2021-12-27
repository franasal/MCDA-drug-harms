import pandas as pd
import streamlit as st
import os
import json
import altair as alt
from pathlib import Path

lang="ES"

def load_data(lang):
    path_ = "./data/Input_drug_scores_Mulit_lan.xlsx"

    labels_df=pd.read_excel(path_, sheet_name=1)

    indexes=labels_df[f'{lang}_VARIABLE'].dropna().tolist()
    col_names=labels_df[f'{lang}_DRUG'].dropna().tolist()

    data=pd.read_excel(path_ , header=None, sheet_name='input_table').rename(index=str, columns=labels_df[f'{lang}_DRUG'])
    data.index = list(indexes)
    data.reset_index(inplace=True)
    descriptions = pd.read_excel(path_,sheet_name='descriptions')[[f'{lang}_VARIABLE',f'{lang}_VARNAME',f'{lang}_DESCRIPTION']].set_index(f'{lang}_VARIABLE').T.to_dict("series")


    return data.drop(16).T, descriptions


transposed_df, categories=load_data(lang)

transposed_df.columns = transposed_df.iloc[0]
transposed_df.columns.name = "Category"
transposed_df.drop('index', inplace=True)
transposed_df.drop('weight', inplace=True)
#create stacked bar chart



def create_plot(sel_substances, sel_categories):

    plot_selection = transposed_df.loc[sel_substances, sel_categories]
    melted_df=pd.melt(plot_selection.reset_index(), id_vars=['index'])
    return melted_df

def main():
    drug_list=sorted(transposed_df.index.tolist())
    categories_list = sorted(transposed_df.columns.tolist()[1:])
    intro_markdown = Path(f"{lang.lower()}_info.md").read_text()
    st.markdown(intro_markdown, unsafe_allow_html=True)

    st.write("##")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  ① ** Pick some Drugs: **")
        st.text("Select at least two substances")
        substances = st.multiselect("", drug_list, [])
        st.markdown("#####  :pill: :candy: :broccoli: :tea: :mushroom: :snowflake: :smoking: :horse_racing::syringe: :wine_glass:")

    with col2:
        st.markdown("### ② **Choose harm categories:**")
        sel_categories = st.multiselect("",categories_list, [])

    if substances and len(substances)>1:
        drug_list = substances
    if sel_categories:
        categories_list = [x for x in sel_categories]

        descripts= "\n\n".join([f"**{cat}** \n {categories[cat][f'{lang}_DESCRIPTION']}" for cat in sel_categories])

        descr_placeholder = st.empty()
        descr_placeholder.info(descripts)



    fig = alt.Chart(create_plot(drug_list, categories_list)).mark_bar().encode(
        x=alt.X('index', sort='-y', title=None),
        y=alt.Y('sum(value)', title=None),
        color=alt.Color('Category', scale=alt.Scale(scheme='dark2')
         )
        ).configure_legend(orient='bottom', columns=5, labelFontSize=10)


    # st.altair_chart(fig, use_container_width=True)
    chart_placeholder = st.empty()
    chart_placeholder.altair_chart(fig, use_container_width=True)


    foot = '#### A project by  [<img src="https://pbs.twimg.com/media/FGE5sFPX0AY6TtV?format=png&name=small"  alt="drawing" width="50"/>](https://mybrainmychoice.de/) [<img src="https://pbs.twimg.com/media/FGGjxH-XIAc101E?format=jpg&name=small" alt="drawing" width="50"/>](https://youthrise.org/) & [<img src="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png" alt="drawing" width="50"/> ViewsOnDrugs](https://twitter.com/ViewsOnDrugsBot/)'
    st.markdown(foot, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
