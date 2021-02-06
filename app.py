from typing import Tuple
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from PIL import Image

from grokkingsvd import configs
from grokkingsvd.utils import to_columnar
from grokkingsvd.measure import measure_vars1, measure_vars2
from grokkingsvd.transform import move_diag_to_col


STEPS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
MATRIX_SIZE_PX = 300


@st.cache
def load_data_frame() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    __ = 0
    _1 = 10
    _2 = 10
    _3 = 10
    co_mat_original = np.array([
        [_2, __, __, __, __, __],
        [__, _2, __, __, __, __],
        [__, __, _2, __, __, __],
        [__, __, __, _2, __, __],
        [__, __, __, __, _2, __],
        [__, __, __, __, __, _2],
    ])

    steps1 = []
    props1 = []
    names1 = []
    steps2 = []
    props2 = []
    names2 = []
    transformations = []
    for step in STEPS:
        # transform matrix
        co_mat_transformed = move_diag_to_col(co_mat_original, step)

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
st.sidebar.write("""
         Use the slider to inspect quantities computed on a toy co-occurrence matrix.
     """)
current_step = st.sidebar.slider('Transformation step', 0, 10, 0)

st.sidebar.write("""
         This visualization is part of a research effort into the distributional structure of nouns in child-directed speech. 
         More info can be found at http://languagelearninglab.org/
     """)
image = Image.open(configs.Dirs.images / 'lab_logo.png')
st.sidebar.image(image)

# load data
df1, df2, df3 = load_data_frame()

# make line chart 1
lines = alt.Chart(df1).mark_line().encode(x='Step',
                                          y='Proportion',
                                          color='Quantity',
                                          tooltip=['Step', 'Proportion', 'Quantity'])
rule = alt.Chart(pd.DataFrame([{"cs": current_step}])).mark_rule(color='black').encode(x='cs:Q')
line_chart1 = lines + rule

# make line chart 2
lines = alt.Chart(df2).mark_line().encode(x='Step',
                                          y='Proportion',
                                          color='Quantity',
                                          tooltip=['Step', 'Proportion', 'Quantity'])
rule = alt.Chart(pd.DataFrame([{"cs": current_step}])).mark_rule(color='black').encode(x='cs:Q')
line_chart2 = lines + rule

# make heat chart
heat_chart = alt.Chart(df3[df3['s'] == current_step]).mark_rect().encode(
    x='x:O',
    y='y:O',
    color='z:Q'
).properties(
    width=MATRIX_SIZE_PX,
    height=MATRIX_SIZE_PX
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