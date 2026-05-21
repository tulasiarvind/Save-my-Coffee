# ================================================================
# SAVE MY COFFEE — INTERACTIVE STREAMLIT DASHBOARD
# By Tulasi Arvind
# Run: python3 -m streamlit run coffee_dashboard.py
# ================================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Save My Coffee",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── COLOURS — from uploaded palette ───────────────────────────
ROSE       = "#DF939D"
BLUSH      = "#E3BBBC"
CREAM      = "#F7EFDA"
SAGE       = "#989769"
BROWN      = "#6F5D4F"
BROWN_DARK = "#3D2E24"
CREAM_DARK = "#EDE0C4"
SAGE_DARK  = "#6B6846"
WHITE      = "#FFFDF7"

HEART_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDMyIDMyIj4KICA8cGF0aCBkPSJNMTYgMjggQzE2IDI4IDQgMjAgNCAxMiBDNCA3LjYgNy42IDQgMTIgNCBDMTQuMiA0IDE2IDYgMTYgNiBDMTYgNiAxNy44IDQgMjAgNCBDMjQuNCA0IDI4IDcuNiAyOCAxMiBDMjggMjAgMTYgMjggMTYgMjhaIiBmaWxsPSIjREY5MzlEIiBzdHJva2U9IiM2RjVENEYiIHN0cm9rZS13aWR0aD0iMS41Ii8+Cjwvc3ZnPg=="

TEMP_COLORS = {
    "too cold":    "#4A90C4",
    "cool stress": "#85B7D9",
    "ideal":       "#A8C5A0",
    "heat stress": "#C8A96E",
    "at risk":     "#B5714A",
    "danger":      "#8B3A3A",
}
REGION_COLORS = {
    "Minas Gerais":   BROWN,
    "Espirito Santo": SAGE,
    "Sao Paulo":      ROSE,
    "Bahia":          BLUSH,
    "Rondonia":       SAGE_DARK,
}
COUNTRY_COLORS = {
    "Brazil":    BROWN,
    "Vietnam":   "#8B3A3A",
    "Colombia":  SAGE,
    "Indonesia": ROSE,
    "Ethiopia":  BLUSH,
}

