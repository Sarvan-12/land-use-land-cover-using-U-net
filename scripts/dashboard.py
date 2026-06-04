import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "analysis_results", "area_analysis1.csv")

# User-configurable region display names mapping
REGION_DISPLAY_NAMES = {
    'region_1': 'REGION 1',
    'region_2': 'REGION 2',
    'region_3': 'REGION 3'
}

# Create a Dash app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "LULC Classification Dashboard"
server = app.server

# Read the CSV file
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Load the data
df = load_data()

# Class columns and their mappings
area_columns = ['11', '21', '22', '23', '24', '31', '41', '42', '43', '52', '71', '81', '82', '90', '95']
class_mapping = {
    '11': 'Water',
    '21': 'Developed, Open Space',
    '22': 'Developed, Low Intensity',
    '23': 'Developed, Medium Intensity',
    '24': 'Developed, High Intensity',
    '31': 'Barren Land',
    '41': 'Deciduous Forest',
    '42': 'Evergreen Forest',
    '43': 'Mixed Forest',
    '52': 'Shrub/Scrub',
    '71': 'Grassland',
    '81': 'Pasture/Hay',
    '82': 'Cultivated Crops',
    '90': 'Woody Wetlands',
    '95': 'Emergent Herbaceous Wetlands',
}

# Reshape for visualizations
df_long = df.melt(
    id_vars=['Region', 'Year'], 
    value_vars=area_columns, 
    var_name='Class', 
    value_name='Area'
)
df_long['Class'] = df_long['Class'].map(class_mapping)

# Brutalist palette color mapping for all classes
brutalist_color_map = {
    'Water': '#00C2FF',                       # Cyan
    'Developed, Open Space': '#FFA4A4',        # Light Red
    'Developed, Low Intensity': '#FF7E7E',     # Medium-Light Red
    'Developed, Medium Intensity': '#FF4D4D',  # Bold Red
    'Developed, High Intensity': '#D01C1C',    # Dark Red
    'Barren Land': '#FFDD00',                 # Yellow
    'Deciduous Forest': '#2E7D32',             # Dark Green
    'Evergreen Forest': '#1B5E20',             # Deep Forest Green
    'Mixed Forest': '#4CAF50',                 # Mid Green
    'Shrub/Scrub': '#81C784',                  # Light Green
    'Grassland': '#C8E6C9',                    # Pale Green
    'Pasture/Hay': '#FFF176',                  # Light Yellow
    'Cultivated Crops': '#FBC02D',              # Crop Gold
    'Woody Wetlands': '#B388FF',               # Purple/Lavender
    'Emergent Herbaceous Wetlands': '#7C4DFF', # Deep Purple
}

# Setup years for Slider
years = sorted(df['Year'].unique())
min_year = min(years)
max_year = max(years)
# Only two endpoint marks — no intermediate dots/ticks at all
year_marks = {
    int(min_year): {'label': str(min_year)},
    int(max_year): {'label': str(max_year)}
}

