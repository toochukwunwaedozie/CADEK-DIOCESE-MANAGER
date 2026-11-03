import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="CADEK Diocese Manager", page_icon="⛪", layout="wide")

# === CONFIG ===
ADMIN_PASSWORD = "CADEK2024"  # <-- CHANGE THIS to your own password

# === SIDEBAR LOGIN ===
def is_admin():
    return st.session_state.get("password_correct", False)

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

with st.sidebar:
    st.title("⛪ CADEK Menu")
    menu = st.selectbox("Menu", ["Dashboard", "Parishes - View", "Parishes - Edit", "Personnel", "Yearly Activities", "Add New"])
    
    st.divider()
    st.subheader("🔐 Admin")
    if is_admin():
        st.success("Admin logged in ✅")
        if st.button("Logout"):
            st.session_state["password_correct"] = False
            st.rerun()
    else:
        pwd = st.text_input("Password to Edit", type="password")
        if st.button("Login to Edit"):
            if pwd == ADMIN_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.caption("Public can view, only admin can edit")

# === DATA ===
if "parishes" not in st.session_state:
    st.session_state.parishes = [{"name":"St peters catholic church oko","location":"oko","priest_in_charge":"very rev fr. prof chiegboka","phone":"09036705243"}]
if "personnel" not in st.session_state:
    st.session_state.personnel = []
if "activities" not in st.session_state:
    st.session_state.activities = []

st.title("⛪ CADEK Diocese Management")
st.caption("Catholic Diocese of Ekwulobia - Parishes & Activities")

# === PAGES ===
if menu == "Dashboard":
    c1,c2,c3 = st.columns(3)
    c1.metric("Parishes", len(st.session_state.parishes))
    c2.metric("Personnel", len(st.session_state.personnel))
    c3.metric("Activities", len(st.session_state.activities))
    st.info("Public can view all pages. Login in sidebar to edit/add.")

elif menu == "Parishes - View":
    st.subheader("All Parishes (Public View)")
    if st.session_state.parishes:
        st.dataframe(pd.DataFrame(st.session_state.parishes), use_container_width=True)
    else:
        st.info("No parish yet")

elif menu == "Parishes - Edit":
    st.subheader("Edit Parishes")
    if not is_admin():
        st.warning("🔒 Please login as Admin in sidebar to edit")
        if st.session_state.parishes:
            st.dataframe(pd.DataFrame(st.session_state.parishes), use_container_width=True)
        st.stop()
    
    if st.session_state.parishes:
        df = pd.DataFrame(st.session_state.parishes)
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="parish_editor")
        if st.button("💾 Save Changes"):
            st.session_state.parishes = edited.to_dict("records")
            st.success("Priest information updated!")
    else:
        st.info("No parish yet - Go to Add New")

elif menu == "Personnel":
    st.subheader("Personnel")
    if st.session_state.personnel:
        df = pd.DataFrame(st.session_state.personnel)
        if is_admin():
            edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="pers_editor")
            if st.button("Save Personnel Changes"):
                st.session_state.personnel = edited.to_dict("records")
                st.success("Updated!")
        else:
            st.dataframe(df, use_container_width=True)
            st.info("Login to edit")
    else:
        st.info("No personnel yet - Go to Add New")

elif menu == "Yearly Activities":
    st.subheader("Yearly Activities")
    if st.session_state.activities:
        df = pd.DataFrame(st.session_state.activities)
        if is_admin():
            edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="act_editor")
            if st.button("Save Activities"):
                st.session_state.activities = edited.to_dict("records")
                st.success("Saved!")
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No activities yet")

elif menu == "Add New":
    if not is_admin():
        st.warning("🔒 Admin login required to add new data. Login in sidebar.")
        st.stop()
    
    tab1,tab2,tab3 = st.tabs(["Add Parish", "Add Personnel", "Add Activity"])
    with tab1:
        name = st.text_input("Parish Name")
        loc = st.text_input("Location")
        priest = st.text_input("Priest in Charge")
        phone = st.text_input("Phone")
        if st.button("Save Parish"):
            if name:
                st.session_state.parishes.append({"name":name,"location":loc,"priest_in_charge":priest,"phone":phone})
                st.success(f"{name} saved!")
            else:
                st.error("Enter parish name")
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
