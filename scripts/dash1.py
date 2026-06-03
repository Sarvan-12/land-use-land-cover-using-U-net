import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Path to the CSV file
CSV_PATH = "data/analysis_results/area_analysis1.csv"

# Create a Dash app
app = dash.Dash(__name__)
app.title = "LULC Classification Dashboard"

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
app.layout = html.Div([
    # Hidden input to track viewport width
    dcc.Input(id='viewport-width-input', type='number', value=1200, style={'display': 'none'}),

    # Newspaper Header
    html.Div([
        html.H1("LAND USE LAND COVER"),
        html.Div("SATELLITE IMAGE ANALYSIS & CHANGE MONITORING (1994 - 2023)", className="dashboard-subtitle")
    ], className="dashboard-header"),

    # Main Dashboard Area: Controls (left) | Stats (right)
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
                            options=[{'label': region.upper(), 'value': region} for region in df['Region'].unique()],
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
                    ], className="control-group")
                ], className="brutalist-card-content")
            ], className="brutalist-card")
        ]),

        # Right: Stats only
        html.Div([
            html.Div([
                html.H3("LAND TYPE AREA STATISTICS", style={'marginBottom': '15px', 'letterSpacing': '0.5px'}),
                html.Div(id='stats-grid', className='stats-grid')
            ], className="stats-container"),
        ])
    ], className="main-grid"),

    # Full-width Charts Row — spans both columns
    html.Div([
        # Pie Chart Card
        html.Div([
            html.Div("Distribution Breakdown", className="brutalist-card-header cyan-header"),
            html.Div(dcc.Graph(id='pie-chart', className="pie-graph"), className="brutalist-card-content", style={'padding': '0'})
        ], className="brutalist-card graph-box"),

        # Trend Card
        html.Div([
            html.Div("Temporal Change Trends", className="brutalist-card-header"),
            html.Div(dcc.Graph(id='trend-graph', className="trend-graph"), className="brutalist-card-content", style={'padding': '0'})
        ], className="brutalist-card graph-box")
    ], className="graphs-row")
])

# Callbacks
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('trend-graph', 'figure'),
     Output('stats-grid', 'children'),
     Output('year-display', 'children')],
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('viewport-width-input', 'value')]
)
def update_dashboard(selected_region, selected_year, viewport_width):
    # Snap slider integer to nearest valid year in the dataset
    selected_year = min(years, key=lambda y: abs(y - selected_year))
    # Filter current snapshot
    filtered_data = df_long[(df_long['Region'] == selected_region) & (df_long['Year'] == selected_year)]

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

    # Check if we are rendering for a mobile device screen (<= 768px)
    is_mobile = viewport_width is not None and int(viewport_width) <= 768

    # Pie Chart
    pie_chart = px.pie(
        filtered_data,
        names='Class',
        values='Area',
        title=f"DISTRIBUTION IN {selected_region.upper()} ({selected_year})",
        color='Class',
        color_discrete_map=brutalist_color_map
    )

    if is_mobile:
        pie_margin = dict(t=50, b=220, l=10, r=10)
        pie_legend = dict(
            orientation='h',
            yanchor='top',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(family="IBM Plex Mono, monospace", size=8, color="#000000"),
            bgcolor='#FFFFFF',
            bordercolor='#000000',
            borderwidth=2
        )
    else:
        pie_margin = dict(t=50, b=120, l=10, r=10)
        pie_legend = dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(family="Space Grotesk, sans-serif", size=10, color="#000000"),
            bgcolor='#FFFFFF',
            bordercolor='#000000',
            borderwidth=2
        )

    pie_chart.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        margin=pie_margin,
        font=dict(family="Space Grotesk, sans-serif", size=12, color="#000000"),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=16, color="#000000")),
        legend=pie_legend
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
        title=f"LAND USE TRENDS OVER TIME IN {selected_region.upper()}",
        color_discrete_map=brutalist_color_map
    )

    if is_mobile:
        trend_margin = dict(t=50, b=240, l=20, r=20)
        trend_legend = dict(
            orientation='h',
            yanchor='top',
            y=-0.28,
            xanchor='center',
            x=0.5,
            font=dict(family="IBM Plex Mono, monospace", size=8, color="#000000"),
            bgcolor='#FFFFFF',
            bordercolor='#000000',
            borderwidth=2
        )
    else:
        trend_margin = dict(t=50, b=20, l=20, r=20)
        trend_legend = dict(
            font=dict(family="IBM Plex Mono, monospace", size=10, color="#000000"),
            bgcolor='#FFFFFF',
            bordercolor='#000000',
            borderwidth=2
        )

    trend_graph.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        margin=trend_margin,
        font=dict(family="Space Grotesk, sans-serif", size=12, color="#000000"),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=16, color="#000000")),
        legend=trend_legend,
        xaxis=dict(
            showgrid=True,
            gridcolor='#EAEAEA',
            linecolor='#000000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family="IBM Plex Mono, monospace", size=10),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=12, color="#000000"))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#EAEAEA',
            linecolor='#000000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family="IBM Plex Mono, monospace", size=10),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=12, color="#000000"))
        )
    )
    trend_graph.update_traces(
        line=dict(width=3)
    )

    return pie_chart, trend_graph, stats_cells, str(selected_year)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
