import pandas as pd
import streamlit as st
import os
import json
import altair as alt
from pathlib import Path

# st.title(':bar_chart: COMPARE DRUG HARMS :mag:')
st.markdown("## **[David Nutt's dangerous drug list](https://www.theguardian.com/science/2009/nov/02/david-nutt-dangerous-drug-list)**")


intro_markdown = Path("README.md").read_text()
st.markdown(intro_markdown, unsafe_allow_html=True)


with open('./data/drug_categories.json', 'r') as json_file:
    categories=json.load(json_file)


@st.cache
def load_data():
    path_base = "./data/"
    datasets_dict = {}
    for csv_f in os.listdir(path_base):
        if csv_f.endswith("csv"):
            dataname = csv_f.split(".csv")[0].strip().replace(" ", "_")
            datasets_dict[dataname] = pd.read_csv(os.path.join(path_base, csv_f),
             sep = "\t", index_col=None)
    return datasets_dict


datasets_dict = load_data()
# display(datasets_dict['Input_criterion_weights_and_drug_scores'])
transposed_2=datasets_dict['Input_criterion_weights_and_drug_scores'].drop(16).T

transposed_2.columns = transposed_2.iloc[0]
transposed_2.columns.name = "Category"
transposed_2.drop('Unnamed: 0', inplace=True)
transposed_2.drop('weight', inplace=True)
#create stacked bar chart
drug_list=sorted(transposed_2.index.tolist())
categories_list = sorted(transposed_2.columns.tolist()[1:])


def create_plot(sel_substances, sel_categories):

    plot_selection = transposed_2.loc[sel_substances, sel_categories]
    melted_df=pd.melt(plot_selection.reset_index(), id_vars=['index'])
    return melted_df

def main():

    end_drug_list = drug_list
    end_categories_list = categories_list

    chart_placeholder = st.empty()
    descr_placeholder = st.empty()
    st.markdown("###  ① ** Let's pick some Drugs: **")
    substances = st.multiselect("", drug_list, []
    )

    st.markdown("### ② **Let's choose some categories:**")
    sel_categories = st.multiselect("",categories.keys(), []
    )

    if substances:
        end_drug_list = substances
    if sel_categories:
        end_categories_list = [categories[x][1] for x in sel_categories]

        descripts= "\n\n".join([f"**{cat}** \n {categories[cat][0]}" for cat in sel_categories])

        descr_placeholder.markdown(descripts)



    fig = alt.Chart(create_plot(end_drug_list, end_categories_list)).mark_bar().encode(
        x=alt.X('index', sort='-y', title=None),
        y=alt.Y('sum(value)', title=None),
        color=alt.Color('Category', scale=alt.Scale(scheme='dark2')
         )
        ).configure_legend(orient='right')


    # st.altair_chart(fig, use_container_width=True)

    chart_placeholder.altair_chart(fig, use_container_width=True)

    st.markdown("## :diamond_shape_with_a_dot_inside: :smoking: :pill: :syringe: :wine_glass: :candy:")


if __name__ == "__main__":
    main()
