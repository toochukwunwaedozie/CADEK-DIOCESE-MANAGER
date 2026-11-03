import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="CADEK Diocese Manager", page_icon="⛪", layout="wide")
st.title("⛪ CADEK Diocese Management")
st.caption("Catholic Diocese of Ekwulobia - Parishes & Activities")

if "parishes" not in st.session_state:
    st.session_state.parishes = []
if "personnel" not in st.session_state:
    st.session_state.personnel = []
if "activities" not in st.session_state:
    st.session_state.activities = []

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Parishes", "Personnel", "Yearly Activities", "Add New"])

if menu == "Dashboard":
    c1,c2,c3 = st.columns(3)
    c1.metric("Parishes", len(st.session_state.parishes))
    c2.metric("Personnel", len(st.session_state.personnel))
    c3.metric("Activities", len(st.session_state.activities))
    if st.session_state.activities:
        st.dataframe(pd.DataFrame(st.session_state.activities))

elif menu == "Parishes":
    if st.session_state.parishes:
        st.dataframe(pd.DataFrame(st.session_state.parishes))
    else:
        st.info("No parish yet - Go to Add New")

elif menu == "Personnel":
    if st.session_state.personnel:
        st.dataframe(pd.DataFrame(st.session_state.personnel))
    else:
        st.info("No personnel yet")

elif menu == "Yearly Activities":
    if st.session_state.activities:
        df = pd.DataFrame(st.session_state.activities)
        st.dataframe(df.sort_values("date"))
    else:
        st.info("No activities yet")

elif menu == "Add New":
    tab1,tab2,tab3 = st.tabs(["Add Parish", "Add Personnel", "Add Activity"])
    with tab1:
        name = st.text_input("Parish Name")
        loc = st.text_input("Location")
        priest = st.text_input("Priest in Charge")
        phone = st.text_input("Phone")
        if st.button("Save Parish"):
            st.session_state.parishes.append({"name":name,"location":loc,"priest_in_charge":priest,"phone":phone})
            st.success(f"{name} saved!")
    with tab2:
        name = st.text_input("Person Name", key="pn")
        role = st.selectbox("Role", ["Parish Priest","Assistant Priest","Catechist","Secretary","Youth Leader","Other"])
        parish = st.text_input("Parish", key="pp")
        if st.button("Save Personnel"):
            st.session_state.personnel.append({"name":name,"role":role,"parish":parish})
            st.success("Saved!")
    with tab3:
        title = st.text_input("Activity Title")
        parish = st.text_input("Parish Involved", key="ap")
        d = st.date_input("Date", value=date.today())
        atype = st.selectbox("Type", ["Sunday Mass","Feast Day","Harvest","Youth Week","Meeting","Other"])
        if st.button("Save Activity"):
            st.session_state.activities.append({"title":title,"parish":parish,"date":str(d),"type":atype})
            st.success("Activity added!")
