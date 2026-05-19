# ================================================================
# COFFEE & CLIMATE — INTERACTIVE STREAMLIT DASHBOARD
# By Tulasi Arvind
# Run: python3 -m streamlit run coffee_dashboard.py
# ================================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Coffee & Climate",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── COLOURS ───────────────────────────────────────────────────
BROWN_DARK  = "#2C1A0E"
BROWN_MID   = "#6B3A2A"
BROWN_WARM  = "#A0522D"
BROWN_LIGHT = "#C8956C"
BROWN_CREAM = "#E8D5B7"
PINK_DEEP   = "#D4789A"
PINK_MID    = "#E8A0B8"
PINK_LIGHT  = "#F5D0DF"
PINK_PALE   = "#FDF0F5"
HEART_B64   = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDMyIDMyIj4KICA8cGF0aCBkPSJNMTYgMjggQzE2IDI4IDQgMjAgNCAxMiBDNCA3LjYgNy42IDQgMTIgNCBDMTQuMiA0IDE2IDYgMTYgNiBDMTYgNiAxNy44IDQgMjAgNCBDMjQuNCA0IDI4IDcuNiAyOCAxMiBDMjggMjAgMTYgMjggMTYgMjhaIiBmaWxsPSIjRDQ3ODlBIiBzdHJva2U9IiNBMDUyMkQiIHN0cm9rZS13aWR0aD0iMS41Ii8+Cjwvc3ZnPg=="

TEMP_COLORS = {
    "too cold":    "#1A5276",
    "cool stress": "#5DADE2",
    "ideal":       "#A8D5A2",
    "heat stress": "#F0A500",
    "at risk":     "#D45500",
    "danger":      "#8B0000",
}
REGION_COLORS = {
    "Minas Gerais":   BROWN_MID,
    "Espirito Santo": BROWN_WARM,
    "Sao Paulo":      BROWN_LIGHT,
    "Bahia":          PINK_DEEP,
    "Rondonia":       PINK_MID,
}
COUNTRY_COLORS = {
    "Brazil":    BROWN_MID,
    "Vietnam":   "#8B0000",
    "Colombia":  BROWN_WARM,
    "Indonesia": PINK_DEEP,
    "Ethiopia":  BROWN_LIGHT,
}

# ── CSS — inject colours as variables, use plain braces in CSS ──
CURSOR = f"url('data:image/svg+xml;base64,{HEART_B64}') 16 16"

css = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {{
      font-family: 'DM Sans', sans-serif;
      background-color: {BROWN_CREAM};
      color: {BROWN_DARK};
      cursor: {CURSOR}, auto;
  }}
  a, button, [data-baseweb="tab"], .stSelectbox, .stMultiSelect,
  .stSlider, [data-testid="metric-container"] {{
      cursor: {CURSOR}, pointer;
  }}
  .stApp {{ background-color: {BROWN_CREAM}; }}
  [data-testid="stSidebar"] {{ background-color: {BROWN_DARK} !important; }}
  [data-testid="stSidebar"] * {{ color: {BROWN_CREAM} !important; }}
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label,
  [data-testid="stSidebar"] .stSlider label {{
      color: {PINK_MID} !important;
      font-size: 13px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
  }}
  h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: {BROWN_DARK}; }}
  [data-testid="metric-container"] {{
      background: white;
      border: 1px solid {BROWN_CREAM};
      border-radius: 12px;
      padding: 16px;
      box-shadow: 2px 4px 12px rgba(44,26,14,0.08);
  }}
  [data-testid="metric-container"] label {{
      color: {BROWN_WARM} !important;
      font-size: 12px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
  }}
  [data-testid="metric-container"] [data-testid="stMetricValue"] {{
      font-family: 'Playfair Display', serif !important;
      color: {BROWN_DARK} !important;
      font-size: 28px !important;
  }}
  .stTabs [data-baseweb="tab-list"] {{
      background-color: transparent;
      border-bottom: 2px solid rgba(107,58,42,0.15);
      gap: 6px;
      padding: 0;
  }}
  .stTabs [data-baseweb="tab"] {{
      font-family: 'DM Sans', sans-serif;
      font-size: 12px;
      letter-spacing: 0.04em;
      color: {BROWN_MID};
      background: {BROWN_CREAM};
      border: 1.5px solid rgba(107,58,42,0.2);
      border-bottom: none;
      border-radius: 8px 8px 0 0;
      padding: 8px 18px 10px 14px;
      position: relative;
      top: 2px;
      transition: background 0.15s;
  }}
  .stTabs [data-baseweb="tab"]:hover {{ background: {PINK_LIGHT} !important; }}
  .stTabs [aria-selected="true"] {{
      background-color: white !important;
      color: {BROWN_DARK} !important;
      border-color: rgba(107,58,42,0.3) !important;
      border-bottom: 2px solid white !important;
      font-weight: 500;
  }}
  .stTabs [data-baseweb="tab-panel"] {{
      background: white;
      border-radius: 0 12px 12px 12px;
      padding: 24px;
      border: 1.5px solid rgba(107,58,42,0.15);
      border-top: none;
  }}
  hr {{ border-color: {PINK_MID}; opacity: 0.4; }}
  .section-label {{
      font-size: 11px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: {BROWN_WARM};
      margin-bottom: 4px;
  }}
  .source-card {{
      background: white;
      border-radius: 14px;
      padding: 24px 28px;
      margin-bottom: 16px;
      box-shadow: 2px 4px 16px rgba(44,26,14,0.07);
      border-left: 5px solid {BROWN_MID};
  }}
  .source-card a {{ color: {BROWN_WARM}; text-decoration: none; font-weight: 500; word-break: break-all; }}
  .source-card a:hover {{ color: {PINK_DEEP}; text-decoration: underline; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ── PLOTLY DEFAULTS ───────────────────────────────────────────
PLOT_LAYOUT = dict(
    font_family="DM Sans", font_color=BROWN_DARK,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(232,213,183,0.3)",
    title_font_family="Playfair Display", title_font_color=BROWN_DARK, title_font_size=16,
    legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor=BROWN_CREAM, borderwidth=1, font_size=11),
    margin=dict(t=50, b=40, l=40, r=20),
)

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{BROWN_DARK} 0%,{BROWN_MID} 60%,{PINK_DEEP} 100%);
            border-radius:16px;padding:40px 48px;margin-bottom:32px;
            position:relative;overflow:hidden;">
  <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
              border-radius:50%;background:rgba(232,160,184,0.15);"></div>
  <div style="position:absolute;bottom:-60px;right:80px;width:140px;height:140px;
              border-radius:50%;background:rgba(200,149,108,0.1);"></div>
  <p style="font-size:11px;letter-spacing:0.2em;text-transform:uppercase;
             color:{PINK_MID};margin:0 0 8px;">Climate Risk Analysis · Tulasi Arvind</p>
  <h1 style="font-family:'Playfair Display';font-size:42px;font-weight:900;
              color:white;margin:0 0 12px;line-height:1.1;">Coffee & Climate</h1>
  <p style="font-size:15px;color:{BROWN_CREAM};margin:0;max-width:560px;
             line-height:1.6;opacity:0.85;">
      How rising temperatures are threatening the world's top coffee producers —
      with a deep dive into Brazil's Arabica growing regions.
  </p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <p style="font-family:'Playfair Display';font-size:22px;color:{PINK_MID};margin-bottom:4px;">
        ☕ Filters</p>
    <p style="font-size:12px;opacity:0.6;margin-bottom:24px;">Adjust to explore the data</p>
    """, unsafe_allow_html=True)
    selected_regions = st.multiselect("Brazil regions",
        options=list(REGION_COLORS.keys()), default=list(REGION_COLORS.keys()))
    selected_countries = st.multiselect("Top 5 producers",
        options=list(COUNTRY_COLORS.keys()), default=list(COUNTRY_COLORS.keys()))
    year_range = st.slider("Year range", min_value=1961, max_value=2024, value=(1990, 2024))
    st.markdown("---")
    st.markdown(f"""
    <p style="font-size:11px;opacity:0.5;letter-spacing:0.08em;text-transform:uppercase;">
        Arabica ideal range</p>
    <p style="font-family:'Playfair Display';font-size:24px;color:{PINK_MID};">18 – 21°C</p>
    """, unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df_temp = pd.read_csv("data/brazil_temp.csv")
    df_temp["year"] = df_temp["year"].astype(int)
    for col in ["avg_temp","avg_tmax","avg_tmin","deviation"]:
        df_temp[col] = pd.to_numeric(df_temp[col], errors="coerce")

    df_prod = pd.read_csv("data/production.csv")
    df_prod["year"] = df_prod["year"].astype(int)
    df_prod.rename(columns={"arabica":"arabica_production","robusta":"robusta_production"}, inplace=True)
    for col in ["production","arabica_production","robusta_production"]:
        df_prod[col] = pd.to_numeric(df_prod[col], errors="coerce").fillna(0)

    df_merged = pd.read_csv("data/brazil_merged.csv")
    df_merged["year"] = df_merged["year"].astype(int)
    df_merged = df_merged.sort_values("year")
    df_merged["prod_change_%"] = df_merged["production"].pct_change() * 100
    return df_temp, df_prod, df_merged

df_temp, df_prod, df_merged = load_data()

df_temp_f   = df_temp[(df_temp["region"].isin(selected_regions)) & (df_temp["year"].between(*year_range))]
df_prod_f   = df_prod[(df_prod["country"].isin(selected_countries)) & (df_prod["year"].between(*year_range))]
df_merged_f = df_merged[df_merged["year"].between(*year_range)]

# ── KPI METRICS ───────────────────────────────────────────────
st.markdown('<p class="section-label">At a glance</p>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
latest_year = df_temp_f["year"].max() if not df_temp_f.empty else 2024
latest_temp = df_temp_f[(df_temp_f["region"]=="Minas Gerais") & (df_temp_f["year"]==latest_year)]["avg_temp"].values
with k1:
    st.metric("Latest avg temp", f"{latest_temp[0]:.1f}°C" if len(latest_temp) else "—", delta="Minas Gerais")
with k2:
    sy = df_temp_f[(df_temp_f["region"]=="Minas Gerais") & (df_temp_f["temp_status"].isin(["heat stress","at risk","danger"]))].shape[0]
    st.metric("Heat stress years", sy, delta="above 21°C")
with k3:
    lp = df_prod_f[(df_prod_f["country"]=="Brazil") & (df_prod_f["year"]==df_prod_f["year"].max())]["production"].values
    st.metric("Brazil production", f"{lp[0]:,.0f}" if len(lp) else "—", delta="1k × 60kg bags")
with k4:
    ad = df_temp_f[df_temp_f["region"]=="Minas Gerais"]["deviation"].mean()
    st.metric("Avg deviation", f"+{ad:.1f}°C" if ad > 0 else f"{ad:.1f}°C", delta="from 21°C ceiling")
with k5:
    ip = df_temp_f[df_temp_f["temp_status"]=="ideal"].shape[0] / max(df_temp_f.shape[0],1) * 100
    st.metric("Years in ideal range", f"{ip:.0f}%", delta="across all regions")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab0,tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "📖  The story",
    "🌡️  Temperature",
    "☕  Production",
    "⚠️  Risk",
    "🔗  Temp vs output",
    "📝  Conclusions",
    "📚  Sources",
])

# ══ TAB 0: STORY ═════════════════════════════════════════════
with tab0:
    st.markdown(f"""
    <div style="max-width:740px;margin:0 auto;padding:8px 0 32px;">
      <p style="font-size:11px;letter-spacing:0.2em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">A project by Tulasi Arvind</p>
      <p style="font-family:'Playfair Display';font-size:36px;font-weight:900;
                 color:{BROWN_DARK};line-height:1.2;margin:0 0 28px;">
          It started with an iced latte.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 18px;">
          I love coffee. Trying out new cafes is something I do in every new place I
          travel to — it's one of those small rituals that makes arriving somewhere feel
          like arriving somewhere. A good flat white in one city, a tiny espresso pulled
          fast in another.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 18px;">
          Then came another blazing summer. My iced latte tasted better than ever —
          cold, strong, exactly what you want when the heat won't let up. But somewhere
          between sips, a thought crept in. <em>What happens to the beans?</em>
          The farms, the growing regions, the harvests that make any of this possible —
          how are they holding up as the planet keeps warming?</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 28px;">
          That question turned into this project.</p>
      <div style="border-left:4px solid {PINK_DEEP};padding:16px 24px;
                  background:{PINK_PALE};border-radius:0 12px 12px 0;margin-bottom:32px;">
        <p style="font-family:'Playfair Display';font-size:18px;font-style:italic;
                   color:{BROWN_DARK};margin:0;line-height:1.7;">
            "Arabica coffee — the variety behind most specialty brews — thrives between
            18°C and 21°C. A seemingly small window. And it's shrinking."</p>
      </div>
      <p style="font-family:'Playfair Display';font-size:21px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 12px;">What I looked at</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 18px;">
          Two datasets — decades of coffee production data from the USDA covering the
          world's top five producers, and 65 years of daily temperature readings from
          over a thousand weather stations across Brazil's five main coffee-growing
          regions: Minas Gerais, Espírito Santo, São Paulo, Bahia, and Rondônia.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 28px;">
          Brazil alone produces nearly 40% of the world's coffee. If anywhere is going
          to show the strain of rising temperatures, it's here.</p>
      <p style="font-family:'Playfair Display';font-size:21px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 12px;">How to use this dashboard</p>
      <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                  border:0.5px solid rgba(107,58,42,0.2);">
        <ul style="font-size:14px;color:{BROWN_DARK};line-height:2.2;margin:0;padding-left:18px;">
          <li>Use the <strong>sidebar filters</strong> to select regions, countries, and year range</li>
          <li><strong>🌡️ Temperature</strong> — how each region's avg temp has changed since 1960</li>
          <li><strong>☕ Production</strong> — output volumes for the top 5 producing countries</li>
          <li><strong>⚠️ Risk</strong> — years each region spent outside the ideal 18–21°C window</li>
          <li><strong>🔗 Temp vs output</strong> — do hotter years mean less coffee?</li>
          <li><strong>📝 Conclusions</strong> — what the data actually says</li>
        </ul>
      </div>
      <p style="font-size:13px;color:{BROWN_WARM};margin:20px 0 0;font-style:italic;">
          Built with Python · Streamlit · Plotly · Data from USDA PSD & Xavier et al. (2022)</p>
    </div>
    """, unsafe_allow_html=True)

# ══ TAB 1: TEMPERATURE ═══════════════════════════════════════
with tab1:
    t1_hot = max(selected_regions, key=lambda r: df_temp_f[df_temp_f["region"]==r]["avg_temp"].mean()) if selected_regions else "—"
    t1_avg = df_temp_f["avg_temp"].mean() if not df_temp_f.empty else 0
    t1_above = df_temp_f[df_temp_f["avg_temp"]>21].shape[0]
    t1_total = max(df_temp_f.shape[0],1)
    t1_warm = max(selected_regions, key=lambda r: (
        df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["year"]>=2015)]["avg_temp"].mean() -
        df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["year"]<=1970)]["avg_temp"].mean()
    )) if selected_regions else "—"
    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {BROWN_MID};
                border:0.5px solid rgba(107,58,42,0.2);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">What you are looking at</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Showing <strong>{len(selected_regions)} region(s)</strong> · {year_range[0]}–{year_range[1]}</li>
        <li>Average temp across selection: <strong>{t1_avg:.1f}°C</strong> — ideal ceiling is 21°C</li>
        <li><strong>{t1_hot}</strong> runs the hottest on average</li>
        <li><strong>{t1_warm}</strong> has warmed the most since the 1960s</li>
        <li><strong>{t1_above} of {t1_total}</strong> region-years ({t1_above/t1_total*100:.0f}%) sit above 21°C</li>
        <li>Heatmap: <span style="color:#1A5276;font-weight:500">blue</span> = below ideal · <span style="color:#8B0000;font-weight:500">red</span> = above ideal</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = go.Figure()
        fig.add_hrect(y0=18, y1=21, fillcolor="rgba(168,213,162,0.2)", line_width=0,
                      annotation_text="Ideal range", annotation_font_color=BROWN_WARM, annotation_font_size=10)
        for region in selected_regions:
            r = df_temp_f[df_temp_f["region"]==region].sort_values("year")
            fig.add_trace(go.Scatter(x=r["year"], y=r["avg_temp"], name=region, mode="lines",
                line=dict(color=REGION_COLORS[region], width=2.5),
                hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:.1f}}°C<extra></extra>"))
        fig.add_hline(y=21, line_dash="dot", line_color=BROWN_WARM, line_width=1,
                      annotation_text="21°C ceiling", annotation_font_color=BROWN_WARM)
        fig.update_layout(**PLOT_LAYOUT, height=380, xaxis_title="Year", yaxis_title="°C")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        mg = df_temp_f[df_temp_f["region"]=="Minas Gerais"].sort_values("year")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_tmax"], name="Tmax", mode="lines",
                                  line=dict(color="#8B0000", width=2)))
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_tmin"], name="Tmin", mode="lines",
                                  line=dict(color="#1A5276", width=2),
                                  fill="tonexty", fillcolor="rgba(232,160,184,0.15)"))
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_temp"], name="Mean", mode="lines",
                                  line=dict(color=BROWN_MID, width=2, dash="dash")))
        fig2.add_hrect(y0=18, y1=21, fillcolor="rgba(168,213,162,0.2)", line_width=0)
        fig2.update_layout(**PLOT_LAYOUT, height=380, xaxis_title="Year", yaxis_title="°C")
        st.plotly_chart(fig2, use_container_width=True)

    pivot_heat = df_temp_f.pivot_table(index="region", columns="year", values="deviation")
    fig3 = go.Figure(data=go.Heatmap(
        z=pivot_heat.values, x=pivot_heat.columns.tolist(), y=pivot_heat.index.tolist(),
        colorscale=[[0.0,"#1A5276"],[0.3,"#5DADE2"],[0.45,"#A8D5A2"],
                    [0.55,"#A8D5A2"],[0.7,"#F0A500"],[0.85,"#D45500"],[1.0,"#8B0000"]],
        zmid=0, colorbar=dict(title="°C from ideal", tickfont_size=10, title_font_color=BROWN_DARK),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:+.1f}°C<extra></extra>",
    ))
    fig3.update_layout(**PLOT_LAYOUT, height=280, xaxis_title="Year", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

# ══ TAB 2: PRODUCTION ════════════════════════════════════════
with tab2:
    t2_latest = df_prod_f["year"].max() if not df_prod_f.empty else year_range[1]
    t2_top = df_prod_f[df_prod_f["year"]==t2_latest].nlargest(1,"production")
    t2_top_name = t2_top["country"].values[0] if not t2_top.empty else "—"
    t2_top_val  = t2_top["production"].values[0] if not t2_top.empty else 0
    t2_total    = df_prod_f[df_prod_f["year"]==t2_latest]["production"].sum()
    t2_share    = t2_top_val / max(t2_total,1) * 100
    t2_ara_pct  = df_prod_f[df_prod_f["year"]==t2_latest]["arabica_production"].sum() / max(t2_total,1) * 100
    t2_growth   = df_prod_f.groupby("country")["production"].apply(
        lambda x: x.iloc[-1]-x.iloc[0] if len(x)>1 else 0).idxmax() if not df_prod_f.empty else "—"
    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {BROWN_WARM};
                border:0.5px solid rgba(160,82,45,0.2);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">What you are looking at</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Showing <strong>{len(selected_countries)} countr{"y" if len(selected_countries)==1 else "ies"}</strong> · {year_range[0]}–{year_range[1]}</li>
        <li>Total production in <strong>{t2_latest}</strong>: <strong>{t2_total:,.0f}</strong> thousand 60kg bags</li>
        <li><strong>{t2_top_name}</strong> leads — <strong>{t2_share:.1f}%</strong> of this selection</li>
        <li>Arabica makes up <strong>{t2_ara_pct:.0f}%</strong> of production in the latest year</li>
        <li><strong>{t2_growth}</strong> has grown production the most over the selected period</li>
        <li>Units: thousands of 60kg bags per year (industry standard)</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig4 = go.Figure()
        for country in selected_countries:
            c = df_prod_f[df_prod_f["country"]==country].sort_values("year")
            fig4.add_trace(go.Scatter(x=c["year"], y=c["production"], name=country, mode="lines",
                line=dict(color=COUNTRY_COLORS[country], width=2.5),
                hovertemplate=f"<b>{country}</b><br>%{{x}}: %{{y:,.0f}}<extra></extra>"))
        fig4.update_layout(**PLOT_LAYOUT, height=380, xaxis_title="Year", yaxis_title="1,000 × 60kg bags")
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        latest = df_prod_f["year"].max()
        snap = df_prod_f[df_prod_f["year"]==latest]
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(name="Arabica", x=snap["country"],
                              y=snap["arabica_production"], marker_color=BROWN_MID))
        fig5.add_trace(go.Bar(name="Robusta", x=snap["country"],
                              y=snap["robusta_production"], marker_color=PINK_DEEP))
        fig5.update_layout(**PLOT_LAYOUT, barmode="stack", height=380, yaxis_title="1,000 × 60kg bags")
        st.plotly_chart(fig5, use_container_width=True)

    snap2 = df_prod_f[df_prod_f["year"]==latest]
    fig6 = go.Figure(go.Pie(
        labels=snap2["country"], values=snap2["production"], hole=0.55,
        marker_colors=[COUNTRY_COLORS[c] for c in snap2["country"]], textfont_size=12,
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig6.add_annotation(text=f"<b>{latest}</b>", x=0.5, y=0.5,
        font=dict(family="Playfair Display", size=18, color=BROWN_DARK), showarrow=False)
    fig6.update_layout(**PLOT_LAYOUT, height=320, showlegend=True)
    st.plotly_chart(fig6, use_container_width=True)

# ══ TAB 3: RISK ══════════════════════════════════════════════
with tab3:
    t3_ideal = df_temp_f[df_temp_f["region"].isin(selected_regions) & (df_temp_f["temp_status"]=="ideal")].shape[0]
    t3_total = max(df_temp_f[df_temp_f["region"].isin(selected_regions)].shape[0],1)
    t3_danger = df_temp_f[df_temp_f["region"].isin(selected_regions) & df_temp_f["temp_status"].isin(["at risk","danger"])].shape[0]
    t3_worst  = max(selected_regions, key=lambda r: df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["deviation"]>0)].shape[0]) if selected_regions else "—"
    t3_safest = min(selected_regions, key=lambda r: df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["deviation"]>0)].shape[0]) if selected_regions else "—"
    t3_early  = df_temp_f[df_temp_f["region"].isin(selected_regions)&(df_temp_f["year"]<1980)&(df_temp_f["deviation"]>0)].shape[0]
    t3_recent = df_temp_f[df_temp_f["region"].isin(selected_regions)&(df_temp_f["year"]>=2005)&(df_temp_f["deviation"]>0)].shape[0]
    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {PINK_DEEP};
                border:0.5px solid rgba(212,120,154,0.25);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">What you are looking at</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Only <strong>{t3_ideal} of {t3_total}</strong> region-years ({t3_ideal/t3_total*100:.0f}%) fell within the ideal 18–21°C range</li>
        <li><strong>{t3_danger}</strong> region-years reached "at risk" or "danger" status (above 24°C)</li>
        <li><strong>{t3_worst}</strong> has spent the most years above ideal</li>
        <li><strong>{t3_safest}</strong> has stayed closest to the ideal range</li>
        <li>Heat stress years before 1980: <strong>{t3_early}</strong> → since 2005: <strong>{t3_recent}</strong> — {"accelerating ↑" if t3_recent > t3_early else "stable →"}</li>
        <li>Risk scale: ideal · cool stress · heat stress · at risk · danger</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        status_order = ["ideal","cool stress","heat stress","at risk","danger"]
        fig7 = go.Figure()
        for status in status_order:
            counts = [df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["temp_status"]==status)].shape[0] for r in selected_regions]
            fig7.add_trace(go.Bar(name=status.title(), x=selected_regions, y=counts,
                marker_color=TEMP_COLORS[status],
                hovertemplate=f"<b>{status}</b><br>%{{x}}: %{{y}} years<extra></extra>"))
        fig7.update_layout(**PLOT_LAYOUT, barmode="stack", height=380, xaxis_tickangle=-25)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        fig8 = go.Figure()
        fig8.add_hrect(y0=-3, y1=0, fillcolor="rgba(26,82,118,0.08)", line_width=0)
        fig8.add_hrect(y0=0,  y1=10, fillcolor="rgba(139,0,0,0.05)",  line_width=0)
        fig8.add_hline(y=0, line_color=BROWN_WARM, line_width=1, line_dash="dot")
        for region in selected_regions:
            r = df_temp_f[df_temp_f["region"]==region].sort_values("year")
            fig8.add_trace(go.Scatter(x=r["year"], y=r["deviation"], name=region, mode="lines",
                line=dict(color=REGION_COLORS[region], width=2),
                hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:+.1f}}°C<extra></extra>"))
        fig8.update_layout(**PLOT_LAYOUT, height=380, xaxis_title="Year", yaxis_title="°C above ideal ceiling")
        st.plotly_chart(fig8, use_container_width=True)

    decades = list(range(1960, 2030, 10))
    fig9 = go.Figure()
    for region in selected_regions:
        counts = [df_temp[(df_temp["region"]==region)&(df_temp["year"]>=d)&(df_temp["year"]<d+10)&(df_temp["deviation"]>0)].shape[0] for d in decades]
        fig9.add_trace(go.Scatter(x=[f"{d}s" for d in decades], y=counts, name=region,
            mode="lines+markers", line=dict(color=REGION_COLORS[region], width=2.5), marker=dict(size=7)))
    fig9.update_layout(**PLOT_LAYOUT, height=300, xaxis_title="Decade", yaxis_title="Years above 21°C")
    st.plotly_chart(fig9, use_container_width=True)

# ══ TAB 4: TEMP vs OUTPUT ════════════════════════════════════
with tab4:
    t4_corr = df_merged_f["avg_temp"].corr(df_merged_f["production"]) if len(df_merged_f)>2 else 0
    t4_stress = df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"])]
    t4_normal = df_merged_f[df_merged_f["temp_status"].isin(["ideal","cool stress"])]
    t4_drop   = df_merged_f[df_merged_f["prod_change_%"]<0].shape[0]
    t4_both   = df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"]) & (df_merged_f["prod_change_%"]<0)].shape[0]
    t4_corr_label = ("negative — higher temps linked to lower output" if t4_corr < -0.3
                     else "positive — output grew despite rising temps" if t4_corr > 0.3
                     else "weak — temperature alone doesn't explain output changes")
    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid #8B0000;
                border:0.5px solid rgba(139,0,0,0.2);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">What you are looking at</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Correlation between temperature and production: <strong>r = {t4_corr:.3f}</strong> — {t4_corr_label}</li>
        <li>Production dropped in <strong>{t4_drop}</strong> of {len(df_merged_f)} years in the selected range</li>
        <li><strong>{t4_both}</strong> of those drop years also had above-ideal temperatures</li>
        <li>Avg production in heat stress years: <strong>{t4_stress["production"].mean():,.0f}</strong> vs <strong>{t4_normal["production"].mean():,.0f}</strong> in normal years</li>
        <li>Bars: <span style="color:{BROWN_MID};font-weight:500">brown</span> = within ideal · <span style="color:#D45500;font-weight:500">orange</span> = heat stress · <span style="color:#8B0000;font-weight:500">red</span> = danger</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    fig10 = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = ["#8B0000" if s in ["at risk","danger"] else "#D45500" if s=="heat stress" else BROWN_MID for s in df_merged_f["temp_status"]]
    fig10.add_trace(go.Bar(x=df_merged_f["year"], y=df_merged_f["production"], name="Production",
        marker_color=bar_colors, opacity=0.8,
        hovertemplate="<b>%{x}</b><br>Production: %{y:,.0f}<extra></extra>"), secondary_y=False)
    fig10.add_trace(go.Scatter(x=df_merged_f["year"], y=df_merged_f["avg_temp"], name="Avg temp (°C)",
        mode="lines+markers", line=dict(color=PINK_DEEP, width=2.5), marker=dict(size=5, color=PINK_DEEP),
        hovertemplate="<b>%{x}</b><br>Temp: %{y:.1f}°C<extra></extra>"), secondary_y=True)
    fig10.add_hrect(y0=18, y1=21, secondary_y=True, fillcolor="rgba(168,213,162,0.15)", line_width=0)
    fig10.add_hline(y=21, secondary_y=True, line_dash="dot", line_color=PINK_DEEP, line_width=1, opacity=0.6)
    fig10.update_layout(**PLOT_LAYOUT, height=420, xaxis_title="Year")
    fig10.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig10.update_yaxes(title_text="Production (1k × 60kg bags)", secondary_y=False, color=BROWN_MID)
    fig10.update_yaxes(title_text="Temperature °C", secondary_y=True, color=PINK_DEEP)
    st.plotly_chart(fig10, use_container_width=True)

    corr = df_merged_f["avg_temp"].corr(df_merged_f["production"])
    direction = "negative" if corr < -0.3 else "positive" if corr > 0.3 else "weak"
    corr_color = "#8B0000" if corr < -0.3 else BROWN_MID if corr > 0.3 else BROWN_WARM
    st.markdown(f"""
    <div style="background:white;border-left:4px solid {corr_color};border-radius:0 12px 12px 0;
                padding:20px 24px;margin-top:20px;box-shadow:2px 4px 12px rgba(44,26,14,0.07);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 6px;">Correlation insight</p>
      <p style="font-family:'Playfair Display';font-size:20px;color:{BROWN_DARK};margin:0 0 8px;">
          r = {corr:.3f} — {direction} correlation</p>
      <p style="font-size:13px;color:#555;margin:0;line-height:1.6;">
          {"Higher temperatures are linked to lower production in this period." if corr < -0.3
           else "Production grew despite rising temperatures — other factors dominate." if corr > 0.3
           else "Temperature alone does not fully explain production changes."}</p>
    </div>
    """, unsafe_allow_html=True)

# ══ TAB 5: CONCLUSIONS ═══════════════════════════════════════
with tab5:
    c_above = df_temp_f[df_temp_f["avg_temp"]>21].shape[0]
    c_all   = max(df_temp_f.shape[0],1)
    c_trend = (df_temp_f[df_temp_f["year"]>=2015]["avg_temp"].mean() -
               df_temp_f[df_temp_f["year"]<=1970]["avg_temp"].mean()) if not df_temp_f.empty else 0
    c_corr  = df_merged_f["avg_temp"].corr(df_merged_f["production"]) if len(df_merged_f)>2 else 0
    c_drop  = df_merged_f[df_merged_f["prod_change_%"]<0].shape[0]
    c_both  = df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"]) & (df_merged_f["prod_change_%"]<0)].shape[0]

    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:28px;border-left:4px solid {PINK_DEEP};
                border:0.5px solid rgba(212,120,154,0.25);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">Key findings — updates with your filter selection</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li><strong>{c_above/c_all*100:.0f}%</strong> of selected region-years sit above the 21°C ideal ceiling</li>
        <li>Average warming across selected regions since the 1960s: <strong>+{c_trend:.1f}°C</strong></li>
        <li>Temperature vs production correlation: <strong>r = {c_corr:.2f}</strong></li>
        <li>Production dropped in <strong>{c_drop}</strong> years — <strong>{c_both}</strong> of those also had above-ideal temperatures</li>
        <li>Heat stress years are becoming more frequent in the most recent decades</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(44,26,14,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;color:#8B0000;margin:0;">
              {c_above/c_all*100:.0f}%</p>
          <p style="font-size:12px;color:{BROWN_WARM};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">region-years above ideal</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(44,26,14,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;color:{BROWN_MID};margin:0;">
              +{c_trend:.1f}°C</p>
          <p style="font-size:12px;color:{BROWN_WARM};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">avg warming since 1960s</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(44,26,14,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;color:{PINK_DEEP};margin:0;">
              {c_corr:.2f}</p>
          <p style="font-size:12px;color:{BROWN_WARM};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">temp vs production r</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="max-width:740px;">
      <p style="font-family:'Playfair Display';font-size:22px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 14px;">What the data says</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 16px;">
          Brazil's coffee regions are warming. The rate is gradual —
          roughly +{c_trend:.1f}°C across the selected period — but consistent,
          and accelerating in the most recent decades. Regions that were already
          warm, like Bahia and Rondônia, now spend almost no years within the
          ideal Arabica range.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 16px;">
          Production tells a more complicated story. Brazil has continued growing
          output despite rising temperatures — driven by technology, irrigation,
          and varietal adaptation. The correlation between temperature and
          production is r = {c_corr:.2f}, suggesting temperature is a factor
          but not the only one.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 24px;">
          The real risk is not today's harvest. It is the compound effect of years
          outside the ideal window and the narrowing of suitable growing altitude.
          The question this project started with —
          <em>what will the beans be like in a few years?</em> — does not have a
          simple answer. But the direction is clear.</p>
      <p style="font-family:'Playfair Display';font-size:22px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 14px;">Limitations</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 8px;">
          This analysis focuses on temperature only. A complete picture would also include
          rainfall, soil quality, pest pressure, altitude shifts, and economic factors.
          Production data from USDA PSD is a reliable aggregate but does not capture
          farm-level variation within regions.</p>
      <p style="font-size:13px;color:{BROWN_WARM};margin:24px 0 0;font-style:italic;">
          A mini project by <strong>Tulasi Arvind</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ══ TAB 6: SOURCES ════════════════════════════════════════════
with tab6:
    st.markdown(f"""
    <div style="background:{BROWN_CREAM};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {BROWN_LIGHT};
                border:0.5px solid rgba(200,149,108,0.3);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 10px;">About the data</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Three datasets — all publicly available and free to access</li>
        <li>Temperature data: <strong>1,194 weather stations</strong> across Brazil, 1961–2024</li>
        <li>Production data: <strong>top 5 producing countries</strong> from the USDA PSD database</li>
        <li>Arabica ideal range of <strong>18–21°C</strong> sourced from NOAA Climate.gov</li>
        <li>Click any link below to view the original source</li>
      </ul>
    </div>
    <p style="font-family:'Playfair Display';font-size:28px;font-weight:700;
               color:{BROWN_DARK};margin-bottom:6px;">Data sources</p>
    <p style="font-size:14px;color:{BROWN_WARM};margin-bottom:32px;line-height:1.6;">
        All datasets and references used in this analysis.</p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="source-card" style="border-left-color:{BROWN_MID};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 8px;">01 — Brazil temperature data</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">
          New improved Brazilian daily weather gridded data (1961–2020)</p>
      <p style="font-size:13px;color:#555;margin:0 0 12px;line-height:1.7;">
          Xavier, A. C., Scanlon, B. R., King, C. W., &amp; Alves, A. I. (2022).
          <em>International Journal of Climatology</em>, 42(16), 8390–8404.</p>
      <a href="https://doi.org/10.1002/joc.7731" target="_blank">https://doi.org/10.1002/joc.7731</a>
    </div>
    <div class="source-card" style="border-left-color:{BROWN_WARM};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 8px;">02 — Coffee production data</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">
          USDA Foreign Agricultural Service — Production, Supply &amp; Distribution</p>
      <p style="font-size:13px;color:#555;margin:0 0 12px;line-height:1.7;">
          United States Department of Agriculture (USDA). PSD Online database.
          Commodity: Coffee, Green (0711100).</p>
      <a href="https://www.fas.usda.gov/data/production/0711100" target="_blank">
          https://www.fas.usda.gov/data/production/0711100</a>
    </div>
    <div class="source-card" style="border-left-color:{PINK_DEEP};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{BROWN_WARM};margin:0 0 8px;">03 — Arabica ideal temperature range</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">Climate &amp; Coffee — NOAA Climate.gov</p>
      <p style="font-size:13px;color:#555;margin:0 0 12px;line-height:1.7;">
          National Oceanic and Atmospheric Administration (NOAA).
          Climate conditions for coffee cultivation including the 18–21°C ideal range.</p>
      <a href="https://www.climate.gov/news-features/climate-and/climate-coffee" target="_blank">
          https://www.climate.gov/news-features/climate-and/climate-coffee</a>
    </div>
    <div style="background:{PINK_PALE};border-radius:10px;padding:16px 20px;
                margin-top:8px;border:0.5px solid {PINK_MID};">
      <p style="font-size:12px;color:{BROWN_WARM};margin:0;line-height:1.7;">
          <strong>Note:</strong> Temperature analysis covers 1961–2024 using daily station data
          from 1,194 weather stations across Brazil. Production data sourced from USDA PSD
          covers Brazil, Vietnam, Colombia, Indonesia, and Ethiopia.
          The Arabica ideal range of 18–21°C is the benchmark throughout.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;opacity:0.45;font-size:12px;
             letter-spacing:0.08em;text-transform:uppercase;">
    Tulasi Arvind &nbsp;·&nbsp; USDA PSD · Xavier et al. (2022) · NOAA Climate.gov
</div>
""", unsafe_allow_html=True)