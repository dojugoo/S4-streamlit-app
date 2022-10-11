import streamlit as st
import pandas as pd
import plotly.express as px


st.write('''
# US Vehicle Advertisement Listings
''')

cars = st.multiselect("Select car brands to view data",
    ['Acura', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Jeep', 'Kia', 'Mercedes-Benz', 'Nissan', 'Ram', 'Subaru', 'Toyota', 'Volkswagen'],
    ['Acura'])

# Creates query string to select on car makes from selection 
query_str = ""
for i, make in enumerate(cars):
    if i == 0:
        query_str = "make == " + '\'' + make.lower() + '\''
    else:
        query_str += " or make == " + '\'' + make.lower() + '\''

# Read US vehicles sales advertisement into df
df = pd.read_csv('vehicles_us.csv')

# Pull the car make from the model column
def make_split(model):
    return model.split(' ')[0]
df['make'] = df['model'].apply(make_split)

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