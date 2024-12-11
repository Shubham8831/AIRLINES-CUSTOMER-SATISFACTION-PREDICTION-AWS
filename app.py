import streamlit as st
import pickle as pkl
import numpy as np

# now we load pre-trained model
with open('models/lgbm_model.pkl','rb') as file:
    loaded_model = pkl.load(file)


# define the ordinal mapping
ordinal_mapping = {
    0:"very poor",
    1:"poor",
    2:"average",
    3:"good",
    4:"excellent",
    5:"outstanding"
}

# define satisfaction mapping
satisfaction_mapping = { 0: 'neutral or dissatisfied', 1:'satisfied'}

#Function to convert user-friendly input back to numeric for prediction
def ordinal_to_numeric(input_value):
    reverse_mapping = {v: k for k,v in ordinal_mapping.items()}
    return reverse_mapping[input_value]

def predict_satisfaction(online_boarding, delay_ratio, inflight_wifi, passenger_class, travel_type, inflight_entertainment, flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness):
         
         x_new = np.array([[online_boarding, delay_ratio, inflight_wifi, passenger_class, travel_type, inflight_entertainment, flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness]])
         y_pred_new = loaded_model.predict(x_new)
         return y_pred_new



# Streamlit app title and layout
st.title("Flight Stisfaction Prediction")
st.markdown("**Gent instant prediction of flight satisfaction based on various factors.**")

#create two columns for a better layout
col1, col2 = st.columns(2)

# column 1 - collecting delay and distance info
with col1:
    st.header("Flight Information")

    arrival_delay = st.number_input("Arrival Delay (min.)",min_value=0.0, step=1.0,help="Total minutes flight was delayed upon arrival.")
    departure_delay = st.number_input("Departure Delay (min.)",min_value=0.0, step=1.0,help="Total minutes flight was delayed upon departure.")
    flight_distance = st.number_input("Flight Distance (km)",min_value=0.0,value=1000.0, step=1.0,help="Distance between departure and destination in kilometers.")

    #calculate total delay and delay ratio
    total_delay = arrival_delay + departure_delay
    delay_ratio = total_delay / (flight_distance+1) 

# column 2 - Collecting user preferences and flight service
with col2:
    st.header("Service Rating")

    inflight_wifi = st.selectbox("Inflight Wifi Service", list(ordinal_mapping.values()), help = "Rate the inflight WiFi service.")
    online_boarding = st.selectbox("Online Boarding", list(ordinal_mapping.values()), help = "Rate the online boarding process.")
    ease_online_booking = st.selectbox("Ease of Booking Flight", list(ordinal_mapping.values()), help = "Rate the ease of booking flight online.")
    seat_comfort = st.selectbox("Seat Comfort", list(ordinal_mapping.values()), help = "Rate comfort level of the seat.")
    inflight_entertainment = st.selectbox("Inflight Entertainment", list(ordinal_mapping.values()), help = "Rate the inflight entertainment options.")
    on_board_service = st.selectbox("On-board Service", list(ordinal_mapping.values()), help = "Rate the quality of on-board service.")
    leg_room_service = st.selectbox("Legroom Service", list(ordinal_mapping.values()), help = "Rate the legroom space during the flight.")
    cleanliness = st.selectbox("Cleanliness", list(ordinal_mapping.values()), help = "Rate the cleanliness of the flight environment.")


#convert ordinal inputs to numeric values
inflight_wifi_num = ordinal_to_numeric(inflight_wifi)
online_boarding_num = ordinal_to_numeric(online_boarding)
ease_online_booking_num = ordinal_to_numeric(ease_online_booking)
seat_comfort_num = ordinal_to_numeric(seat_comfort)
inflight_entertainment_num = ordinal_to_numeric(inflight_entertainment)
on_board_service_num = ordinal_to_numeric(on_board_service)
leg_room_service_num = ordinal_to_numeric(leg_room_service)
cleanliness_num = ordinal_to_numeric(cleanliness)

#organizing additional options in a horizontal layout
st.header("Additional Travel Information")

col3,col4 = st.columns(2)

with col3:
    passannger_class = st.selectbox("Class", ["Business","Eco", "Eco Plus"], help="Select the class of passanger travelling.")

with col4:
    travel_type = st.selectbox("Type of Travell", ["Business travel", "Personal Travel"], help = "Specify the purpose of your travel")


# convert class and travel type to numeric value
travel_type_mapping= {'Business travel': 0, 'Personal Travel': 1}
class_mapping  = {'Business': 0, 'Eco': 1, 'Eco Plus': 2}

passannger_class_num = class_mapping[passannger_class]
travel_type_num = travel_type_mapping[travel_type]

# Button to make the prediction
if st.button("Predict Satisfaction"):
    
    # make prediction
    prediction = predict_satisfaction(online_boarding_num, delay_ratio, inflight_wifi_num, passannger_class_num, travel_type_num, inflight_entertainment_num, flight_distance, seat_comfort_num, leg_room_service_num, on_board_service_num, ease_online_booking_num, cleanliness_num)

    # map the numeric prediction to the satisfaction label
    satisfaction_label = satisfaction_mapping[int(prediction[0])]

    # display the prediction with interactivity
    if satisfaction_label == 'satisfied':
         st.success(f"✅ **Prediction: {satisfaction_label.capitalize()}**")
    else:
         st.warning(f"✅ **Prediction: {satisfaction_label.capitalize()}**")