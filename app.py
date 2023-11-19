import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

df = pd.read_csv('vehicles_us.csv')

# print(df.info())  # 51,525 entries
# print(df['model_year'].isna().sum())

st.header('Vehicles For Sale')

st.write('It is not a functional application yet. Under construction.')

# st.write(df.info())


# fig.show()

fig_histogram = px.histogram(df, x="price", nbins=50)
# Histogram
st.plotly_chart(fig_histogram)

fig_scatter = px.scatter(df, x="model_year", y="price")
# Scatter Plot
st.plotly_chart(fig_scatter)

# st.checkbox