# Layout
app.layout = html.Div(id='main-container', className='main-container', children=[
    # Newspaper Header
    html.Div([
        html.Div([
            html.H1("LAND USE LAND COVER", style={'margin': '0'}),
            html.Div("SATELLITE IMAGE ANALYSIS & CHANGE MONITORING (1994 - 2023)", className="dashboard-subtitle")
        ], style={'flex': '1', 'minWidth': '300px'}),
        html.Div([
            html.Label("THEME MODE:", className="theme-label", style={'marginRight': '10px', 'fontWeight': '700'}),
            dcc.RadioItems(
                id='theme-toggle',
                options=[
                    {'label': 'LIGHT', 'value': 'light'},
                    {'label': 'DARK', 'value': 'dark'}
                ],
                value='light',
                inline=True,
                className="theme-radio"
            )
        ], className="theme-selector-box")
    ], className="dashboard-header", style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '15px'}),

    # Main Dashboard Area: Controls (left) | U-Net Map (middle) | Stats (right)
    html.Div([
        # Left: Controls
        html.Div([
            html.Div([
                html.Div("Controls", className="brutalist-card-header yellow-header"),
                html.Div([
                    html.Div([
                        html.Label("SELECT REGION"),
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[{'label': REGION_DISPLAY_NAMES.get(region, region.upper()), 'value': region} for region in df['Region'].unique()],
                            value=df['Region'].unique()[0],
                            clearable=False,
                            className="dash-dropdown"
                        )
                    ], className="control-group"),
                    
                    html.Div([
                        html.Label("SELECT YEAR"),
                        html.Div(
                            id='year-display',
                            style={
                                'fontFamily': "'IBM Plex Mono', monospace",
                                'fontSize': '42px',
                                'fontWeight': '700',
                                'textAlign': 'center',
                                'border': '3px solid #000',
                                'boxShadow': '4px 4px 0px #000',
                                'background': '#FFDD00',
                                'padding': '10px 0',
                                'marginBottom': '18px',
                                'letterSpacing': '2px',
                            }
                        ),
                        html.Div([
                            dcc.Slider(
                                id='year-slider',
                                min=min_year,
                                max=max_year,
                                step=1,
                                marks=year_marks,
                                value=min_year,
                                tooltip={'always_visible': True, 'placement': 'top'}
                            )
                        ], className="slider-container")
                    ], className="control-group"),
                    
                    html.Button("EXPORT DATA (CSV)", id="btn-export-csv", className="brutalist-button", style={'width': '100%', 'marginTop': '10px'}),
                    dcc.Download(id="download-dataframe-csv")
                ], className="brutalist-card-content")
            ], className="brutalist-card")
        ]),

        # Middle: U-Net Map Card
        html.Div([
            html.Div([
                html.Div("LAND COVER MAP", className="brutalist-card-header cyan-header"),
                html.Div([
                    html.Img(id='classified-map-img', className="comparison-image")
                ], className="brutalist-card-content", style={'textAlign': 'center', 'padding': '15px'})
            ], className="brutalist-card")
        ]),

        # Right: Stats only
        html.Div([
            html.Div([
                # Desktop header — always visible
                html.H3("LAND TYPE AREA STATISTICS",
                        className='stats-desktop-header'),
                # Mobile toggle button — hidden on desktop via CSS
                html.Button(
                    "LAND TYPE AREA STATISTICS \u25bc",
                    id='stats-toggle-btn',
                    className='stats-toggle-btn',
                    n_clicks=0
                ),
                html.Div(id='stats-grid', className='stats-grid stats-grid-hidden')
            ], className="stats-container"),
        ])
    ], className="main-grid"),

    # KPI Highlights Row
    html.Div(id='kpi-row', className="kpi-row"),

    # Full-width Charts Row — spans both columns
    html.Div([
        # Pie Chart Card
        html.Div([
            html.Div("Distribution Breakdown", className="brutalist-card-header cyan-header"),
            html.Div(dcc.Graph(id='pie-chart', style={'height': '480px'}), className="brutalist-card-content", style={'padding': '0'})
        ], className="brutalist-card graph-box"),

        # Trend Card
        html.Div([
            html.Div("Temporal Change Trends", className="brutalist-card-header"),
            html.Div([
                dcc.Graph(id='trend-graph', className="trend-graph"),
            ], className="brutalist-card-content", style={'padding': '0'})
        ], className="brutalist-card graph-box")
    ], className="graphs-row"),

    # Full-width Shared Legend Card below the charts
    html.Div([
        html.Div("Class Legend", className="brutalist-card-header yellow-header"),
        html.Div(id='trend-legend-container', className="custom-legend-card-grid")
    ], className="brutalist-card", style={'marginTop': '30px', 'marginBottom': '30px'})
])

