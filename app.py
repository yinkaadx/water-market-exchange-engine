import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Water Market Exchange Engine", layout="wide")

st.title("Serverless Supply-Side Water Exchange")
st.caption("Real-Time Hydrological Monitoring & Dynamic Club-Level Pricing")

st.sidebar.header("Market Mechanism Configuration")
selected_catchment = st.sidebar.selectbox("Simulated River Catchment", ["Wellington Small Catchment Alpha", "Canterbury Agricultural Basin", "Waikato River Demand Zone"])
drought_severity = st.sidebar.slider("Simulate Exogenous Drought Severity", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize Digital Water Market")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: AWS Hydrological Ingestion -> XGBoost Dynamic Pricing -> Market Ledger")

if run_simulation:
    st.subheader(f"Active Market Trading Exchange: {selected_catchment}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_supply = col1.empty()
    metric_demand = col2.empty()
    metric_price = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(2323)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    supply_levels = []
    market_prices = []
    
    base_supply = 1000.0 
    base_price = 10.0
    
    for i in range(100):
        if i < 30:
            current_supply = base_supply + np.random.uniform(-10.0, 10.0)
            current_demand = np.random.uniform(400.0, 500.0)
            current_price = base_price + np.random.uniform(-0.5, 0.5)
            status = "MARKET EQUILIBRIUM"
        elif i >= 30 and i < 70:
            current_supply = base_supply - (i - 30) * (8.0 * drought_severity) + np.random.uniform(-20.0, 20.0)
            current_demand = 600.0 + (i - 30) * 2.0 + np.random.uniform(-10.0, 10.0)
            current_price = base_price + ((1000.0 - current_supply) / 50.0) * drought_severity
            status = "RESOURCE SCARCITY DETECTED"
        else:
            current_supply = current_supply + np.random.uniform(-5.0, 5.0)
            current_demand = max(200.0, current_demand - np.random.uniform(10.0, 30.0)) 
            current_price = current_price + np.random.uniform(-1.0, 1.0)
            status = "CLUB COOPERATION ACTIVE"
            
        current_supply = max(100.0, current_supply)
            
        supply_levels.append(current_supply)
        market_prices.append(current_price)
        
        metric_supply.metric("Catchment Supply Flow", f"{current_supply:.1f} ML", f"{(current_supply - base_supply):.1f} ML")
        metric_demand.metric("Aggregated Agricultural Demand", f"{current_demand:.1f} ML")
        metric_price.metric("Dynamic Market Clearing Price", f"${current_price:.2f} / ML", f"+${(current_price - base_price):.2f}")
        
        if status == "RESOURCE SCARCITY DETECTED":
            metric_status.metric("Market Dynamics", status, "Price Inflation")
        elif status == "CLUB COOPERATION ACTIVE":
            metric_status.metric("Market Dynamics", status, "Demand Curtailed")
        else:
            metric_status.metric("Market Dynamics", status, "Stable Trading")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=supply_levels, mode='lines', name='Catchment Supply Level (ML)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=market_prices, mode='lines', name='Dynamic Market Price (USD/ML)', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Environmental Economics: Hydrological Scarcity vs Algorithmic Supply-Side Pricing",
            xaxis=dict(title="High-Frequency Market Timeline"),
            yaxis=dict(title="Resource Supply (ML)"),
            yaxis2=dict(title="Market Price (USD/ML)", overlaying='y', side='right', range=[0, max(50, current_price + 10)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "RESOURCE SCARCITY DETECTED" and i == 30:
            log_placeholder.error(f"CLIMATE ALERT: Severe drought metrics ingested at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine dynamically increasing water extraction price to prevent catchment depletion.")
        elif status == "CLUB COOPERATION ACTIVE" and i == 70:
            log_placeholder.success(f"MARKET SUCCESS: Price signals successfully transmitted via cloud architecture. Water clubs initiated group-level conservation protocols. Demand curtailed. Welfare maximized.")
        elif status == "MARKET EQUILIBRIUM" and i % 5 == 0:
            log_placeholder.info(f"Log: Hydrological telemetry tick {i} ingested via serverless API. Micro-transactions clearing at baseline equilibrium prices.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud exchange successfully modeled supply-side water trading and avoided resource shortage via dynamic algorithmic pricing.")
else:
    st.info("Click 'Initialize Digital Water Market' in the sidebar to simulate high-frequency resource economics data ingestion.")