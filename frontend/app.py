import requests
import pandas as pd
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Student Management",
    page_icon=":material/school:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state for navigation
if "current_section" not in st.session_state:
    st.session_state.current_section = "Add Student"

# Custom header with HTML
st.html("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        background: linear-gradient(90deg, #1f77b4 0%, #1557a0 100%);
        color: white;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .header-title {
        font-size: 24px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-nav {
        display: flex;
        gap: 8px;
    }
</style>
<div class="header-container">
    <div class="header-title">
        🎓 Student Management
    </div>
</div>
""")

# ── Navigation Menu ────────────────────────────────────────────────────────────
nav_container = st.container()
with nav_container:
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)

    with col_nav1:
        if st.button(":material/person_add: Add Student", use_container_width=True, key="nav_add"):
            st.session_state.current_section = "Add Student"

    with col_nav2:
        if st.button(":material/groups: View Students", use_container_width=True, key="nav_view"):
            st.session_state.current_section = "View Students"

    with col_nav3:
        if st.button(":material/search: Search", use_container_width=True, key="nav_search"):
            st.session_state.current_section = "Search Student"

    with col_nav4:
        if st.button(":material/edit: Update", use_container_width=True, key="nav_update"):
            st.session_state.current_section = "Update Student"

    with col_nav5:
        if st.button(":material/delete: Delete", use_container_width=True, key="nav_delete"):
            st.session_state.current_section = "Delete Student"

section = st.session_state.current_section
st.markdown("---")

# ── Add Student ────────────────────────────────────────────────────────────────
if section == "Add Student":
    st.header(":material/person_add: Add Student")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Student Information")
        sid = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, step=1)

    with col2:
        st.subheader("Contact & Course")
        course = st.text_input("Course")
        email = st.text_input("Email")

    st.markdown("---")
    col_submit, col_empty = st.columns([1, 4])
    with col_submit:
        if st.button(":material/check_circle: Add Student", use_container_width=True, key="btn_add_student"):
            payload = {"id": int(sid), "name": name, "age": int(age), "course": course, "email": email}
            try:
                r = requests.post(BACKEND_URL + "/students", json=payload)
                if r.status_code == 201:
                    st.success(":material/done: Student added successfully!")
                else:
                    detail = r.json().get("detail", r.text)
                    if isinstance(detail, list):
                        detail = "; ".join(d.get("msg", str(d)) for d in detail)
                    st.error(f":material/error: {detail}")
            except requests.exceptions.ConnectionError:
                st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")

# ── View Students ──────────────────────────────────────────────────────────────
elif section == "View Students":
    st.header(":material/groups: View Students")

    try:
        r = requests.get(BACKEND_URL + "/students")
        data = r.json()
        if data:
            df = pd.DataFrame(data)
            st.metric("Total Students", len(df))
            st.markdown("---")
            st.dataframe(df, use_container_width=True)
        else:
            st.info(":material/info: No students enrolled yet. Start by adding a new student!")
    except requests.exceptions.ConnectionError:
        st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")

# ── Search Student ─────────────────────────────────────────────────────────────
elif section == "Search Student":
    st.header(":material/search: Search Student")

    col1, col2 = st.columns([3, 1])
    with col1:
        sid = st.number_input("Student ID", min_value=1, step=1)

    with col2:
        st.markdown("")
        if st.button(":material/search: Search", use_container_width=True, key="btn_search_student"):
            try:
                r = requests.get(BACKEND_URL + f"/students/{int(sid)}")
                if r.status_code == 200:
                    s = r.json()
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.info(f":material/id_card: **ID:** {s['id']}")
                        st.info(f":material/person: **Name:** {s['name']}")
                        st.info(f":material/cake: **Age:** {s['age']}")
                    with col_b:
                        st.info(f":material/school: **Course:** {s['course']}")
                        st.info(f":material/email: **Email:** {s['email']}")
                elif r.status_code == 404:
                    st.warning(":material/person_search: Student not found.")
                else:
                    st.error(r.json().get("detail", r.text))
            except requests.exceptions.ConnectionError:
                st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")

# ── Update Student ─────────────────────────────────────────────────────────────
elif section == "Update Student":
    st.header(":material/edit: Update Student")

    col1, col2 = st.columns([3, 1])
    with col1:
        sid = st.number_input("Student ID", min_value=1, step=1, key="upd_sid")

    with col2:
        st.markdown("")
        if st.button(":material/search: Look up", use_container_width=True, key="btn_lookup_student"):
            try:
                r = requests.get(BACKEND_URL + f"/students/{int(sid)}")
                if r.status_code == 200:
                    st.session_state["upd_data"] = r.json()
                elif r.status_code == 404:
                    st.warning(":material/person_search: Student not found.")
                    st.session_state.pop("upd_data", None)
                else:
                    st.error(r.json().get("detail", r.text))
            except requests.exceptions.ConnectionError:
                st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")

    if "upd_data" in st.session_state:
        existing = st.session_state["upd_data"]
        st.markdown("---")
        st.subheader(":material/edit_note: Edit Student Information")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value=existing["name"])
            age = st.number_input("Age", min_value=1, step=1, value=existing["age"])

        with col2:
            course = st.text_input("Course", value=existing["course"])
            email = st.text_input("Email", value=existing["email"])

        col_save, col_cancel = st.columns([1, 4])
        with col_save:
            if st.button(":material/save: Save Changes", use_container_width=True, key="btn_save_changes"):
                payload = {"id": int(sid), "name": name, "age": int(age), "course": course, "email": email}
                try:
                    r = requests.put(BACKEND_URL + f"/students/{int(sid)}", json=payload)
                    if r.status_code == 200:
                        st.success(":material/done: Student updated successfully!")
                        st.session_state.pop("upd_data", None)
                    else:
                        detail = r.json().get("detail", r.text)
                        if isinstance(detail, list):
                            detail = "; ".join(d.get("msg", str(d)) for d in detail)
                        st.error(f":material/error: {detail}")
                except requests.exceptions.ConnectionError:
                    st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")

# ── Delete Student ─────────────────────────────────────────────────────────────
elif section == "Delete Student":
    st.header(":material/delete: Delete Student")

    st.warning(":material/warning: This action cannot be undone. Please proceed with caution.", icon="⚠️")

    col1, col2 = st.columns([3, 1])
    with col1:
        sid = st.number_input("Student ID", min_value=1, step=1)

    with col2:
        st.markdown("")
        if st.button(":material/delete_forever: Delete", use_container_width=True, type="primary", key="btn_delete_student"):
            try:
                r = requests.delete(BACKEND_URL + f"/students/{int(sid)}")
                if r.status_code == 200:
                    st.success(":material/done: Student deleted successfully.")
                elif r.status_code == 404:
                    st.warning(":material/person_search: Student not found.")
                else:
                    st.error(r.json().get("detail", r.text))
            except requests.exceptions.ConnectionError:
                st.error(":material/cloud_off: Cannot reach backend — is uvicorn running?")
