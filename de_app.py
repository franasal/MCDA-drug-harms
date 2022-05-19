import pandas as pd
import streamlit as st
import os
import json
from pathlib import Path
import matplotlib.pyplot as plt

lang="DE"


def load_data(lang):
    path_ = "./data/lang"

    lang_df = pd.read_csv(os.path.join(path_, f"{lang}.tsv"), sep = '\t')
    descriptions = lang_df[['VARIABLE','VARNAME','DESCRIPTION']].dropna().set_index('VARNAME').T.to_dict("series")
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


data_df, categories, lab_names=load_data(lang)

def main():
    drug_list = sorted(data_df.index.tolist())
    categories_list = sorted(data_df.columns.tolist())
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

    data = data_df.loc[drug_list, categories_list ]
    plt.style.use(['dark_background'])
    s = data.sum(axis=1)
    plot_df=data.T[s.sort_values(ascending=False).index].T

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1))
    plot_df.plot(ax=ax,kind='bar', stacked=True, rot=0)
    vals = ax.get_yticks()
    ax.xaxis.grid(False)
    ax.yaxis.grid(linestyle='-.', linewidth=.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.xticks(rotation = 70, ha="right")
    plt.title(f"{lab_names['__graph_tittle']}")

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3),
              fancybox=True, shadow=True, ncol=3)
    chart_placeholder = st.empty()
    chart_placeholder.pyplot(plt, use_container_width=True)


    foot = f'#### {lab_names["__foot"]}  [<img src="https://pbs.twimg.com/media/FGE5sFPX0AY6TtV?format=png&name=small"  alt="drawing" width="50"/>](https://mybrainmychoice.de/)'
    st.markdown(foot, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
