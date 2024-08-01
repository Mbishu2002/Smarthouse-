import streamlit as st
import requests

# Define the base URL of your Flask API
API_BASE_URL = "http://localhost:5000"  

st.title("Smart Home Device Management")

# Function to fetch devices from the API
def fetch_devices():
    response = requests.get(f"{API_BASE_URL}/devices")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch devices")
        return []

# Function to add a new device
def add_device(name, status):
    response = requests.post(f"{API_BASE_URL}/devices", json={"name": name, "status": status})
    if response.status_code == 201:
        st.success("Device added successfully")
    else:
        st.error("Failed to add device: " + response.json().get('error', 'Unknown error'))

# Function to update device status
def update_device(id, status):
    response = requests.put(f"{API_BASE_URL}/devices/{id}", json={"status": status})
    if response.status_code == 200:
        st.success("Device status updated successfully")
    else:
        st.error("Failed to update device status")

# Function to delete a device
def delete_device(id):
    response = requests.delete(f"{API_BASE_URL}/devices/{id}")
    if response.status_code == 200:
        st.success("Device deleted successfully")
    else:
        st.error("Failed to delete device")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard", "Add Device", "Update Device Status", "Delete Device", "Connect Device"])

# Dashboard Page
if page == "Dashboard":
    st.header("Devices")
    devices = fetch_devices()
    for device in devices:
        st.write(f"**ID:** {device['id']}, **Name:** {device['name']}, **Status:** {device['status']}")

    # Visualization of devices
    st.subheader("Device Visualization")
    st.write("Visual representation of devices")

# Add Device Page
elif page == "Add Device":
    st.header("Add Device")
    with st.form(key='add_device_form'):
        name = st.text_input("Device Name")
        status = st.text_input("Device Status")
        submit_button = st.form_submit_button("Add Device")

        if submit_button and name and status:
            add_device(name, status)
            st.experimental_rerun()

# Update Device Status Page
elif page == "Update Device Status":
    st.header("Update Device Status")
    with st.form(key='update_device_form'):
        device_id = st.number_input("Device ID", min_value=1)
        new_status = st.text_input("New Device Status")
        update_button = st.form_submit_button("Update Status")

        if update_button and new_status:
            update_device(device_id, new_status)
            st.experimental_rerun()

# Delete Device Page
elif page == "Delete Device":
    st.header("Delete Device")
    with st.form(key='delete_device_form'):
        delete_id = st.number_input("Device ID to Delete", min_value=1)
        delete_button = st.form_submit_button("Delete Device")

        if delete_button:
            delete_device(delete_id)
            st.experimental_rerun()

# Connect Device Page
elif page == "Connect Device":
    st.header("Connect Device")
    connection_type = st.radio("Connection Type", ["Bluetooth", "Hotspot"])

    if connection_type == "Bluetooth":
        # Implement Bluetooth connection logic
        st.write("Bluetooth connection logic goes here.")
        if st.button("Connect via Bluetooth"):
            st.write("Initiating Bluetooth connection...")


    elif connection_type == "Hotspot":
        # Implement Hotspot connection logic
        st.write("Hotspot connection logic goes here.")
        if st.button("Connect via Hotspot"):
            st.write("Initiating Hotspot connection...")
