import streamlit as st
import pandas as pd
import plotly.express as px

st.write('''
# US Vehicle Advertisement Listings
''')

# Read US vehicles sales advertisement into df
df = pd.read_csv('vehicles_us.csv')

# Pull the car make from the model column
def make_split(model):
    return model.split(' ')[0]
df['make'] = df['model'].apply(make_split)

# Due to few data points for mercedes-benz, remove from the data for this visualization
df = df.query("make != 'mercedes-benz'")

# Multi selection for which car brands to view data for the rest of the page
cars = st.multiselect("Select car brands to view data",
    ['All Makes', 'Acura', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Jeep', 'Kia', 'Nissan', 'Ram', 'Subaru', 'Toyota', 'Volkswagen'],
    ['Acura'])

# Creates query string to select on car makes from selection 
query_str = ""
if 'All Makes' in cars:
    selected_cars = df
else:
    for i, make in enumerate(cars):
        if i == 0:
            query_str = "make == " + '\'' + make.lower() + '\''
        else:
            query_str += " or make == " + '\'' + make.lower() + '\''
    # Filter dataframe on query string
    selected_cars = df.query(query_str)

# Normalize histograms by percent if checked
norm = st.checkbox('Normalize Data', False)
if norm:
    hnorm = 'percent'
else:
    hnorm = None

# Plotting days listed per car make
fig1 = px.histogram(selected_cars, x='days_listed', color='make', opacity=.8, nbins=100, histnorm=hnorm)
fig1.update_layout(xaxis_title_text='Days Listed')
st.header('Number of Days Listed for Sale by Car Brand')
st.plotly_chart(fig1, use_container_width=True)

# Plotting price per car make
fig2 = px.histogram(selected_cars, x='price', color='make', opacity=.8, range_x=[0, 150000], histnorm=hnorm)
fig2.update_layout(xaxis_title_text='Price')
st.header('Distribution of Prices by Car Brand')
st.plotly_chart(fig2, use_container_width=True)

# Plotting type of car
fig3 = px.histogram(selected_cars, x='type', color='make', opacity=.8, histnorm=hnorm)
fig3.update_layout(xaxis_title_text='Type of Vehicle')
st.header('Type of Vehicles by Car Brand')
st.plotly_chart(fig3, use_container_width=True)

# Scatter plot of odometer reading vs price
st.header('Odometer Reading vs Price')
trendline = st.checkbox('Add Trendline', False, key='t1')
# Toggle option to add trendline to data
if trendline:
    tline = 'ols'
else:
    tline = None

# Remove missing odometer rows in dataset
selected_cars_odometer = selected_cars.dropna(subset=['odometer'])
fig4 = px.scatter(selected_cars_odometer, x='odometer', y='price', color='make', symbol='make', trendline=tline)
fig4.update_layout(xaxis_title_text='Odometer Reading')
st.plotly_chart(fig4, use_container_width=True)

# Scatter plot of number of days listed vs price
st.header('Number of Days Listed for Sale vs Price')
trendline2 = st.checkbox('Add Trendline', False, key='t2')
# Toggle option to add trendline to data
if trendline2:
    tline2 = 'ols'
else:
    tline2 = None
fig5 = px.scatter(selected_cars, x='days_listed', y='price', color='make', symbol='make', trendline=tline2)
fig5.update_layout(xaxis_title_text='Days Listed')
st.plotly_chart(fig5, use_container_width=True)