# Callbacks
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('trend-graph', 'figure'),
     Output('stats-grid', 'children'),
     Output('year-display', 'children'),
     Output('trend-legend-container', 'children'),
     Output('classified-map-img', 'src'),
     Output('kpi-row', 'children')],
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('theme-toggle', 'value')]
)
def update_dashboard(selected_region, selected_year, theme):
    # Snap slider integer to nearest valid year in the dataset
    selected_year = min(years, key=lambda y: abs(y - selected_year))
    # Filter current snapshot
    filtered_data = df_long[(df_long['Region'] == selected_region) & (df_long['Year'] == selected_year)]

    is_dark = theme == 'dark'
    bg_color = '#1A1A1A' if is_dark else '#FFFFFF'
    text_color = '#FFFFFF' if is_dark else '#000000'
    grid_color = '#333333' if is_dark else '#EAEAEA'

    # Generate Stats Cells
    stats_cells = []
    # Sort from largest area to smallest
    sorted_stats = filtered_data.sort_values(by='Area', ascending=False)
    for idx, row in sorted_stats.iterrows():
        # format large numbers nicely
        area_val = f"{row['Area']:,}"
        stats_cells.append(
            html.Div([
                html.Div(row['Class'].upper(), className="stat-cell-title"),
                html.Div(area_val, className="stat-cell-value")
            ], className="stat-cell")
        )

    # Pie Chart
    pie_chart = px.pie(
        filtered_data,
        names='Class',
        values='Area',
        title=f"DISTRIBUTION IN {REGION_DISPLAY_NAMES.get(selected_region, selected_region).upper()} ({selected_year})",
        color='Class',
        color_discrete_map=brutalist_color_map
    )
    pie_chart.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(t=50, b=20, l=10, r=10),
        font=dict(family="Space Grotesk, sans-serif", size=12, color=text_color),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=16, color=text_color)),
        showlegend=False
    )
    pie_chart.update_traces(
        marker=dict(line=dict(color='#000000', width=2)),
        textinfo='percent',
        textposition='inside'
    )

    # Line Chart
    trend_data = df[df['Region'] == selected_region].sort_values(by='Year')
    trend_data_long = trend_data.melt(
        id_vars=['Region', 'Year'],
        value_vars=area_columns,
        var_name='Class',
        value_name='Area'
    )
    trend_data_long['Class'] = trend_data_long['Class'].map(class_mapping)

    trend_graph = px.line(
        trend_data_long,
        x='Year',
        y='Area',
        color='Class',
        title=f"LAND USE TRENDS OVER TIME IN {REGION_DISPLAY_NAMES.get(selected_region, selected_region).upper()}",
        color_discrete_map=brutalist_color_map
    )

    trend_graph.update_layout(
        showlegend=False,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(t=50, b=40, l=20, r=20),
        font=dict(family="Space Grotesk, sans-serif", size=12, color=text_color),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=16, color=text_color)),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor=text_color,
            linewidth=2,
            ticks='outside',
            tickfont=dict(family="IBM Plex Mono, monospace", size=10, color=text_color),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=12, color=text_color))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor=text_color,
            linewidth=2,
            ticks='outside',
            tickfont=dict(family="IBM Plex Mono, monospace", size=10, color=text_color),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=12, color=text_color))
        )
    )
    trend_graph.update_traces(
        line=dict(width=3)
    )

    # Custom HTML Legend Items
    legend_items = []
    for label, color in brutalist_color_map.items():
        legend_items.append(
            html.Div([
                html.Div(style={
                    'width': '14px',
                    'height': '14px',
                    'backgroundColor': color,
                    'border': '2px solid #000000',
                    'marginRight': '10px',
                    'flexShrink': '0'
                }),
                html.Span(label, className="legend-item-text")
            ], style={'display': 'flex', 'alignItems': 'center'})
        )

    # Determine dynamic image source asset URL for the classified map
    classified_img_src = app.get_asset_url(f"images/classified/{selected_region}_{selected_region}_{selected_year}.png")

    # Calculate KPI values
    water_row = filtered_data[filtered_data['Class'] == 'Water']
    water_area = water_row['Area'].sum() if not water_row.empty else 0

    dev_classes = ['Developed, Open Space', 'Developed, Low Intensity', 'Developed, Medium Intensity', 'Developed, High Intensity']
    dev_area = filtered_data[filtered_data['Class'].isin(dev_classes)]['Area'].sum()

    forest_classes = ['Deciduous Forest', 'Evergreen Forest', 'Mixed Forest']
    forest_area = filtered_data[filtered_data['Class'].isin(forest_classes)]['Area'].sum()

    dominant_row = filtered_data.loc[filtered_data['Area'].idxmax()] if not filtered_data.empty else None
    dominant_class = dominant_row['Class'] if dominant_row is not None else "N/A"
    dominant_area = dominant_row['Area'] if dominant_row is not None else 0

    kpi_cards = [
        html.Div([
            html.Div("TOTAL WATER COVER", className="kpi-card-title"),
            html.Div(f"{water_area:,} sq m", className="kpi-card-value")
        ], className="kpi-card cyan-kpi"),
        html.Div([
            html.Div("TOTAL DEVELOPED AREA", className="kpi-card-title"),
            html.Div(f"{dev_area:,} sq m", className="kpi-card-value")
        ], className="kpi-card red-kpi"),
        html.Div([
            html.Div("TOTAL FOREST COVER", className="kpi-card-title"),
            html.Div(f"{forest_area:,} sq m", className="kpi-card-value")
        ], className="kpi-card green-kpi"),
        html.Div([
            html.Div(f"DOMINANT: {dominant_class.upper()}", className="kpi-card-title"),
            html.Div(f"{dominant_area:,} sq m", className="kpi-card-value")
        ], className="kpi-card yellow-kpi")
    ]

    return pie_chart, trend_graph, stats_cells, str(selected_year), legend_items, classified_img_src, kpi_cards

# Clientside callback — toggles stats grid visibility on mobile button click
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks === undefined || n_clicks === null) {
            return ["LAND TYPE AREA STATISTICS \u25bc", "stats-grid stats-grid-hidden"];
        }
        var isOpen = n_clicks % 2 === 1;
        var btnText  = isOpen
            ? "LAND TYPE AREA STATISTICS \u25b2"
            : "LAND TYPE AREA STATISTICS \u25bc";
        var gridClass = isOpen ? "stats-grid" : "stats-grid stats-grid-hidden";
        return [btnText, gridClass];
    }
    """,
    [Output('stats-toggle-btn', 'children'),
     Output('stats-grid', 'className')],
    Input('stats-toggle-btn', 'n_clicks')
)

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-export-csv", "n_clicks"),
    [State('region-dropdown', 'value'),
     State('year-slider', 'value')],
    prevent_initial_call=True
)
def export_csv(n_clicks, selected_region, selected_year):
    selected_year = min(years, key=lambda y: abs(y - selected_year))
    filtered = df[(df['Region'] == selected_region) & (df['Year'] == selected_year)]
    return dcc.send_data_frame(filtered.to_csv, f"LULC_{selected_region}_{selected_year}.csv", index=False)

app.clientside_callback(
    """
    function(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            return 'main-container dark-mode';
        } else {
            document.body.classList.remove('dark-mode');
            return 'main-container';
        }
    }
    """,
    Output('main-container', 'className'),
    Input('theme-toggle', 'value')
)

def create_dashboard():
    """Wrapper function to run the Dash dashboard server."""
    app.run(debug=False)

# Run server
if __name__ == "__main__":
    create_dashboard()