# ── CSS ───────────────────────────────────────────────────────
CURSOR = f"url('data:image/svg+xml;base64,{HEART_B64}') 16 16"
css = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');
  html, body, [class*="css"] {{
      font-family: 'DM Sans', sans-serif;
      background-color: {CREAM};
      color: {BROWN_DARK};
      cursor: {CURSOR}, auto;
  }}
  a, button, [data-baseweb="tab"], .stSelectbox, .stMultiSelect,
  .stSlider, [data-testid="metric-container"] {{
      cursor: {CURSOR}, pointer;
  }}
  .stApp {{ background-color: {CREAM}; }}
  [data-testid="stSidebar"] {{ display: none; }}
  h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: {BROWN_DARK}; }}
  [data-testid="metric-container"] {{
      background: {WHITE};
      border: 1px solid {CREAM_DARK};
      border-radius: 12px;
      padding: 16px;
      box-shadow: 2px 4px 12px rgba(61,46,36,0.08);
  }}
  [data-testid="metric-container"] label {{
      color: {SAGE_DARK} !important;
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
      border-bottom: 2px solid rgba(111,93,79,0.2);
      gap: 6px;
      padding: 0;
  }}
  .stTabs [data-baseweb="tab"] {{
      font-family: 'DM Sans', sans-serif;
      font-size: 12px;
      letter-spacing: 0.04em;
      color: {BROWN};
      background: {CREAM_DARK};
      border: 1.5px solid rgba(111,93,79,0.25);
      border-bottom: none;
      border-radius: 8px 8px 0 0;
      padding: 8px 18px 10px 14px;
      position: relative;
      top: 2px;
      transition: background 0.15s;
  }}
  .stTabs [data-baseweb="tab"]:hover {{ background: {BLUSH} !important; }}
  .stTabs [aria-selected="true"] {{
      background-color: {WHITE} !important;
      color: {BROWN_DARK} !important;
      border-color: rgba(111,93,79,0.35) !important;
      border-bottom: 2px solid {WHITE} !important;
      font-weight: 500;
  }}
  .stTabs [data-baseweb="tab-panel"] {{
      background: {WHITE};
      border-radius: 0 12px 12px 12px;
      padding: 24px;
      border: 1.5px solid rgba(111,93,79,0.15);
      border-top: none;
  }}
  .filter-bar {{
      background: {CREAM_DARK};
      border-radius: 12px;
      padding: 16px 24px;
      margin-bottom: 24px;
      border: 0.5px solid rgba(111,93,79,0.2);
      display: flex;
      align-items: center;
      gap: 24px;
  }}
  .source-card {{
      background: {WHITE};
      border-radius: 14px;
      padding: 24px 28px;
      margin-bottom: 16px;
      box-shadow: 2px 4px 16px rgba(61,46,36,0.07);
      border-left: 5px solid {BROWN};
  }}
  .source-card a {{ color: {SAGE_DARK}; text-decoration: none; font-weight: 500; word-break: break-all; }}
  .source-card a:hover {{ color: {ROSE}; text-decoration: underline; }}
  hr {{ border-color: {BLUSH}; opacity: 0.5; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ── PLOTLY DEFAULTS ───────────────────────────────────────────
def plot_layout(title=""):
    return dict(
        title=title,
        font_family="DM Sans", font_color=BROWN_DARK,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=f"rgba(237,224,196,0.25)",
        title_font_family="Playfair Display",
        title_font_color=BROWN_DARK, title_font_size=15,
        legend=dict(bgcolor="rgba(255,253,247,0.8)", bordercolor=CREAM_DARK, borderwidth=1, font_size=11),
        margin=dict(t=55, b=40, l=40, r=20),
    )

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{BROWN_DARK} 0%,{BROWN} 55%,{SAGE} 100%);
            border-radius:16px;padding:40px 48px;margin-bottom:24px;
            position:relative;overflow:hidden;">
  <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
              border-radius:50%;background:rgba(223,147,157,0.15);"></div>
  <div style="position:absolute;bottom:-60px;right:80px;width:140px;height:140px;
              border-radius:50%;background:rgba(152,151,105,0.12);"></div>
  <p style="font-size:11px;letter-spacing:0.2em;text-transform:uppercase;
             color:{BLUSH};margin:0 0 8px;">Climate Risk Analysis · Tulasi Arvind</p>
  <h1 style="font-family:'Playfair Display';font-size:42px;font-weight:900;
              color:{CREAM};margin:0 0 12px;line-height:1.1;">Save My Coffee</h1>
  <p style="font-size:15px;color:{BLUSH};margin:0;max-width:560px;line-height:1.6;opacity:0.9;">
      How rising temperatures are threatening the world's top coffee producers —
      with a deep dive into Brazil's Arabica growing regions.
  </p>
</div>
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

ALL_REGIONS   = sorted(df_temp["region"].unique().tolist())
ALL_COUNTRIES = sorted(df_prod["country"].unique().tolist())
DATA_MIN_YEAR = int(df_temp["year"].min())
DATA_MAX_YEAR = int(df_temp["year"].max())

# ── YEAR FILTER BAR — above all graphs ────────────────────────
st.markdown(f"""
<div style="background:{CREAM_DARK};border-radius:12px;padding:14px 24px 4px;
            margin-bottom:20px;border:0.5px solid rgba(111,93,79,0.2);">
  <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
             color:{SAGE_DARK};margin:0 0 4px;">Filter by year range</p>
</div>
""", unsafe_allow_html=True)

year_range = st.slider(
    "", min_value=DATA_MIN_YEAR, max_value=DATA_MAX_YEAR,
    value=(1990, DATA_MAX_YEAR), label_visibility="collapsed"
)

# ── FILTERED DATA ─────────────────────────────────────────────
df_temp_f   = df_temp[df_temp["year"].between(*year_range)]
df_prod_f   = df_prod[df_prod["year"].between(*year_range)]
df_merged_f = df_merged[df_merged["year"].between(*year_range)]

# ── KPI METRICS ───────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
latest_year = df_temp_f["year"].max() if not df_temp_f.empty else year_range[1]
latest_temp = df_temp_f[(df_temp_f["region"]=="Minas Gerais")&(df_temp_f["year"]==latest_year)]["avg_temp"].values
with k1:
    st.metric("Latest avg temp", f"{latest_temp[0]:.1f}°C" if len(latest_temp) else "—", delta="Minas Gerais")
with k2:
    sy = df_temp_f[(df_temp_f["region"]=="Minas Gerais")&(df_temp_f["temp_status"].isin(["heat stress","at risk","danger"]))].shape[0]
    st.metric("Heat stress years", sy, delta="above 21°C")
with k3:
    lp = df_prod_f[(df_prod_f["country"]=="Brazil")&(df_prod_f["year"]==df_prod_f["year"].max())]["production"].values
    st.metric("Brazil production", f"{lp[0]:,.0f}" if len(lp) else "—", delta="1k × 60kg bags")
with k4:
    ad = df_temp_f[df_temp_f["region"]=="Minas Gerais"]["deviation"].mean()
    st.metric("Avg deviation", f"+{ad:.1f}°C" if (not np.isnan(ad) and ad>0) else (f"{ad:.1f}°C" if not np.isnan(ad) else "No data"), delta="from 21°C ceiling")
with k5:
    ip = df_temp_f[df_temp_f["temp_status"]=="ideal"].shape[0] / max(df_temp_f.shape[0],1)*100
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
                 color:{SAGE_DARK};margin:0 0 10px;">A project by Tulasi Arvind</p>
      <p style="font-family:'Playfair Display';font-size:36px;font-weight:900;
                 color:{BROWN_DARK};line-height:1.2;margin:0 0 28px;">It started with an iced latte.</p>
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
      <div style="border-left:4px solid {ROSE};padding:16px 24px;
                  background:{CREAM_DARK};border-radius:0 12px 12px 0;margin-bottom:32px;">
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
      <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                  border:0.5px solid rgba(111,93,79,0.2);">
        <ul style="font-size:14px;color:{BROWN_DARK};line-height:2.2;margin:0;padding-left:18px;">
          <li>Use the <strong>year slider</strong> above the tabs to filter all charts at once</li>
          <li><strong>🌡️ Temperature</strong> — how each region's avg temp has changed since 1960</li>
          <li><strong>☕ Production</strong> — output volumes for the top 5 producing countries</li>
          <li><strong>⚠️ Risk</strong> — years each region spent outside the ideal 18–21°C window</li>
          <li><strong>🔗 Temp vs output</strong> — do hotter years mean less coffee?</li>
          <li><strong>📝 Conclusions</strong> — what the data actually says</li>
        </ul>
      </div>
      <p style="font-size:13px;color:{SAGE_DARK};margin:20px 0 0;font-style:italic;">
          Built with Python · Streamlit · Plotly · Data from USDA PSD & Xavier et al. (2022)</p>
    </div>
    """, unsafe_allow_html=True)

# ══ TAB 1: TEMPERATURE ═══════════════════════════════════════
with tab1:
    t1_avg   = df_temp_f["avg_temp"].mean()
    t1_above = df_temp_f[df_temp_f["avg_temp"]>21].shape[0]
    t1_total = max(df_temp_f.shape[0],1)
    t1_hot   = max(ALL_REGIONS, key=lambda r: df_temp_f[df_temp_f["region"]==r]["avg_temp"].mean()) if not df_temp_f.empty else "—"
    t1_warm  = max(ALL_REGIONS, key=lambda r: (
        df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["year"]>=year_range[1]-9)]["avg_temp"].mean() -
        df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["year"]<=year_range[0]+9)]["avg_temp"].mean()
    )) if not df_temp_f.empty else "—"

    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {BROWN};
                border:0.5px solid rgba(111,93,79,0.2);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">What you are looking at · {year_range[0]}–{year_range[1]}</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Average temp across all regions {year_range[0]}–{year_range[1]}: <strong>{t1_avg:.1f}°C</strong> — ideal ceiling is 21°C</li>
        <li><strong>{t1_hot}</strong> runs the hottest on average in this period</li>
        <li><strong>{t1_warm}</strong> has warmed the most across the selected range</li>
        <li><strong>{t1_above} of {t1_total}</strong> region-years ({t1_above/t1_total*100:.0f}%) sit above 21°C</li>
        <li>Heatmap: <span style="color:#4A90C4;font-weight:500">blue</span> = below ideal · <span style="color:#8B3A3A;font-weight:500">red</span> = above ideal</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = go.Figure()
        fig.add_hrect(y0=18, y1=21, fillcolor="rgba(168,197,160,0.2)", line_width=0,
                      annotation_text="Ideal range", annotation_font_color=SAGE_DARK, annotation_font_size=10)
        for region in ALL_REGIONS:
            r = df_temp_f[df_temp_f["region"]==region].sort_values("year")
            fig.add_trace(go.Scatter(x=r["year"], y=r["avg_temp"], name=region, mode="lines",
                line=dict(color=REGION_COLORS[region], width=2.5),
                hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:.1f}}°C<extra></extra>"))
        fig.add_hline(y=21, line_dash="dot", line_color=SAGE_DARK, line_width=1,
                      annotation_text="21°C ceiling", annotation_font_color=SAGE_DARK)
        fig.update_layout(**plot_layout(f"Average temperature per region · {year_range[0]}–{year_range[1]}"),
                          height=380, xaxis_title="Year", yaxis_title="°C")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        mg = df_temp_f[df_temp_f["region"]=="Minas Gerais"].sort_values("year")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_tmax"], name="Tmax", mode="lines",
                                  line=dict(color="#8B3A3A", width=2)))
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_tmin"], name="Tmin", mode="lines",
                                  line=dict(color="#4A90C4", width=2),
                                  fill="tonexty", fillcolor="rgba(227,187,188,0.2)"))
        fig2.add_trace(go.Scatter(x=mg["year"], y=mg["avg_temp"], name="Mean", mode="lines",
                                  line=dict(color=BROWN, width=2, dash="dash")))
        fig2.add_hrect(y0=18, y1=21, fillcolor="rgba(168,197,160,0.2)", line_width=0)
        fig2.update_layout(**plot_layout(f"Minas Gerais — Tmax / Tmin · {year_range[0]}–{year_range[1]}"),
                           height=380, xaxis_title="Year", yaxis_title="°C")
        st.plotly_chart(fig2, use_container_width=True)

    if not df_temp_f.empty:
        pivot_heat = df_temp_f.pivot_table(index="region", columns="year", values="deviation")
        fig3 = go.Figure(data=go.Heatmap(
            z=pivot_heat.values, x=pivot_heat.columns.tolist(), y=pivot_heat.index.tolist(),
            colorscale=[[0.0,"#4A90C4"],[0.3,"#85B7D9"],[0.45,"#A8C5A0"],
                        [0.55,"#A8C5A0"],[0.7,"#C8A96E"],[0.85,"#B5714A"],[1.0,"#8B3A3A"]],
            zmid=0,
            colorbar=dict(title="°C from ideal", tickfont_size=10, title_font_color=BROWN_DARK),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:+.1f}°C<extra></extra>",
        ))
        fig3.update_layout(**plot_layout(f"Deviation from ideal ceiling (21°C) · {year_range[0]}–{year_range[1]}"),
                           height=280, xaxis_title="Year", yaxis_title="")
        st.plotly_chart(fig3, use_container_width=True)

    # Scatter: avg temp vs deviation per region
    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:10px;padding:12px 18px;
                margin:16px 0 8px;border:0.5px solid rgba(111,93,79,0.15);">
      <p style="font-size:12px;color:{SAGE_DARK};margin:0;">
          <strong>Scatter:</strong> each dot is one region-year.
          Shows how avg temperature relates to deviation from the 21°C ideal ceiling.
      </p>
    </div>""", unsafe_allow_html=True)
    fig_sc1 = go.Figure()
    for region in ALL_REGIONS:
        r = df_temp_f[df_temp_f["region"]==region]
        fig_sc1.add_trace(go.Scatter(
            x=r["avg_temp"], y=r["deviation"], mode="markers", name=region,
            marker=dict(color=REGION_COLORS[region], size=6, opacity=0.7),
            hovertemplate=f"<b>{region}</b><br>Avg temp: %{{x:.1f}}°C<br>Deviation: %{{y:+.1f}}°C<extra></extra>",
        ))
    fig_sc1.add_vline(x=21, line_dash="dot", line_color=SAGE_DARK, line_width=1)
    fig_sc1.add_hline(y=0,  line_dash="dot", line_color=SAGE_DARK, line_width=1)
    fig_sc1.update_layout(**plot_layout(f"Avg temperature vs deviation from ideal · {year_range[0]}–{year_range[1]}"),
                          height=340, xaxis_title="Avg temperature (°C)", yaxis_title="Deviation from 21°C (°C)")
    st.plotly_chart(fig_sc1, use_container_width=True)

