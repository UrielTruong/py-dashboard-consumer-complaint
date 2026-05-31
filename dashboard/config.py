from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "complaints.duckdb"

PALETTE = {
    "accent":  "#929DFF",  # main purple
    "accent2": "#FF7E67",  # main orange-red
    "accent3": "#A6C1FF",  # support blue
    "pos":     "#47D1A0",  # positive green
    "neg":     "#FF6B6B",  # negative red
    "warn":    "#FFD93D",  # warning yellow
    "bg":      "#F8F9FE",  # main background
    "bg2":     "#FFFFFF",  # card background
    "bg3":     "#EEF2FF",  # sidebar background
    "ink":     "#1E293B",  # bold text
    "muted":   "#64748B",  # support text
    "border":  "#E2E8F0",  # borders
}

DONUT_COLORS = [
    "#929DFF",  # Lavender
    "#A1C4FD",  # Soft Blue
    "#94E7E4",  # Turquoise
    "#C1F1D5",  # Mint Green
    "#D6BBFB",  # Light Purple
    "#85C1E9",  # Sky Blue
    "#B2EBF2",  # Cyan Light
]

US_STATES = {
    "AL": "Alabama",        "AK": "Alaska",         "AZ": "Arizona",
    "AR": "Arkansas",       "CA": "California",     "CO": "Colorado",
    "CT": "Connecticut",    "DE": "Delaware",       "FL": "Florida",
    "GA": "Georgia",        "HI": "Hawaii",         "ID": "Idaho",
    "IL": "Illinois",       "IN": "Indiana",        "IA": "Iowa",
    "KS": "Kansas",         "KY": "Kentucky",       "LA": "Louisiana",
    "ME": "Maine",          "MD": "Maryland",       "MA": "Massachusetts",
    "MI": "Michigan",       "MN": "Minnesota",      "MS": "Mississippi",
    "MO": "Missouri",       "MT": "Montana",        "NE": "Nebraska",
    "NV": "Nevada",         "NH": "New Hampshire",  "NJ": "New Jersey",
    "NM": "New Mexico",     "NY": "New York",       "NC": "North Carolina",
    "ND": "North Dakota",   "OH": "Ohio",           "OK": "Oklahoma",
    "OR": "Oregon",         "PA": "Pennsylvania",   "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota",   "TN": "Tennessee",
    "TX": "Texas",          "UT": "Utah",           "VT": "Vermont",
    "VA": "Virginia",       "WA": "Washington",     "WV": "West Virginia",
    "WI": "Wisconsin",      "WY": "Wyoming",
    "DC": "District of Columbia", "PR": "Puerto Rico",
}

CUSTOM_CSS = """
<style>
/* ── KPI cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 22px 20px;
    height: 100%;
}
.kpi-label {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 34px;
    line-height: 1;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 4px;
}
.kpi-value.accent { color: #929DFF; }
.kpi-value.warn   { color: #FF7E67; }
.kpi-sub   { font-size: 12px; color: #64748B; }
.kpi-trend { font-size: 11px; margin-top: 4px; }
.kpi-trend.up   { color: #FF6B6B; }
.kpi-trend.down { color: #47D1A0; }

/* ── Section labels ── */
.card-eyebrow {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 4px;
}
.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #1E293B;
    margin: 0 0 14px;
}

/* ── Insight cards ── */
.insight {
    border-left: 3px solid #929DFF;
    padding: 12px 16px;
    background: linear-gradient(to right, rgba(146,157,255,0.08), transparent 60%);
    border-radius: 0 6px 6px 0;
    margin-bottom: 10px;
}
.insight.warn { border-left-color: #FF7E67; background: linear-gradient(to right, rgba(255,126,103,0.08), transparent 60%); }
.insight.pos  { border-left-color: #47D1A0; background: linear-gradient(to right, rgba(71,209,160,0.08), transparent 60%); }
.insight.time { border-left-color: #A6C1FF; }
.insight.resp { border-left-color: #FFD93D; }
.insight .ins-tag { font-size: 10px; text-transform: uppercase; color: #64748B; margin-bottom: 4px; }
.insight h4 { font-size: 15px; font-weight: 600; margin: 0 0 6px; color: #1E293B; }
.insight p  { margin: 0; font-size: 13px; color: #64748B; line-height: 1.5; }

hr { border: 0; border-top: 1px solid #E2E8F0; margin: 12px 0 18px; }

/* ── Plotly chart SVG text (fill, not color) ── */
[data-testid="stPlotlyChart"] text,
[data-testid="stPlotlyChart"] .xtick text,
[data-testid="stPlotlyChart"] .ytick text,
[data-testid="stPlotlyChart"] .gtitle,
[data-testid="stPlotlyChart"] .legendtext,
[data-testid="stPlotlyChart"] .g-xtitle text,
[data-testid="stPlotlyChart"] .g-ytitle text {
    fill: #64748B !important;
}
</style>
"""
