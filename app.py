import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

df_vehicles_us = pd.read_csv('vehicles_us.csv')

# print(df.info())  # 51,525 entries
# print(df['model_year'].isna().sum())

st.header('Vehicles For Sale')

st.write('''
    It is not a functional application yet. 
    
    Under construction.

    ''')

# st.write(df.info())

fig_histogram = px.histogram(df_vehicles_us, x="price", nbins=50)
# fig.show()
# Histogram
st.plotly_chart(fig_histogram)

fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price")
# Scatter Plot
st.plotly_chart(fig_scatter)

def change_plot_args(column_x, column_y):  # pass different column names to change the x-values of the graphs
    #    clean up df_vehicles_us if it has null values
    df_nan_less = df_vehicles_us[~df_vehicles_us[column_x].isna()]
    #    fig_scatter = px.scatter(df_vehicles_us, x=column_x, y="price")
    vs_scatter = px.scatter(df_nan_less, x=column_x, y=column_y)  #, size="days_listed", color='make')
    st.plotly_chart(vs_scatter)



st.write('Choose the Scatter Plot')

yvp = st.checkbox("Year vs Price")
ovp = st.checkbox("Odometer vs Price")

if yvp:
    change_plot_args('model_year', 'price')
elif ovp:
    change_plot_args('odometer', 'price')
else:
    st.write('A scatter plot should appear HERE after clicking a checkbox.')

# cd /Documents/GitHub/vehicles_sprint4_proj