# ══ TAB 2: PRODUCTION ════════════════════════════════════════
with tab2:
    t2_latest  = df_prod_f["year"].max() if not df_prod_f.empty else year_range[1]
    t2_snap    = df_prod_f[df_prod_f["year"]==t2_latest]
    t2_total   = t2_snap["production"].sum()
    t2_top     = t2_snap.nlargest(1,"production")
    t2_top_name= t2_top["country"].values[0] if not t2_top.empty else "—"
    t2_top_val = t2_top["production"].values[0] if not t2_top.empty else 0
    t2_share   = t2_top_val / max(t2_total,1) * 100
    t2_ara_pct = t2_snap["arabica_production"].sum() / max(t2_total,1) * 100
    t2_growth  = (df_prod_f.groupby("country")["production"]
                  .apply(lambda x: x.iloc[-1]-x.iloc[0] if len(x)>1 else 0)
                  .idxmax()) if not df_prod_f.empty else "—"

    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {SAGE};
                border:0.5px solid rgba(152,151,105,0.3);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">What you are looking at · {year_range[0]}–{year_range[1]}</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Total production across top 5 in <strong>{t2_latest}</strong>: <strong>{t2_total:,.0f}</strong> thousand 60kg bags</li>
        <li><strong>{t2_top_name}</strong> leads — <strong>{t2_share:.1f}%</strong> of total in this selection</li>
        <li>Arabica makes up <strong>{t2_ara_pct:.0f}%</strong> of production in {t2_latest}</li>
        <li><strong>{t2_growth}</strong> has grown production the most over {year_range[0]}–{year_range[1]}</li>
        <li>Units: thousands of 60kg bags per year (industry standard)</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig4 = go.Figure()
        for country in ALL_COUNTRIES:
            c = df_prod_f[df_prod_f["country"]==country].sort_values("year")
            fig4.add_trace(go.Scatter(x=c["year"], y=c["production"], name=country, mode="lines",
                line=dict(color=COUNTRY_COLORS[country], width=2.5),
                hovertemplate=f"<b>{country}</b><br>%{{x}}: %{{y:,.0f}}<extra></extra>"))
        fig4.update_layout(**plot_layout(f"Production over time — top 5 · {year_range[0]}–{year_range[1]}"),
                           height=380, xaxis_title="Year", yaxis_title="1,000 × 60kg bags")
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        snap = df_prod_f[df_prod_f["year"]==t2_latest]
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(name="Arabica", x=snap["country"],
                              y=snap["arabica_production"], marker_color=SAGE))
        fig5.add_trace(go.Bar(name="Robusta", x=snap["country"],
                              y=snap["robusta_production"], marker_color=ROSE))
        fig5.update_layout(**plot_layout(f"Arabica vs Robusta · {t2_latest}"),
                           barmode="stack", height=380, yaxis_title="1,000 × 60kg bags")
        st.plotly_chart(fig5, use_container_width=True)

    snap2 = df_prod_f[df_prod_f["year"]==t2_latest]
    fig6 = go.Figure(go.Pie(
        labels=snap2["country"], values=snap2["production"], hole=0.55,
        marker_colors=[COUNTRY_COLORS[c] for c in snap2["country"]], textfont_size=12,
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig6.add_annotation(text=f"<b>{t2_latest}</b>", x=0.5, y=0.5,
        font=dict(family="Playfair Display", size=18, color=BROWN_DARK), showarrow=False)
    fig6.update_layout(**plot_layout(f"World share · {t2_latest}"), height=320, showlegend=True)
    st.plotly_chart(fig6, use_container_width=True)

    # Scatter: year vs production per country
    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:10px;padding:12px 18px;
                margin:16px 0 8px;border:0.5px solid rgba(111,93,79,0.15);">
      <p style="font-size:12px;color:{SAGE_DARK};margin:0;">
          <strong>Scatter:</strong> each dot is one country-year.
          Shows production volume over time with dot size scaled to Arabica share.
      </p>
    </div>""", unsafe_allow_html=True)
    fig_sc2 = go.Figure()
    for country in ALL_COUNTRIES:
        c = df_prod_f[df_prod_f["country"]==country].copy()
        c["ara_share"] = c["arabica_production"] / c["production"].replace(0, np.nan) * 100
        fig_sc2.add_trace(go.Scatter(
            x=c["year"], y=c["production"], mode="markers", name=country,
            marker=dict(color=COUNTRY_COLORS[country], size=c["ara_share"].fillna(10)/5+5, opacity=0.7),
            hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Production: %{{y:,.0f}}<br>Arabica share: %{{customdata:.0f}}%<extra></extra>",
            customdata=c["ara_share"].fillna(0),
        ))
    fig_sc2.update_layout(**plot_layout(f"Production scatter · {year_range[0]}–{year_range[1]} (dot size = Arabica share %)"),
                          height=360, xaxis_title="Year", yaxis_title="Production (1k × 60kg bags)")
    st.plotly_chart(fig_sc2, use_container_width=True)

# ══ TAB 3: RISK ══════════════════════════════════════════════
with tab3:
    t3_ideal  = df_temp_f[df_temp_f["temp_status"]=="ideal"].shape[0]
    t3_total  = max(df_temp_f.shape[0],1)
    t3_danger = df_temp_f[df_temp_f["temp_status"].isin(["at risk","danger"])].shape[0]
    t3_worst  = max(ALL_REGIONS, key=lambda r: df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["deviation"]>0)].shape[0]) if not df_temp_f.empty else "—"
    t3_safest = min(ALL_REGIONS, key=lambda r: df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["deviation"]>0)].shape[0]) if not df_temp_f.empty else "—"
    t3_early  = df_temp_f[(df_temp_f["year"]<=year_range[0]+9)&(df_temp_f["deviation"]>0)].shape[0]
    t3_recent = df_temp_f[(df_temp_f["year"]>=year_range[1]-9)&(df_temp_f["deviation"]>0)].shape[0]

    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {ROSE};
                border:0.5px solid rgba(223,147,157,0.3);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">What you are looking at · {year_range[0]}–{year_range[1]}</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Only <strong>{t3_ideal} of {t3_total}</strong> region-years ({t3_ideal/t3_total*100:.0f}%) fell within the ideal 18–21°C range</li>
        <li><strong>{t3_danger}</strong> region-years reached "at risk" or "danger" (above 24°C)</li>
        <li><strong>{t3_worst}</strong> has spent the most years above the ideal ceiling</li>
        <li><strong>{t3_safest}</strong> has stayed closest to the ideal range</li>
        <li>First decade heat stress years: <strong>{t3_early}</strong> → last decade: <strong>{t3_recent}</strong> — {"accelerating ↑" if t3_recent > t3_early else "stable →"}</li>
        <li>Risk scale: ideal · cool stress · heat stress · at risk · danger</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        status_order = ["ideal","cool stress","heat stress","at risk","danger"]
        fig7 = go.Figure()
        for status in status_order:
            counts = [df_temp_f[(df_temp_f["region"]==r)&(df_temp_f["temp_status"]==status)].shape[0] for r in ALL_REGIONS]
            fig7.add_trace(go.Bar(name=status.title(), x=ALL_REGIONS, y=counts,
                marker_color=TEMP_COLORS[status],
                hovertemplate=f"<b>{status}</b><br>%{{x}}: %{{y}} years<extra></extra>"))
        fig7.update_layout(**plot_layout(f"Years per risk status · {year_range[0]}–{year_range[1]}"),
                           barmode="stack", height=380, xaxis_tickangle=-25)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        fig8 = go.Figure()
        fig8.add_hrect(y0=-3, y1=0, fillcolor="rgba(74,144,196,0.08)", line_width=0)
        fig8.add_hrect(y0=0,  y1=10, fillcolor="rgba(139,58,58,0.05)",  line_width=0)
        fig8.add_hline(y=0, line_color=SAGE_DARK, line_width=1, line_dash="dot")
        for region in ALL_REGIONS:
            r = df_temp_f[df_temp_f["region"]==region].sort_values("year")
            fig8.add_trace(go.Scatter(x=r["year"], y=r["deviation"], name=region, mode="lines",
                line=dict(color=REGION_COLORS[region], width=2),
                hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:+.1f}}°C<extra></extra>"))
        fig8.update_layout(**plot_layout(f"Deviation from ideal over time · {year_range[0]}–{year_range[1]}"),
                           height=380, xaxis_title="Year", yaxis_title="°C above ideal ceiling")
        st.plotly_chart(fig8, use_container_width=True)

    decades = list(range(DATA_MIN_YEAR, DATA_MAX_YEAR+1, 10))
    fig9 = go.Figure()
    for region in ALL_REGIONS:
        counts = [df_temp[(df_temp["region"]==region)&(df_temp["year"]>=d)&(df_temp["year"]<d+10)&(df_temp["deviation"]>0)].shape[0] for d in decades]
        fig9.add_trace(go.Scatter(x=[f"{d}s" for d in decades], y=counts, name=region,
            mode="lines+markers", line=dict(color=REGION_COLORS[region], width=2.5), marker=dict(size=7)))
    fig9.update_layout(**plot_layout("Years above 21°C per decade — all time"),
                       height=300, xaxis_title="Decade", yaxis_title="Years above 21°C")
    st.plotly_chart(fig9, use_container_width=True)

    # Scatter: region deviation by year coloured by risk
    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:10px;padding:12px 18px;
                margin:16px 0 8px;border:0.5px solid rgba(111,93,79,0.15);">
      <p style="font-size:12px;color:{SAGE_DARK};margin:0;">
          <strong>Scatter:</strong> each dot is one region-year coloured by risk status.
          Clusters above zero show when and where heat stress concentrates.
      </p>
    </div>""", unsafe_allow_html=True)
    fig_sc3 = go.Figure()
    for status in status_order:
        sub = df_temp_f[df_temp_f["temp_status"]==status]
        fig_sc3.add_trace(go.Scatter(
            x=sub["year"], y=sub["deviation"], mode="markers", name=status.title(),
            marker=dict(color=TEMP_COLORS[status], size=7, opacity=0.65),
            hovertemplate=f"<b>{status}</b><br>Year: %{{x}}<br>Deviation: %{{y:+.1f}}°C<extra></extra>",
        ))
    fig_sc3.add_hline(y=0, line_dash="dot", line_color=SAGE_DARK, line_width=1)
    fig_sc3.update_layout(**plot_layout(f"Risk scatter — deviation by year · {year_range[0]}–{year_range[1]}"),
                          height=340, xaxis_title="Year", yaxis_title="Deviation from 21°C")
    st.plotly_chart(fig_sc3, use_container_width=True)

# ══ TAB 4: TEMP vs OUTPUT ════════════════════════════════════
with tab4:
    t4_corr  = df_merged_f["avg_temp"].corr(df_merged_f["production"]) if len(df_merged_f)>2 else np.nan
    t4_stress= df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"])]
    t4_normal= df_merged_f[df_merged_f["temp_status"].isin(["ideal","cool stress"])]
    t4_drop  = df_merged_f[df_merged_f["prod_change_%"]<0].shape[0]
    t4_both  = df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"]) & (df_merged_f["prod_change_%"]<0)].shape[0]
    t4_corr_str = f"{t4_corr:.3f}" if not np.isnan(t4_corr) else "insufficient data"
    t4_corr_label = ("negative — higher temps linked to lower output" if (not np.isnan(t4_corr) and t4_corr < -0.3)
                     else "positive — output grew despite rising temps" if (not np.isnan(t4_corr) and t4_corr > 0.3)
                     else "weak — temperature alone doesn't explain output changes" if not np.isnan(t4_corr)
                     else "select a wider year range for correlation analysis")
    t4_stress_avg = t4_stress["production"].mean()
    t4_normal_avg = t4_normal["production"].mean()

    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid #8B3A3A;
                border:0.5px solid rgba(139,58,58,0.2);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">What you are looking at · {year_range[0]}–{year_range[1]}</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li>Correlation between temperature and production: <strong>r = {t4_corr_str}</strong> — {t4_corr_label}</li>
        <li>Production dropped in <strong>{t4_drop}</strong> of {len(df_merged_f)} years in this range</li>
        <li><strong>{t4_both}</strong> drop years also had above-ideal temperatures</li>
        <li>Avg production in heat stress years: <strong>{t4_stress_avg:,.0f}</strong> vs <strong>{t4_normal_avg:,.0f}</strong> in normal years</li>
        <li>Bars: <span style="color:{BROWN};font-weight:500">brown</span> = within ideal · <span style="color:#B5714A;font-weight:500">orange</span> = heat stress · <span style="color:#8B3A3A;font-weight:500">red</span> = danger</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    fig10 = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = ["#8B3A3A" if s in ["at risk","danger"] else "#B5714A" if s=="heat stress" else BROWN for s in df_merged_f["temp_status"]]
    fig10.add_trace(go.Bar(x=df_merged_f["year"], y=df_merged_f["production"], name="Production",
        marker_color=bar_colors, opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Production: %{y:,.0f}<extra></extra>"), secondary_y=False)
    fig10.add_trace(go.Scatter(x=df_merged_f["year"], y=df_merged_f["avg_temp"], name="Avg temp (°C)",
        mode="lines+markers", line=dict(color=ROSE, width=2.5), marker=dict(size=5, color=ROSE),
        hovertemplate="<b>%{x}</b><br>Temp: %{y:.1f}°C<extra></extra>"), secondary_y=True)
    fig10.add_hrect(y0=18, y1=21, secondary_y=True, fillcolor="rgba(168,197,160,0.15)", line_width=0)
    fig10.add_hline(y=21, secondary_y=True, line_dash="dot", line_color=ROSE, line_width=1, opacity=0.6)
    fig10.update_layout(**plot_layout(f"Brazil production vs Minas Gerais temperature · {year_range[0]}–{year_range[1]}"),
                        height=420, xaxis_title="Year")
    fig10.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig10.update_yaxes(title_text="Production (1k × 60kg bags)", secondary_y=False, color=BROWN)
    fig10.update_yaxes(title_text="Temperature °C", secondary_y=True, color=ROSE)
    st.plotly_chart(fig10, use_container_width=True)

    if not np.isnan(t4_corr):
        corr_color = "#8B3A3A" if t4_corr < -0.3 else SAGE if t4_corr > 0.3 else SAGE_DARK
        st.markdown(f"""
        <div style="background:{WHITE};border-left:4px solid {corr_color};border-radius:0 12px 12px 0;
                    padding:20px 24px;margin-top:20px;box-shadow:2px 4px 12px rgba(61,46,36,0.07);">
          <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                     color:{SAGE_DARK};margin:0 0 6px;">Correlation insight</p>
          <p style="font-family:'Playfair Display';font-size:20px;color:{BROWN_DARK};margin:0 0 8px;">
              r = {t4_corr:.3f} — {("negative" if t4_corr < -0.3 else "positive" if t4_corr > 0.3 else "weak")} correlation</p>
          <p style="font-size:13px;color:#555;margin:0;line-height:1.6;">
              {"Higher temperatures are linked to lower production in this period." if t4_corr < -0.3
               else "Production grew despite rising temperatures — other factors dominate." if t4_corr > 0.3
               else "Temperature alone does not fully explain production changes."}</p>
        </div>
        """, unsafe_allow_html=True)

    # Scatter: temperature vs production
    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:10px;padding:12px 18px;
                margin:20px 0 8px;border:0.5px solid rgba(111,93,79,0.15);">
      <p style="font-size:12px;color:{SAGE_DARK};margin:0;">
          <strong>Scatter:</strong> each dot is one year. Shows directly whether hotter years
          produced more or less coffee. Dots coloured by risk status.
      </p>
    </div>""", unsafe_allow_html=True)
    fig_sc4 = go.Figure()
    for status in ["ideal","cool stress","heat stress","at risk","danger"]:
        sub = df_merged_f[df_merged_f["temp_status"]==status]
        fig_sc4.add_trace(go.Scatter(
            x=sub["avg_temp"], y=sub["production"], mode="markers", name=status.title(),
            marker=dict(color=TEMP_COLORS[status], size=9, opacity=0.8),
            text=sub["year"].astype(str),
            hovertemplate=f"<b>{status}</b><br>Year: %{{text}}<br>Temp: %{{x:.1f}}°C<br>Production: %{{y:,.0f}}<extra></extra>",
        ))
    fig_sc4.add_vline(x=21, line_dash="dot", line_color=SAGE_DARK, line_width=1,
                      annotation_text="21°C ceiling", annotation_font_color=SAGE_DARK)
    fig_sc4.update_layout(**plot_layout(f"Temperature vs production — each dot = one year · {year_range[0]}–{year_range[1]}"),
                          height=380, xaxis_title="Avg temperature °C (Minas Gerais)",
                          yaxis_title="Production (1k × 60kg bags)")
    st.plotly_chart(fig_sc4, use_container_width=True)

# ══ TAB 5: CONCLUSIONS ═══════════════════════════════════════
with tab5:
    c_above = df_temp_f[df_temp_f["avg_temp"]>21].shape[0]
    c_all   = max(df_temp_f.shape[0],1)

    # Safe warming trend — handle NaN and short ranges
    early_temps  = df_temp_f[df_temp_f["year"]<=year_range[0]+9]["avg_temp"].mean()
    recent_temps = df_temp_f[df_temp_f["year"]>=year_range[1]-9]["avg_temp"].mean()
    if np.isnan(early_temps) or np.isnan(recent_temps):
        c_trend     = None
        c_trend_str = "insufficient data for this range"
    elif early_temps == 0:
        c_trend     = 0
        c_trend_str = "0.0°C (no change)"
    else:
        c_trend     = recent_temps - early_temps
        c_trend_str = f"+{c_trend:.1f}°C" if c_trend > 0 else f"{c_trend:.1f}°C"

    c_corr = df_merged_f["avg_temp"].corr(df_merged_f["production"]) if len(df_merged_f)>2 else np.nan
    c_corr_str = f"{c_corr:.2f}" if not np.isnan(c_corr) else "—"
    c_drop = df_merged_f[df_merged_f["prod_change_%"]<0].shape[0]
    c_both = df_merged_f[df_merged_f["temp_status"].isin(["heat stress","at risk","danger"]) & (df_merged_f["prod_change_%"]<0)].shape[0]

    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:28px;border-left:4px solid {ROSE};
                border:0.5px solid rgba(223,147,157,0.3);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">Key findings · {year_range[0]}–{year_range[1]}</p>
      <ul style="font-size:13px;color:{BROWN_DARK};line-height:2;margin:0;padding-left:18px;">
        <li><strong>{c_above/c_all*100:.0f}%</strong> of region-years in this range sit above the 21°C ideal ceiling</li>
        <li>Warming from start to end of range: <strong>{c_trend_str}</strong></li>
        <li>Temperature vs production correlation: <strong>r = {c_corr_str}</strong></li>
        <li>Production dropped in <strong>{c_drop}</strong> years — <strong>{c_both}</strong> of those also had above-ideal temperatures</li>
        <li>Heat stress years are becoming more frequent in more recent decades</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:{WHITE};border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(61,46,36,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;
                     color:#8B3A3A;margin:0;">{c_above/c_all*100:.0f}%</p>
          <p style="font-size:12px;color:{SAGE_DARK};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">region-years above ideal</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:{WHITE};border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(61,46,36,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;
                     color:{BROWN};margin:0;">{c_trend_str}</p>
          <p style="font-size:12px;color:{SAGE_DARK};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">warming across range</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:{WHITE};border-radius:14px;padding:24px;text-align:center;
                    box-shadow:2px 4px 16px rgba(61,46,36,0.07);">
          <p style="font-family:'Playfair Display';font-size:38px;font-weight:900;
                     color:{ROSE};margin:0;">{c_corr_str}</p>
          <p style="font-size:12px;color:{SAGE_DARK};margin:6px 0 0;
                     letter-spacing:0.08em;text-transform:uppercase;">temp vs production r</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    trend_text = f"roughly {c_trend_str}" if c_trend is not None else "across the selected period"
    corr_text  = f"r = {c_corr_str}" if c_corr_str != "—" else "r = insufficient data"
    st.markdown(f"""
    <div style="max-width:740px;">
      <p style="font-family:'Playfair Display';font-size:22px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 14px;">What the data says</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 16px;">
          Brazil's coffee regions are warming. The rate is gradual —
          {trend_text} — but consistent, and accelerating in the most
          recent decades. Regions that were already warm, like Bahia and Rondônia,
          now spend almost no years within the ideal Arabica range.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 16px;">
          Production tells a more complicated story. Brazil has continued growing
          output despite rising temperatures — driven by technology, irrigation,
          and varietal adaptation. The correlation between temperature and
          production is {corr_text}, suggesting temperature is a factor
          but not the only one.</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 24px;">
          The real risk is not today's harvest. It is the compound effect of years
          outside the ideal window and the narrowing of suitable growing altitude.</p>
      <p style="font-family:'Playfair Display';font-size:22px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 14px;">Limitations</p>
      <p style="font-size:15px;line-height:1.9;color:{BROWN_DARK};margin:0 0 8px;">
          This analysis focuses on temperature only. A complete picture would also include
          rainfall, soil quality, pest pressure, altitude shifts, and economic factors.
          Production data from USDA PSD is a reliable aggregate but does not capture
          farm-level variation within regions.</p>
      <p style="font-size:13px;color:{SAGE_DARK};margin:24px 0 0;font-style:italic;">
          A mini project by <strong>Tulasi Arvind</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ══ TAB 6: SOURCES ════════════════════════════════════════════
with tab6:
    st.markdown(f"""
    <div style="background:{CREAM_DARK};border-radius:12px;padding:18px 24px;
                margin-bottom:24px;border-left:4px solid {SAGE};
                border:0.5px solid rgba(152,151,105,0.3);">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 10px;">About the data</p>
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
    <p style="font-size:14px;color:{SAGE_DARK};margin-bottom:32px;line-height:1.6;">
        All datasets and references used in this analysis.</p>
    <div class="source-card" style="border-left-color:{BROWN};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 8px;">01 — Brazil temperature data</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">
          New improved Brazilian daily weather gridded data (1961–2020)</p>
      <p style="font-size:13px;color:#666;margin:0 0 12px;line-height:1.7;">
          Xavier, A. C., Scanlon, B. R., King, C. W., &amp; Alves, A. I. (2022).
          <em>International Journal of Climatology</em>, 42(16), 8390–8404.</p>
      <a href="https://doi.org/10.1002/joc.7731" target="_blank">https://doi.org/10.1002/joc.7731</a>
    </div>
    <div class="source-card" style="border-left-color:{SAGE};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 8px;">02 — Coffee production data</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">
          USDA Foreign Agricultural Service — Production, Supply &amp; Distribution</p>
      <p style="font-size:13px;color:#666;margin:0 0 12px;line-height:1.7;">
          United States Department of Agriculture (USDA). PSD Online database.
          Commodity: Coffee, Green (0711100).</p>
      <a href="https://www.fas.usda.gov/data/production/0711100" target="_blank">
          https://www.fas.usda.gov/data/production/0711100</a>
    </div>
    <div class="source-card" style="border-left-color:{ROSE};">
      <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                 color:{SAGE_DARK};margin:0 0 8px;">03 — Arabica ideal temperature range</p>
      <p style="font-family:'Playfair Display';font-size:18px;font-weight:700;
                 color:{BROWN_DARK};margin:0 0 10px;">Climate &amp; Coffee — NOAA Climate.gov</p>
      <p style="font-size:13px;color:#666;margin:0 0 12px;line-height:1.7;">
          National Oceanic and Atmospheric Administration (NOAA).
          Climate conditions for coffee cultivation including the 18–21°C ideal range.</p>
      <a href="https://www.climate.gov/news-features/climate-and/climate-coffee" target="_blank">
          https://www.climate.gov/news-features/climate-and/climate-coffee</a>
    </div>
    <div style="background:{CREAM_DARK};border-radius:10px;padding:16px 20px;
                margin-top:8px;border:0.5px solid rgba(152,151,105,0.3);">
      <p style="font-size:12px;color:{SAGE_DARK};margin:0;line-height:1.7;">
          <strong>Note:</strong> Temperature analysis covers 1961–2024 using daily station data
          from 1,194 weather stations across Brazil. Production data covers Brazil, Vietnam,
          Colombia, Indonesia, and Ethiopia. Arabica ideal range 18–21°C used throughout.
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
