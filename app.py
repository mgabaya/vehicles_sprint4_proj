import pandas as pd
import streamlit as st
import plotly.express as px
# import altair as alt

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

# Pivot Tables
pt_make_type = df_vehicles_us.groupby(['make', 'type'])['price'].mean().reset_index()
pt_make_type_odom = df_vehicles_us.groupby(['make', 'type'])['odometer'].mean().reset_index()
# Merge Pivot Tables
cars_merge = pt_make_type.merge(pt_make_type_odom, on=['make', 'type'], how='outer')

######----- Begin streamlit code -----######

st.header('Vehicles For Sale')

st.write('''
    This dashboard app allows you to view and compare the different auto makers prices for their used cars. 
    
    Some graphs have added features. Select the checkboxes to enhance the charts.

    ''')

# create a text header above the dataframe
st.header('Data viewer')
# display the dataframe with streamlit
st.dataframe(df_vehicles_us)

#### CHECKBOX IDEAS
# Show makers
# Select size by days_listed or odometer

# Scatter Plot
st.write('''
    The Scatter Plot below shows compares the model year and price of used cars in our data set.
    
    To add sizing to each dot according to the number of days listed and coloring each dot by maker, click the checkbox below
''')

enhanced = st.checkbox("Enhance the plot")  #, on_change=show_scatter())
#color_make = st.checkbox("Show Vehicle Make by Color")  #, on_change=show_scatter())
# def show_scatter():
#     if size_days_listed:
#         fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price", size="days_listed")
#     elif color_make:
#         fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price", color='make')
#     elif size_days_listed & color_make:
#         fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price", size="days_listed", color='make')
#     else:
#         fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price")
if enhanced:
    fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price", size="days_listed", color='make')
else:
    fig_scatter = px.scatter(df_vehicles_us, x="model_year", y="price")
fig_scatter.update_layout(
    title_text='Pricing by Year',  # title of plot
    xaxis_title_text='Model Year',  # xaxis label
    yaxis_title_text='Price $USD',  # yaxis label
)
st.plotly_chart(fig_scatter)


st.write('''
    Customize the Histogram #2
    
    There were a few extremely expensive cars for sale. We provided a checkbox 
    to see what it would look like without these values.
    ''')

outliers = st.checkbox("Without the Extreme Values")
if outliers:
    with_or_without = df_vehicles_us[df_vehicles_us['price']<=100000]
else:
    with_or_without = df_vehicles_us
pt_histogram = px.histogram(with_or_without, x='price', color='make', barmode="overlay", nbins=30)  # add checkboxes to show color make and hover type
pt_histogram.update_layout(
    title_text='Price For Used Cars', # title of plot
    xaxis_title_text='Price $', # xaxis label
    yaxis_title_text='Count', # yaxis label
)
st.plotly_chart(pt_histogram)

# def change_plot_args(column_x, column_y):  # pass different column names to change the x-values of the graphs
#     #    clean up df_vehicles_us if it has null values
#     df_nan_less = df_vehicles_us[~df_vehicles_us[column_x].isna()]
#     #    fig_scatter = px.scatter(df_vehicles_us, x=column_x, y="price")
#     vs_scatter = px.scatter(df_nan_less, x=column_x, y=column_y)  #, size="days_listed", color='make')
#     st.plotly_chart(vs_scatter)

# yvp = st.checkbox("Year vs Price")
# ovp = st.checkbox("Odometer vs Price")
#
# if yvp:
#     change_plot_args('model_year', 'price')
# elif ovp:
#     change_plot_args('odometer', 'price')
# else:
#     st.write('A scatter plot should appear HERE after clicking a checkbox.')

# cd /Documents/GitHub/vehicles_sprint4_proj

# Added 8/16/24
st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df_vehicles_us['make'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('bmw'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df_vehicles_us['make'] == manufacturer_1) | (df_vehicles_us['make'] == manufacturer_2)
df_filtered = df_vehicles_us[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))
