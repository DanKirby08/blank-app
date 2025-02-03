import streamlit as st
st.markdown("""
    <style>
        .header {
            background-color: pink;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title inside the pink strip
st.markdown('<div class="header">London house price analytics and Prediction</div>', unsafe_allow_html=True)

# Additional content
st.write("Welcome to the house price prediction tool. Enter your details below to predict the price of a house.")
import pydeck as pdk
from geopy.geocoders import Nominatim

# Function to get latitude and longitude from address
def geocode_address(address):
    geolocator = Nominatim(user_agent="house-price-predictor")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Streamlit user input for address
address = st.text_input("Enter an address in London:")

# If an address is entered, geocode it and show the map
if address:
    lat, lon = geocode_address(address)
    
    if lat and lon:
        # Create an interactive map with pydeck
        deck = pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=16.5,  # Adjust zoom level to control when the box is visible
                pitch=0
            ),
            layers=[ 
                pdk.Layer(
                    "ScatterplotLayer",
                    data=[{"latitude": lat, "longitude": lon}],
                    get_position=["longitude", "latitude"],
                    get_color=[255, 0, 0],  # Red color
                    get_radius=4,  # Dot radius set to 5
                ),
                pdk.Layer(
                    "TextLayer",  # Layer for the "Price" text and price in the same box
                    data=[{
                        "latitude": lat + 0.0001,  # Slightly above the dot
                        "longitude": lon, 
                        "text": "Price:\n£2,000,000"  # Both in the same box with a newline
                    }],
                    get_position=["longitude", "latitude"],
                    get_text="text",
                    get_size=16,  # Smaller text size
                    get_color=[255, 255, 255],  # White color for text
                    background_color=[255, 228, 196],  # Cream-white background
                    border_color=[255, 105, 180],  # Pink border
                    get_angle=0,
                    get_font_family="Arial",
                    get_font_weight=600,
                    pickable=True,
                ),
            ]
        )
        
        # Display the map
        st.pydeck_chart(deck)
        st.write(f"Showing the map for address: {address}")
    else:
        st.write("Sorry, we couldn't find that address. Please try again.")
else:
    st.write("Enter an address above to see the map.")


# Function to simulate fetching property details
def fetch_property_details(address):
    # Placeholder data, replace with actual data retrieval logic
    if address == "London":
        return {
            "previous_sales": [
                {"price": "£1,500,000", "date": "2020-05-12"},
                {"price": "£1,200,000", "date": "2017-07-21"}
            ],
            "bedrooms": 3,
            "bathrooms": 2,
            "days_on_market": 45
        }
    else:
        return None

# If an address is entered, fetch and display property details
if address:
    property_details = fetch_property_details(address)

    if property_details:
        # Display property details below the map
        st.write(f"### Property Details for {address}")
        st.write(f"**Bedrooms**: {property_details['bedrooms']}")
        st.write(f"**Bathrooms**: {property_details['bathrooms']}")
        st.write(f"**Days on Market**: {property_details['days_on_market']} days")
        st.write("**Previous Sales**:")
        for sale in property_details["previous_sales"]:
            st.write(f"- **Price**: {sale['price']} on **{sale['date']}**")
    else:
        st.write("Sorry, no property details available for this address.")

