from typing import Tuple
import streamlit as st
import pandas as pd
import altair as alt

from codex.utils import to_columnar
from codex.measure import measure_vars1, measure_vars2
from codex.collection import load_collection, get_width_height_pixels

STEPS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DEFAULT_SCENARIO_ID = 7
NUM_SCENARIOS = DEFAULT_SCENARIO_ID + 1


@st.cache
def load_data_frame(scenario_id: int,
                    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    # load the base matrix, and the callable that transforms it
    co_mat_original, transform = load_collection(scenario_id)

    steps1 = []
    props1 = []
    names1 = []
    steps2 = []
    props2 = []
    names2 = []
    transformations = []
    for step in STEPS:
        # transform matrix
        co_mat_transformed = transform(co_mat_original, step)

        # measure properties
        props1i, names1i = measure_vars1(co_mat_transformed)
        props2i, names2i = measure_vars2(co_mat_transformed)

        # collect for line chart 1
        steps1 += [step] * len(props1i)
        props1 += props1i
        names1 += names1i

        # collect for line chart 2
        steps2 += [step] * len(props2i)
        props2 += props2i
        names2 += names2i

        # collect transformed matrix for heat chart
        transformations.append(co_mat_transformed)

    df1 = pd.DataFrame(data={'Step': steps1, 'Proportion': props1, 'Quantity': names1})
    df2 = pd.DataFrame(data={'Step': steps2, 'Proportion': props2, 'Quantity': names2})
    df3 = pd.DataFrame(data=to_columnar(transformations))

    return df1, df2, df3


# sidebar
st.sidebar.title('Understanding Matrix Decomposition')
st.sidebar.write('Learn how measures related to matrix decomposition change as a function of matrix transformations.')
st.sidebar.write('There are multiple scenarios. '
                 'A scenario is defined by a toy co-occurrence matrix and a transformation '
                 'that subtracts from some elements in the matrix and adds to others, while keeping its sum constant.')
scenario_id = st.sidebar.selectbox('Select a scenario.',
                                   list(range(NUM_SCENARIOS)),
                                   DEFAULT_SCENARIO_ID)
st.sidebar.write('Use the slider to transform the matrix.')
current_step = st.sidebar.slider('Transformation step', 0, 10, 0)

st.sidebar.write("""
         This visualization is part of a research effort into the distributional structure of nouns in child-directed speech. 
         More info can be found at http://languagelearninglab.org/
     """)

# load data
df1, df2, df3 = load_data_frame(scenario_id)

# make line chart 1
chart1_y_label = 'Proportion of Joint Entropy'
df1.rename(columns={'Proportion': chart1_y_label}, inplace=True)
lines = alt.Chart(df1).mark_line().encode(x='Step',
                                          y=chart1_y_label,
                                          color='Quantity',
                                          tooltip=['Step', chart1_y_label, 'Quantity'])
rule = alt.Chart(pd.DataFrame([{'current_step': current_step}])).mark_rule(color='black').encode(
    x=alt.X('current_step', title='Step'))
line_chart1 = lines + rule

# make line chart 2
chart2_y_label = 'Proportion of Variance'
df2.rename(columns={'Proportion': chart2_y_label}, inplace=True)
lines = alt.Chart(df2).mark_line().encode(x='Step',
                                          y=chart2_y_label,
                                          color='Quantity',
                                          tooltip=['Step', chart2_y_label, 'Quantity'])
rule = alt.Chart(pd.DataFrame([{'current_step': current_step}])).mark_rule(color='black').encode(
    x=alt.X('current_step', title='Step')
)
line_chart2 = lines + rule

# make heat chart
heat_chart = alt.Chart(df3[df3['s'] == current_step]).mark_rect().encode(
    alt.X('x:O', axis=None),
    alt.Y('y:O', axis=None),
    color='z:Q'
).properties(
    width=get_width_height_pixels(scenario_id)[0],
    height=get_width_height_pixels(scenario_id)[1],
)

# show charts
st.header('Co-occurrence Data')
st.altair_chart(heat_chart)
col1, col2 = st.beta_columns(2)
with col1:
    st.header('Information Decomposition')
    st.altair_chart(line_chart1, use_container_width=True)
with col2:
    st.header('Singular Value Decomposition')
    st.altair_chart(line_chart2, use_container_width=True)