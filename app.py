import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

df_vehicles_us = pd.read_csv('vehicles_us.csv')

# function for replacing implicit duplicates
def replace_wrong_models(wrong_models, correct_models):
    for wrong_model in wrong_models:
        df_vehicles_us['model'] = df_vehicles_us['model'].replace(wrong_models, correct_models)

# removing implicit duplicates
duplicates_f_150 = ['ford f150']
duplicates_f_250 = ['ford f250']
duplicates_f_250_sd = ['ford f-250 sd', 'ford f250 super duty']
duplicates_f_350_sd = ['ford f350 super duty', 'ford f-350 sd']
replace_wrong_models(duplicates_f_150, 'ford f-150')
replace_wrong_models(duplicates_f_250, 'ford f-250')
replace_wrong_models(duplicates_f_250_sd, 'ford f-250 super duty')
replace_wrong_models(duplicates_f_350_sd, 'ford f-350 super duty')

# string to lowercase for type
df_vehicles_us['type'] = df_vehicles_us['type'].str.lower()
# to_datetime: date_posted
df_vehicles_us['date_posted'] = pd.to_datetime(df_vehicles_us['date_posted'], format='%Y-%m-%d')
# For paint_color, we will change the color to 'unknown'
df_vehicles_us['paint_color'] = df_vehicles_us['paint_color'].fillna('unknown')
# For is_4wd, we will change the null values to 0, since 1 represents that a four wheel drive (4WD) car.
df_vehicles_us['is_4wd'] = df_vehicles_us['is_4wd'].fillna(0)

# Make a model make column
df_vehicles_us['make'] = df_vehicles_us['model'].str.split().str[0]

# Remove duplicated mbz rows
mbz_index = df_vehicles_us[df_vehicles_us['model'] == 'mercedes-benz benze sprinter 2500'].index.tolist()
df_vehicles_us.drop(mbz_index[1: ], inplace=True)

# print(df_vehicles_us.info())  # 51,525 entries

st.header('Vehicles For Sale')

st.write('''
    It is not a functional application yet. 
    
    Under construction.

    ''')

# create a text header above the dataframe
st.header('Data viewer')
# display the dataframe with streamlit
st.dataframe(df_vehicles_us)


fig_histogram = px.histogram(df_vehicles_us, x="price", nbins=50)
# fig.show()
# Histogram
st.plotly_chart(fig_histogram)

fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price", size="days_listed", color='make')
fig_scatter.update_layout(
    title_text='Pricing by Year', # title of plot
    xaxis_title_text='Model Year', # xaxis label
    yaxis_title_text='Price $USD', # yaxis label
)
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
