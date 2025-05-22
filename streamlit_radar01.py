import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# --- Load and clean the data ---
df = pd.read_csv("2022.csv", sep=';')

# Keep only relevant fields
df = df[[
    'Country',
    'Helping a stranger Score',
    'Donating money Score',
    'Volunteering time Score'
]]
df.columns = ['Country', 'Stranger', 'Donate', 'Volunteer']

# Clean % symbols and other artifacts
def clean(col):
    return pd.to_numeric(col.astype(str).str.replace(r"[^\d.]", "", regex=True), errors='coerce')

df['Stranger'] = clean(df['Stranger'])
df['Donate'] = clean(df['Donate'])
df['Volunteer'] = clean(df['Volunteer'])

# --- Set up Streamlit app ---
st.set_page_config(page_title="Global Generosity Compass", layout="wide")
st.subheader("🌍 Global Generosity Compass")
st.markdown("Compare how countries give: donating, volunteering, and helping strangers.")

features = ['Donate', 'Volunteer', 'Stranger']

# Country selection
selected = st.multiselect(
    "Select countries to compare:",
    options=df['Country'].dropna().unique(),
    default=['Indonesia', 'Kenya', 'United States of America']
)

# Generate radar chart
fig = go.Figure()

for country in selected:
    values = df[df['Country'] == country][features].values.flatten().tolist()
    if any(pd.isna(values)):
        continue
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=features + [features[0]],
        fill='toself',
        name=country
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)
