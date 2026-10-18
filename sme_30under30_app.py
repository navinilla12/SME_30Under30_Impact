import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. PAGE CONFIGURATION & LIGHT STYLING
# ==============================================================================
st.set_page_config(
    page_title="SME Media | 30 Under 30 Impact Dashboard",
    page_icon="🌟",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .profile-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .tag-chip {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA ENGINE
# ==============================================================================
@st.cache_data
def load_data():
    raw_data = [
        {
            "Name": "Alex Chen",
            "Age": 27,
            "Company": "Boeing",
            "Industry_Sector": "Aerospace & Defense",
            "Technology_Focus": "Additive Manufacturing",
            "LinkedIn_Impressions": 14200,
            "Reactions": 890,
            "Shares": 120,
            "Bio": "Developing 3D-printed titanium flight components that reduce aircraft weight by 18%."
        },
        {
            "Name": "Maya Patel",
            "Age": 25,
            "Company": "FANUC America",
            "Industry_Sector": "Robotics & Automation",
            "Technology_Focus": "Physical AI & Vision Systems",
            "LinkedIn_Impressions": 18500,
            "Reactions": 1240,
            "Shares": 210,
            "Bio": "Engineered autonomous bin-picking algorithms for high-speed assembly lines."
        },
        {
            "Name": "Jordan Miller",
            "Age": 28,
            "Company": "Oak Ridge National Lab",
            "Industry_Sector": "Smart Manufacturing",
            "Technology_Focus": "Digital Twin & Sensor Analytics",
            "LinkedIn_Impressions": 11300,
            "Reactions": 670,
            "Shares": 85,
            "Bio": "Created real-time sensor analytics predicting tooling failure in CNC machines."
        },
        {
            "Name": "Sophia Ramirez",
            "Age": 26,
            "Company": "Tesla",
            "Industry_Sector": "Automotive & EV",
            "Technology_Focus": "Battery Cell Automation",
            "LinkedIn_Impressions": 22100,
            "Reactions": 1820,
            "Shares": 340,
            "Bio": "Optimized robotic electrode coating processes, accelerating factory yield."
        },
        {
            "Name": "David Wright",
            "Age": 29,
            "Company": "General Motors",
            "Industry_Sector": "Workforce Leadership",
            "Technology_Focus": "Apprenticeship Programs",
            "LinkedIn_Impressions": 9800,
            "Reactions": 540,
            "Shares": 65,
            "Bio": "Spearheaded high-school manufacturing apprenticeships across Midwestern plants."
        }
    ]
    df = pd.DataFrame(raw_data)
    df['Engagement_Rate_%'] = round(((df['Reactions'] + df['Shares']) / df['LinkedIn_Impressions']) * 100, 2)
    return df

df_master = load_data()

# ==============================================================================
# 3. HEADER & EXPANDED SIDEBAR CONTROLS
# ==============================================================================
st.title("🌟 SME Media: 30 Under 30 Impact Dashboard")
st.caption("Executive overview of 30 Under 30 honorees, sector engagement, corporate contributions, and content reach.")

st.sidebar.header("🕹️ Global Controls")
st.sidebar.markdown("Use the filters below to customize your executive view.")

# Filter 1: Industry Sectors
selected_sectors = st.sidebar.multiselect(
    "Filter by Industry Sector:",
    options=df_master['Industry_Sector'].unique(),
    default=df_master['Industry_Sector'].unique()
)

# Filter 2: Partner Companies
selected_companies = st.sidebar.multiselect(
    "Filter by Partner Company:",
    options=df_master['Company'].unique(),
    default=df_master['Company'].unique()
)

# Filter 3: Age Range Slider
min_age, max_age = int(df_master['Age'].min()), int(df_master['Age'].max())
selected_age_range = st.sidebar.slider(
    "Filter by Honoree Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Filter 4: Minimum LinkedIn Impressions Slider
min_impressions = st.sidebar.slider(
    "Minimum LinkedIn Impressions:",
    min_value=0,
    max_value=int(df_master['LinkedIn_Impressions'].max()),
    value=0,
    step=1000
)

# Filter 5: Text Search Box
search_query = st.sidebar.text_input("🔍 Search Name or Tech Focus:", "")

# Apply All Sidebar Filters
df_filtered = df_master[
    (df_master['Industry_Sector'].isin(selected_sectors)) &
    (df_master['Company'].isin(selected_companies)) &
    (df_master['Age'].between(selected_age_range[0], selected_age_range[1])) &
    (df_master['LinkedIn_Impressions'] >= min_impressions) &
    (
        df_master['Name'].str.contains(search_query, case=False) |
        df_master['Technology_Focus'].str.contains(search_query, case=False)
    )
]

# ==============================================================================
# 4. EXECUTIVE KPI CARDS (PULLED TO TOP)
# ==============================================================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Selected Honorees", len(df_filtered))
col2.metric("Partner Companies", df_filtered['Company'].nunique() if not df_filtered.empty else 0)
col3.metric("Total Impressions", f"{df_filtered['LinkedIn_Impressions'].sum():,}")
col4.metric("Total Reactions", f"{df_filtered['Reactions'].sum():,}")
col5.metric("Avg Engagement", f"{round(df_filtered['Engagement_Rate_%'].mean(), 2)}%" if not df_filtered.empty else "0%")

st.divider()

# ==============================================================================
# 5. CHARTS ROW 1: HONOREE REACH & SECTOR SHARE
# ==============================================================================
col_chart1, col_chart2 = st.columns([3, 2])

with col_chart1:
    st.subheader("LinkedIn Impressions by Honoree")
    if df_filtered.empty:
        st.info("No data available for the current filter criteria.")
    else:
        fig_bar = px.bar(
            df_filtered,
            x="Name",
            y="LinkedIn_Impressions",
            color="Industry_Sector",
            text_auto=".2s",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_bar.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=20, b=10),
            clickmode='event+select'
        )
        
        event_bar = st.plotly_chart(
            fig_bar, 
            use_container_width=True, 
            on_select="rerun", 
            selection_mode="points",
            key="bar_selection"
        )

with col_chart2:
    st.subheader("Audience Reactions Share")
    if df_filtered.empty:
        st.info("No data available for the current filter criteria.")
    else:
        fig_pie = px.pie(
            df_filtered,
            names="Industry_Sector",
            values="Reactions",
            hole=0.4,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_pie.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=20, b=10),
            clickmode='event+select'
        )
        
        event_pie = st.plotly_chart(
            fig_pie, 
            use_container_width=True, 
            on_select="rerun", 
            selection_mode="points",
            key="pie_selection"
        )

st.divider()

# ==============================================================================
# 6. CHARTS ROW 2: CORPORATE CONTRIBUTIONS & SECTOR BENCHMARK
# ==============================================================================
col_row2_left, col_row2_right = st.columns(2)

with col_row2_left:
    st.subheader("🏢 Corporate Talent Pipeline & Reach")
    st.caption("Total LinkedIn impressions generated per partner organization.")
    
    if df_filtered.empty:
        st.info("No data available.")
    else:
        df_company_reach = df_filtered.groupby("Company", as_index=False)["LinkedIn_Impressions"].sum()
        df_company_reach = df_company_reach.sort_values(by="LinkedIn_Impressions", ascending=True)

        fig_company = px.bar(
            df_company_reach,
            x="LinkedIn_Impressions",
            y="Company",
            orientation="h",
            text_auto=".2s",
            color="LinkedIn_Impressions",
            color_continuous_scale="Teal",
            template="plotly_white"
        )
        fig_company.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Total Impressions Generated",
            yaxis_title="Company / Organization",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_company, use_container_width=True)

