import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
def initialize_appointments():
    return pd.DataFrame(columns=["Pet Name", "Appointment Date", "Appointment Time"])

if "booked_appointments" not in st.session_state:
    st.session_state.booked_appointments = initialize_appointments()
def hide_streamlit_style():
    hide_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_style, unsafe_allow_html=True)


def home_page():
 
    logo_path = "logo.jpg" 
    st.image(logo_path, width=200, caption="Pet Clinic ")
    st.title("Welcome to the Pet Clinic App!")
    st.subheader("Our Services:")
    services = ["Vaccinations", "Check-ups", "Surgery", "Dental Care", "Emergency Care"]
    st.markdown("> - " + "\n> - ".join(services))
    user_pet_name = st.text_input("Enter your pet's name:")
    appointment_date = st.date_input("Select appointment date:")
    appointment_time = st.time_input("Select appointment time:")

    if st.button("Schedule Appointment"):
        new_appointment = pd.DataFrame([[user_pet_name, appointment_date, appointment_time]],
                                        columns=["Pet Name", "Appointment Date", "Appointment Time"])
        st.session_state.booked_appointments = pd.concat([st.session_state.booked_appointments, new_appointment],
                                                         ignore_index=True)
        st.success(f"Appointment scheduled for {user_pet_name} on {appointment_date} at {appointment_time}")


def appointments_page():
   
    st.title("Booked Appointments")
    st.table(st.session_state.booked_appointments)

def edit_appointments_page():
    st.title("Edit Appointments")
    st.table(st.session_state.booked_appointments)
    appointment_to_edit = st.text_input("Enter the Pet Name to edit:")
    appointment_index = st.session_state.booked_appointments.index[
        st.session_state.booked_appointments["Pet Name"] == appointment_to_edit
    ].tolist()

    if appointment_index:
        new_date = st.date_input("Enter new appointment date:")
        new_time = st.time_input("Enter new appointment time:")

        if st.button("Edit Appointment"):
            st.session_state.booked_appointments.at[appointment_index[0], "Appointment Date"] = new_date
            st.session_state.booked_appointments.at[appointment_index[0], "Appointment Time"] = new_time
            st.success(f"Appointment details edited for {appointment_to_edit}")

    else:
        st.warning(f"No appointment found for {appointment_to_edit}")



def analytics_page():
    st.title("Analytics - Appointments Insights")

    if not st.session_state.booked_appointments.empty:
        st.session_state.booked_appointments["Appointment DateTime"] = pd.to_datetime(
            st.session_state.booked_appointments["Appointment Date"].astype(str) +
            " " +
            st.session_state.booked_appointments["Appointment Time"].astype(str)
        )
        fig_count_by_date = px.histogram(st.session_state.booked_appointments, x="Appointment Date",
                                         title="Appointment Count by Date",
                                         labels={"Appointment Date": "Date", "count": "Appointment Count"})
        st.plotly_chart(fig_count_by_date)

        fig_time_distribution = px.pie(st.session_state.booked_appointments,
                                       names="Appointment Time",
                                       title="Appointment Time Distribution")
        st.plotly_chart(fig_time_distribution)
        fig_time_series = px.line(st.session_state.booked_appointments,
                                  x="Appointment DateTime",
                                  title="Appointment Count Over Time")
        st.plotly_chart(fig_time_series)

        max_appointment = st.session_state.booked_appointments.loc[
            st.session_state.booked_appointments["Appointment DateTime"].idxmax()
        ]

        st.subheader("Maximum Appointment Details:")
        st.write(max_appointment[["Pet Name", "Appointment Date", "Appointment Time"]])

    else:
        st.warning("No booked appointments for analytics.")


hide_streamlit_style()
# page = st.sidebar.selectbox("Select Page", ["Home", "Appointments", "Edit Appointments", "Analytics"])

page = option_menu(
    menu_title=None,
    options=["Home", "Appointments", "Edit Appointments", "Analytics"],
    icons=["🐶Clinic", "📋","📝","📑"],
    orientation="horizontal",
    
)
if page == "Home":
    home_page()
elif page == "Appointments":
    appointments_page()
elif page == "Edit Appointments":
    edit_appointments_page()
elif page == "Analytics":
    analytics_page()

