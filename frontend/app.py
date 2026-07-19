import streamlit as st
from PIL import Image
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
import io

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="RoadPulse",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:1rem;
}

.hero{
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    padding:30px;
    border-radius:18px;
    color:white;
}

.metric-card{
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    border-radius:15px;
    padding:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1);
    text-align:center;
}

.report-card{
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    padding:18px;
    border-radius:12px;
    margin-bottom:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.sidebar .sidebar-content{
    background:#0F172A;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("RoadPulse")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Report Issue",
        "Reports",
        "Analytics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "AI Powered Road Intelligence"
)

# -----------------------------
# Dashboard
# -----------------------------
if page == "Dashboard":

    st.markdown("""
    <div class='hero'>
    <h1>RoadPulse</h1>

    AI Powered Traffic & Road Infrastructure Intelligence

    Report potholes, waterlogging,
    accidents and blocked roads in
    real time.
    </div>
    """,
    unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class='metric-card'>
        <h2>120</h2>
        <p>Total Reports</p>
        </div>
        """,
        unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='metric-card'>
        <h2>45</h2>
        <p>Pending</p>
        </div>
        """,
        unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='metric-card'>
        <h2>68</h2>
        <p>Resolved</p>
        </div>
        """,
        unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class='metric-card'>
        <h2>7</h2>
        <p>Critical</p>
        </div>
        """,
        unsafe_allow_html=True)

    st.write("")

    st.subheader("Recent Activity")

    st.markdown("""
    <div class='report-card'>
    🚧 Large pothole detected near City Mall
    <br><br>
    Department : Road Department
    <br>
    Status : Pending
    </div>
    """,
    unsafe_allow_html=True)

    st.markdown("""
    <div class='report-card'>
    🚦 Traffic signal failure
    <br><br>
    Department : Traffic Police
    <br>
    Status : Assigned
    </div>
    """,
    unsafe_allow_html=True)

    st.markdown("""
    <div class='report-card'>
    🌊 Waterlogging reported
    <br><br>
    Department : Drainage Department
    <br>
    Status : Pending
    </div>
    """,
    unsafe_allow_html=True)

    # =====================================
# REPORT ISSUE PAGE
# =====================================

elif page == "Report Issue":

    st.title("Report Road Issue")

    st.write(
        "Upload a road image and provide location details. "
        "AI will analyze the issue automatically."
    )

    st.divider()


    # -------------------------
    # Image Upload
    # -------------------------

uploaded_image = st.file_uploader("Upload Road Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # 1. Open and display the image in Streamlit (this moves the internal file pointer)
    img_bytes = uploaded_image.getvalue()
    
    image = Image.open(io.BytesIO(img_bytes))
    
    # 🌟 FIX: Swapped out 'use_container_width=True' for 'width="stretch"' 
    # This immediately stops that warning flood in your console log terminal!
    st.image(
        image,
        caption="Uploaded Road Image",
        width="stretch" 
    )
    
    # 2. Add your submission button
    if st.button("Submit Report to RoadPulse AI"):
        uploaded_image.seek(0)
        # FIX: Explicitly extract the raw binary array using .getvalue() 
        # This completely bypasses the moved file pointer issue!
        files = {
            "image": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)
        }
        
        # Your API form data fields
        data = {
            "latitude": "40.7128", 
            "longitude": "-74.0060",
            "address": "Intersection of Main St and 5th Ave",
            "description": "Pothole spotted from Streamlit app interface."
        }
        
        with st.spinner("Analyzing image with RoadPulse AI pipeline..."):
            try:
                # Send the request out to your backend server
                response = requests.post("http://127.0.0.1:8000/reports/", files=files, data=data)
                
                if response.status_code == 200:
                    st.success("Report successfully processed and stored!")
                    st.json(response.json())
                else:
                    st.error(f"Backend returned error code: {response.status_code}")
                    st.text(response.text)
            except Exception as e:
                st.error(f"Connection failed: {e}")

        st.divider()


    # -------------------------
    # Location Map
    # -------------------------

    st.subheader(
        "Select Location"
    )


    default_lat = 23.0225
    default_lon = 72.5714


    road_map = folium.Map(
        location=[
            default_lat,
            default_lon
        ],
        zoom_start=13
    )


    folium.Marker(
        [
            default_lat,
            default_lon
        ],
        popup="Select incident location"
    ).add_to(
        road_map
    )


    map_data = st_folium(
        road_map,
        width=700,
        height=450
    )


    latitude = default_lat
    longitude = default_lon


    if map_data["last_clicked"]:


        latitude = map_data["last_clicked"]["lat"]

        longitude = map_data["last_clicked"]["lng"]



    col1,col2 = st.columns(2)


    with col1:

        latitude = st.number_input(
            "Latitude",
            value=float(latitude),
            format="%.6f"
        )


    with col2:

        longitude = st.number_input(
            "Longitude",
            value=float(longitude),
            format="%.6f"
        )



    st.divider()


    # -------------------------
    # Details
    # -------------------------

    address = st.text_input(
        "Address",
        placeholder="Enter road location"
    )


    description = st.text_area(
        "Description",
        placeholder="Describe the problem",
        height=120
    )


    st.divider()



    # -------------------------
    # Submit
    # -------------------------

    if st.button(
        "Submit Report",
        type="primary",
        use_container_width=True
    ):


        if uploaded_image is None:

            st.error(
                "Please upload an image"
            )


        elif address == "":

            st.error(
                "Please enter address"
            )


        else:


            with st.spinner(
                "AI is analyzing the road issue..."
            ):


                files = {

                    "image":
                    (
                        uploaded_image.name,
                        uploaded_image,
                        uploaded_image.type
                    )

                }


                data = {

                    "latitude": latitude,

                    "longitude": longitude,

                    "address": address,

                    "description": description

                }


                try:


                    response = requests.post(

                        f"{API_URL}/reports/",

                        files=files,

                        data=data

                    )



                    if response.status_code == 200:


                        result = response.json()


                        st.success(
                            "Report submitted successfully"
                        )


                        st.subheader(
                            "AI Analysis"
                        )


                        report = result["report"]



                        col1,col2,col3 = st.columns(3)


                        with col1:

                            st.metric(
                                "Incident",
                                report["incident_type"]
                            )


                        with col2:

                            st.metric(
                                "Severity",
                                report["severity"]
                            )


                        with col3:

                            st.metric(
                                "Confidence",
                                f"{report['confidence']}%"
                            )



                        st.info(
                            report["summary"]
                        )



                        st.write(
                            "Department:",
                            report["department"]
                        )



                        if result["duplicate"]:

                            st.warning(
                                "Duplicate report detected"
                            )

                        else:

                            st.success(
                                "New incident created"
                            )


                    else:


                        st.error(
                            response.text
                        )


                except Exception as e:


                    st.error(
                        f"API Error: {e}"
                    )

# =====================================
# REPORTS PAGE
# =====================================

elif page == "Reports":

    st.title("Road Reports")

    st.write(
        "View all reported road incidents and their current status."
    )

    st.divider()


    # -------------------------
    # Fetch Reports
    # -------------------------

    try:

        response = requests.get(
            f"{API_URL}/reports/"
        )


        if response.status_code == 200:

            reports = response.json()


        else:

            st.error(
                "Unable to fetch reports"
            )

            reports = []


    except Exception as e:

        st.error(
            f"API Error: {e}"
        )

        reports = []



    if reports:


        # -------------------------
        # Search and Filter
        # -------------------------

        search = st.text_input(
            "Search by incident type or location"
        )


        status_filter = st.selectbox(
            "Filter Status",
            [
                "All",
                "Pending",
                "Assigned",
                "Resolved"
            ]
        )


        filtered_reports = reports



        if search:

            filtered_reports = [

                r for r in filtered_reports

                if search.lower()
                in (
                    str(r.get("incident_type",""))
                    +
                    str(r.get("address",""))
                ).lower()

            ]



        if status_filter != "All":

            filtered_reports = [

                r for r in filtered_reports

                if r.get("status")
                ==
                status_filter

            ]



        st.write(
            f"Showing {len(filtered_reports)} reports"
        )


        st.divider()



        # -------------------------
        # Display Cards
        # -------------------------

        for report in filtered_reports:


            with st.container(border=True):


                col1,col2 = st.columns(
                    [1,3]
                )


                with col1:


                    image_path = report.get(
                        "image_path"
                    )


                    if image_path:


                        image_url = (
                            f"{API_URL}/"
                            +
                            image_path
                        )


                        try:

                            st.image(
                                image_url,
                                use_container_width=True
                            )

                        except:

                            st.write(
                                "Image unavailable"
                            )



                with col2:


                    st.subheader(

                        report.get(
                            "incident_type",
                            "Unknown"
                        )

                    )


                    c1,c2,c3 = st.columns(3)


                    with c1:

                        st.metric(
                            "Severity",
                            report.get(
                                "severity",
                                "-"
                            )
                        )


                    with c2:

                        st.metric(
                            "Status",
                            report.get(
                                "status",
                                "-"
                            )
                        )


                    with c3:

                        st.metric(
                            "Confidence",
                            f"{report.get('confidence',0)}%"
                        )



                    st.write(
                        "Location:",
                        report.get(
                            "address",
                            "-"
                        )
                    )


                    st.write(
                        "Department:",
                        report.get(
                            "department",
                            "-"
                        )
                    )


                    st.write(
                        "Description:",
                        report.get(
                            "description",
                            "-"
                        )
                    )


                    st.write(
                        "Duplicate Reports:",
                        report.get(
                            "duplicate_count",
                            0
                        )
                    )



                    with st.expander(
                        "View AI Summary"
                    ):

                        st.write(
                            report.get(
                                "summary",
                                "No summary"
                            )
                        )


    else:

        st.info(
            "No reports available"
        )
# =====================================
# ANALYTICS PAGE
# =====================================

elif page == "Analytics":

    st.title("RoadPulse Analytics")

    st.write(
        "AI-powered insights from road infrastructure reports."
    )

    st.divider()


    # -------------------------
    # Fetch Reports Data
    # -------------------------

    try:

        response = requests.get(
            f"{API_URL}/reports/"
        )


        if response.status_code == 200:

            reports = response.json()


        else:

            reports = []


    except Exception as e:

        st.error(
            f"API Error: {e}"
        )

        reports = []



    if len(reports) > 0:


        df = pd.DataFrame(
            reports
        )


        # -------------------------
        # KPI SECTION
        # -------------------------

        total = len(df)


        pending = len(
            df[
                df["status"]
                ==
                "Pending"
            ]
        )


        resolved = len(
            df[
                df["status"]
                ==
                "Resolved"
            ]
        )


        critical = len(
            df[
                df["severity"]
                ==
                "Critical"
            ]
        )



        c1,c2,c3,c4 = st.columns(4)


        with c1:

            st.metric(
                "Total Reports",
                total
            )


        with c2:

            st.metric(
                "Pending",
                pending
            )


        with c3:

            st.metric(
                "Resolved",
                resolved
            )


        with c4:

            st.metric(
                "Critical",
                critical
            )



        st.divider()



        # -------------------------
        # Incident Distribution
        # -------------------------

        st.subheader(
            "Incident Type Distribution"
        )


        incident_chart = (

            df["incident_type"]
            .value_counts()
            .reset_index()

        )


        incident_chart.columns = [

            "Incident",
            "Count"

        ]



        fig1 = px.pie(

            incident_chart,

            names="Incident",

            values="Count",

            title="Road Issues"

        )


        st.plotly_chart(
            fig1,
            use_container_width=True
        )



        # -------------------------
        # Severity Analysis
        # -------------------------

        st.subheader(
            "Severity Analysis"
        )


        severity_chart = (

            df["severity"]
            .value_counts()
            .reset_index()

        )


        severity_chart.columns = [

            "Severity",
            "Count"

        ]



        fig2 = px.bar(

            severity_chart,

            x="Severity",

            y="Count",

            title="Issue Severity"

        )


        st.plotly_chart(

            fig2,

            use_container_width=True

        )



        # -------------------------
        # Department Performance
        # -------------------------

        st.subheader(
            "Department Workload"
        )


        dept_chart = (

            df["department"]
            .value_counts()
            .reset_index()

        )


        dept_chart.columns = [

            "Department",
            "Complaints"

        ]



        fig3 = px.bar(

            dept_chart,

            x="Department",

            y="Complaints",

            title="Complaints By Department"

        )


        st.plotly_chart(

            fig3,

            use_container_width=True

        )



        # -------------------------
        # Status Performance
        # -------------------------

        st.subheader(
            "Resolution Status"
        )


        status_chart = (

            df["status"]
            .value_counts()
            .reset_index()

        )


        status_chart.columns = [

            "Status",
            "Count"

        ]



        fig4 = px.pie(

            status_chart,

            names="Status",

            values="Count",

            title="Report Status"

        )


        st.plotly_chart(

            fig4,

            use_container_width=True

        )


    else:

        st.info(
            "No data available for analytics"
        )