with col_row2_right:
    st.subheader("📊 Sector Audience Engagement Benchmark (% Rate)")
    st.caption("Identifies high-performing sectors versus areas for future audience focus.")

    if df_filtered.empty:
        st.info("No data available.")
    else:
        df_sector_engagement = df_filtered.groupby("Industry_Sector", as_index=False)["Engagement_Rate_%"].mean()
        df_sector_engagement = df_sector_engagement.sort_values(by="Engagement_Rate_%", ascending=True)

        fig_sector_eng = px.bar(
            df_sector_engagement,
            x="Engagement_Rate_%",
            y="Industry_Sector",
            orientation="h",
            text_auto=".2f",
            color="Engagement_Rate_%",
            color_continuous_scale="Blues",
            template="plotly_white"
        )
        fig_sector_eng.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Avg Engagement Rate (%)",
            yaxis_title="Industry Sector",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sector_eng, use_container_width=True)

st.divider()

# ==============================================================================
# 7. INTERACTIVE HONOREE DIRECTORY CARDS
# ==============================================================================
st.subheader("📋 Honoree Profile Breakdown")

# Handle Chart Selections
selected_names = []
if 'event_bar' in locals() and event_bar and "points" in event_bar.get("selection", {}):
    for pt in event_bar["selection"]["points"]:
        if "x" in pt:
            selected_names.append(pt["x"])

if selected_names:
    df_filtered = df_filtered[df_filtered['Name'].isin(selected_names)]
    st.info(f"Filtering profile data by selected chart honoree: **{', '.join(selected_names)}**")

if df_filtered.empty:
    st.warning("No honorees match your current sidebar filters or chart selections. Please adjust your filters.")
else:
    for _, row in df_filtered.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="profile-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin:0; color:#0F172A;">{row['Name']} ({row['Age']}) — <strong>{row['Company']}</strong></h3>
                    <span class="tag-chip">{row['Industry_Sector']}</span>
                </div>
                <p style="color:#475569; margin-top: 0.5rem;"><strong>Focus:</strong> {row['Technology_Focus']}</p>
                <blockquote style="margin: 0.5rem 0; color:#334155;"><em>"{row['Bio']}"</em></blockquote>
            </div>
            """, unsafe_allow_html=True)
            
            c_label, c_bar = st.columns([1, 4])
            c_label.caption(f"Engagement Score ({row['Engagement_Rate_%']}%)")
            c_bar.progress(min(int(row['Engagement_Rate_%'] * 10), 100))