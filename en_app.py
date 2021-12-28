import pandas as pd
import streamlit as st
import os
import json
import altair as alt
from pathlib import Path

lang="EN"


def load_data(lang):
    path_ = "./data/lang"

    lang_df = pd.read_csv(os.path.join(path_, f"{lang}.tsv"), sep = '\t')
    descriptions = lang_df[['VARIABLE','VARNAME','DESCRIPTION']].dropna().set_index('VARIABLE').T.to_dict("series")
    lab_names = lang_df[[f'__loc_dont_modify_', 'LABEL']].dropna().set_index('__loc_dont_modify_').to_dict()['LABEL']
    indexes=descriptions.keys()
    col_names = lang_df['DRUG'].dropna().tolist()
    data = pd.read_csv(os.path.join("./data/", "input_table.tsv"), header=None, sep = '\t', decimal=',').rename(columns=lang_df['DRUG'])

    data.index = list(indexes)
    data = data.reset_index().T
    data.columns = data.iloc[0]
    data.columns.name = "Category"
    data.drop('index', inplace=True)

    return data, descriptions, lab_names


transposed_df, categories, lab_names=load_data(lang)


def create_plot(sel_substances, sel_categories):

    plot_selection = transposed_df.loc[sel_substances, sel_categories]
    melted_df = pd.melt(plot_selection.reset_index(), id_vars=['index'])
    return melted_df

def main():
    drug_list = sorted(transposed_df.index.tolist())
    categories_list = sorted(transposed_df.columns.tolist())
    intro_markdown = Path(f"{lang.lower()}_info.md").read_text()
    st.markdown(intro_markdown, unsafe_allow_html=True)

    st.write("##")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"###  ① ** {lab_names['__select_d_title']}: **")
        st.text(f"{lab_names['__select_d_subt']}")
        substances = st.multiselect("", drug_list, [])
        st.markdown("#####  :pill: :candy: :broccoli: :tea: :mushroom: :snowflake: :smoking: :horse_racing::syringe: :wine_glass:")

    with col2:
        st.markdown(f"### ② **{lab_names['__select_c_title']}:**")
        st.text(f"{lab_names['__select_c_subt']}")
        sel_categories = st.multiselect("",categories_list, [])

    if substances and len(substances)>1:
        drug_list = substances
    if sel_categories:
        categories_list = [x for x in sel_categories]

        descripts = "\n\n".join([f"**{cat}** \n {categories[cat]['DESCRIPTION']}" for cat in sel_categories])

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


    foot = f'#### {lab_names["__foot"]}  [<img src="https://pbs.twimg.com/media/FGE5sFPX0AY6TtV?format=png&name=small"  alt="drawing" width="50"/>](https://mybrainmychoice.de/) [<img src="https://pbs.twimg.com/media/FGGjxH-XIAc101E?format=jpg&name=small" alt="drawing" width="50"/>](https://youthrise.org/) & [<img src="https://pbs.twimg.com/profile_images/1396102254487384065/ZjD8GvMw_400x400.png" alt="drawing" width="50"/> ViewsOnDrugs](https://twitter.com/ViewsOnDrugsBot/)'
    st.markdown(foot, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
