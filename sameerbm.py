import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Axis Bank | Credit Risk Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (Axis Bank Branding) ---
st.markdown("""
    <style>
    /* Global Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');
    html, body, [class*="css"] {font-family: 'Lato', sans-serif;}
    
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    
    /* Axis Burgundy Colors */
    h1, h2, h3 {color: #861F41 !important;} 
    .stMetric {
        background-color: #ffffff; 
        border-left: 5px solid #861F41; 
        padding: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-radius: 5px;
    }
    
    /* Decision Card Styling */
    .decision-card {
        padding: 25px; 
        border-radius: 12px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        margin-top: 10px;
        background: white;
        border: 1px solid #e0e0e0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: SCORING ENGINE ---
st.sidebar.header("⚙️ Credit Scoring Parameters")
st.sidebar.caption("Adjust inputs to simulate committee vote.")

# Defaults set to generate Score ~6.05 (Conditional)
s_solv = st.sidebar.slider("Solvency (Z-Score) [25%]", 0, 10, 9, help="Altman Z-Score strength")
s_ops = st.sidebar.slider("Efficiency (F-Score) [15%]", 0, 10, 4, help="Piotrski F-Score trend")
s_str = st.sidebar.slider("Strategic Fit (GPS) [20%]", 0, 10, 9, help="Alignment with Growth/Sustainability")
s_col = st.sidebar.slider("Collateral Structure [30%]", 0, 10, 2, help="0=Unsecured, 10=Fully Secured")
s_mgt = st.sidebar.slider("Management Quality [10%]", 0, 10, 8)

# Weighted Score Calculation
score = (s_solv * 0.25) + (s_ops * 0.15) + (s_str * 0.20) + (s_col * 0.30) + (s_mgt * 0.10)

# Decision Logic (Axis Policy)
if score >= 7.5:
    status = "APPROVED"
    color = "#00796B" # Teal Green
    bg_color = "#E0F2F1"
    icon = "✅"
    rationale = "Proposal meets all RAROC and Risk hurdles."
elif score >= 5.5:
    status = "CONDITIONAL"
    color = "#F57F17" # Dark Amber
    bg_color = "#FFFDE7"
    icon = "🔄"
    rationale = "<b>REJECT Unsecured.</b><br>Counter-offer <b>Secured Term Loan</b> (₹1,415 Cr) to mitigate F-Score risk."
else:
    status = "REJECT"
    color = "#C62828" # Deep Red
    bg_color = "#FFEBEE"
    icon = "⛔"
    rationale = "Does not fit Risk Appetite. Exit relationship."

if st.sidebar.button("↺ Reset Dashboard"):
    st.cache_data.clear()
    st.rerun()

# --- 4. HEADER: LOGOS & CONTEXT ---
# Using columns to center align title between logos
c1, c2, c3 = st.columns([1, 3.5, 1])

with c1:
    # Axis Bank Logo
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Axis_Bank_logo.svg/1200px-Axis_Bank_logo.svg.png", width=160)

with c2:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Wholesale Banking Credit Committee</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; font-size: 1.1em;'><b>Borrower:</b> Jindal Steel & Power Ltd (JSPL) | <b>Facility:</b> ₹1,415 Cr Unsecured Term Loan</p>", unsafe_allow_html=True)

with c3:
    # JSPL Logo
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Jindal_Steel_and_Power_Logo.svg/1200px-Jindal_Steel_and_Power_Logo.svg.png", width=160)

st.markdown("---")

# --- 5. TOP SECTION: RISKOMETER & VERDICT ---
col_left, col_right = st.columns([1.2, 2])

# LEFT: RISKOMETER
with col_left:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>AXIS AI SCORE</b>", 'font': {'size': 20, 'color': '#861F41'}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "#333"},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#eee",
            'steps': [
                {'range': [0, 5.5], 'color': "#ffcdd2"},   # Red Zone
                {'range': [5.5, 7.5], 'color': "#fff9c4"}, # Amber Zone
                {'range': [7.5, 10], 'color': "#c8e6c9"}   # Green Zone
            ],
            'threshold': {'line': {'color': "#861F41", 'width': 4}, 'thickness': 0.75, 'value': 7.5}
        }
    ))
    fig_gauge.update_layout(height=280, margin=dict(l=30,r=30,t=50,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

# RIGHT: VERDICT CARD
with col_right:
    st.markdown(f"""
    <div class="decision-card" style="background: {bg_color}; border-top: 5px solid {color};">
        <h3 style="color: {color} !important; margin: 0; font-size: 1.8em;">{icon} RECOMMENDATION: {status}</h3>
        <h1 style="font-size: 4em; margin: 10px 0; color: #333;">{score:.2f} <span style="font-size: 0.3em; color: #777;">/ 10.0</span></h1>
        <hr style="border-top: 1px solid {color}; opacity: 0.3; margin: 15px 0;">
        <p style="font-size: 1.3em; color: #333; font-weight: 500;">{rationale}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. KEY METRICS ROW ---
st.markdown("### 📊 Key Risk Indicators")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Net Debt / EBITDA", "1.48x", "Safe (< 2.5x)", delta_color="normal")
m2.metric("Altman Z''-Score", "3.71", "Strong Solvency", delta_color="normal")
m3.metric("Piotrski F-Score", "4 / 9", "Weak Efficiency", delta_color="inverse")
m4.metric("Deal RAROC", "11.2%", "Below Hurdle (16%)", delta_color="inverse")

st.markdown("---")

# --- 7. GRAPHS (2x2 Grid) ---
st.markdown("### 📈 Quantitative & Strategic Deep Dive")
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# GRAPH 1: SOLVENCY VS EFFICIENCY (The Conflict)
with row1_col1:
    st.markdown("**1. The Conflict: Solvency vs. Efficiency Gap**")
    # Normalized scores for visual comparison
    gap_data = pd.DataFrame({
        'Metric': ['Solvency (Z-Score)', 'Efficiency (F-Score)'],
        'Score (0-10)': [9.2, 4.4], 
        'Status': ['Strong', 'Weak']
    })
    fig_gap = px.bar(gap_data, x='Metric', y='Score (0-10)', color='Status',
                     color_discrete_map={'Strong':'#28a745', 'Weak':'#dc3545'},
                     text='Score (0-10)')
    fig_gap.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_gap.update_layout(yaxis=dict(range=[0, 11]), height=320, showlegend=False)
    st.plotly_chart(fig_gap, use_container_width=True)

# GRAPH 2: RAROC ANALYSIS (Profitability)
with row1_col2:
    st.markdown("**2. RAROC Analysis: Unsecured vs. Secured**")
    raroc_fig = go.Figure()
    
    # Bars
    raroc_fig.add_trace(go.Bar(
        x=['Unsecured (Ask)', 'Secured (Offer)'],
        y=[11.2, 18.5],
        marker_color=['#dc3545', '#28a745'],
        name='Deal RAROC',
        text=[11.2, 18.5],
        textposition='auto'
    ))
    
    # Hurdle Line
    raroc_fig.add_trace(go.Scatter(
        x=['Unsecured (Ask)', 'Secured (Offer)'],
        y=[16, 16],
        mode='lines',
        name='Axis Hurdle (16%)',
        line=dict(color='#861F41', width=3, dash='dash')
    ))
    raroc_fig.update_layout(height=320, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(raroc_fig, use_container_width=True)

# GRAPH 3: FINANCIAL TREND (Debt vs Margins)
with row2_col1:
    st.markdown("**3. Trend: Rising Debt, Shrinking Margins**")
    trend_data = pd.DataFrame({
        'Year': ['FY23', 'FY24', 'FY25 (Est)'],
        'Net Debt (₹ Cr)': [9500, 10200, 14156],
        'EBITDA Margin (%)': [24.5, 21.0, 16.5]
    })
    
    # Create figure with secondary y-axis
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=trend_data['Year'], y=trend_data['Net Debt (₹ Cr)'], name='Net Debt', marker_color='#BDBDBD'))
    fig_trend.add_trace(go.Scatter(x=trend_data['Year'], y=trend_data['EBITDA Margin (%)'], name='Margin %', yaxis='y2', line=dict(color='#861F41', width=4)))
    
    fig_trend.update_layout(
        height=320,
        yaxis=dict(title="Debt (Cr)"),
        yaxis2=dict(title="Margin (%)", overlaying='y', side='right'),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# GRAPH 4: RISK RADAR (Gap Analysis)
with row2_col2:
    st.markdown("**4. Risk Profile: Actual vs. Ideal**")
    categories = ['Solvency', 'Efficiency', 'Strategic Fit', 'Collateral', 'Management']
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[s_solv, s_ops, s_str, s_col, s_mgt],
        theta=categories,
        fill='toself',
        name='JSPL Proposal',
        line_color='#861F41'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[8, 7, 8, 8, 8],
        theta=categories,
        name='Ideal Threshold',
        line_color='#28a745',
        line_dash='dot'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        height=320,
        showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 8. FOOTER ---
st.markdown("---")
st.info("💡 **Negotiation Strategy:** JSPL's Solvency is excellent (Z-Score > 3), meaning they are safe. However, their Efficiency is low (F-Score < 5), meaning they are cash-strapped. **Pivot to Secured Lending** to protect the bank during this expansion phase.")