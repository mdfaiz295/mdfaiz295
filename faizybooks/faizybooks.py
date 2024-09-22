import streamlit as st
import pandas as pd
import time


# Load the data
westbengal_data = pd.read_csv("Westbengal_Data.csv")
telangana_data = pd.read_csv("Telangana_Data.csv")
kerela_data = pd.read_csv("Kerala_Data.csv")
punjab_data = pd.read_csv("Punjab_Data.csv")
assam_data = pd.read_csv("KAAC_Data.csv")
southbengal_data = pd.read_csv("Southbengal_Data.csv")
andra_data=pd.read_csv(r"C:\Users\moham\vs code\guvi\project-1\faizybooks\apsrtc_Data.csv")
chandigarh_data=pd.read_csv(r"C:\Users\moham\vs code\guvi\project-1\faizybooks\ctu_Data.csv")
uttarpradesh_data=pd.read_csv(r"C:\Users\moham\vs code\guvi\project-1\faizybooks\upsrtc_Data.csv")
jammu_data=pd.read_csv(r"C:\Users\moham\vs code\guvi\project-1\faizybooks\jksrtc_Data.csv")

# Add a 'state' column to each DataFrame
chandigarh_data['state'] = 'Chandigarh'
westbengal_data['state'] = 'West Bengal'
andra_data['state'] = 'Andhra Pradesh'
punjab_data['state'] = 'Punjab'
assam_data['state'] = 'assam'
southbengal_data['state'] = 'South Bengal'
uttarpradesh_data['state'] = 'Bihar'
jammu_data['state'] = 'Jammu'
kerela_data['state'] = 'Kerala'
telangana_data['state'] = 'telangana'

# Combine the data into a single DataFrame and remove unnamed columns
all_data = pd.concat([chandigarh_data,westbengal_data,andra_data,punjab_data, assam_data, southbengal_data,uttarpradesh_data, jammu_data,telangana_data,kerela_data], ignore_index=True)
all_data = all_data.loc[:, ~all_data.columns.str.contains('^Unnamed')]
# App title
st.title("Faizybooks")
st.subheader("Book on a Click")  
# Sidebar filters
st.sidebar.title('click to fit!')
st.sidebar.header('🔍 find your bus')
state = st.sidebar.selectbox('Select State', all_data['state'].unique())
route = st.sidebar.selectbox('🚍Select Route', all_data[all_data['state'] == state]['route_name'].unique())
bus_type = st.sidebar.selectbox('🚌Select Bus Type', all_data[all_data['state'] == state]['bustype'].unique())
st.sidebar.header('⭐ Ratings & 💰 Pricing')
star_rating = st.sidebar.select_slider('⭐ Select Star Rating', options=[1, 2, 3, 4, 5])

min_price, max_price = st.sidebar.slider(
    '💰 Select Price Range',
    min_value=0, 
    max_value=1000, 
    value=(0, 1000)
)


# Show loading spinner
with st.spinner("🚍 Loading bus data..."):
    time.sleep(2)  # Simulate loading time (you can remove this in production)
# Filter data based on selections
filtered_data = all_data[
    (all_data['state'] == state) &
    (all_data['route_name'] == route) &
    (all_data['bustype'] == bus_type) &
    (all_data['star_rating'] == star_rating) &  # Use star_rating directly
    (all_data['price'] >= min_price) &
    (all_data['price'] <= max_price)]

# Display the filtered data
st.title('Bus Timings Data')
st.subheader('Filtered Bus Data')
st.dataframe(filtered_data)
# Check if the filtered data is empty
if filtered_data.empty:
    st.write("🚫 No buses available for the selected criteria.")
    # Show alternative data, e.g., highest rating for the same route and bus type
    alternative_data = all_data[
        (all_data['route_name'] == route) &
        (all_data['bustype'] == bus_type) &
        (all_data['price'] >= min_price) & 
        (all_data['price'] <= max_price)
    ]
    if not alternative_data.empty:
        st.write("Here are some alternative options:")
        # Sort by star rating to show the highest rating available
        alternative_data = alternative_data.sort_values(by='star_rating', ascending=False)
        st.dataframe(alternative_data)
    else:
        st.write("No alternative options available.")
else:
    # Display the filtered data if available
    st.title('Bus Timings Data')
    st.subheader('Filtered Bus Data')
    st.dataframe(filtered_data)
