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
app.title = "Land Use Land Cover Dashboard"

# Read the CSV file
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Load the data
df = load_data()

# Columns for class IDs
area_columns = ['11', '21', '22', '23', '24', '31', '41', '42', '43', '52', '71', '81', '82', '90', '95']

# Map class IDs to descriptive names
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

# Convert the dataframe to long format for pie chart usage
df_long = df.melt(
    id_vars=['Region', 'Year'], 
    value_vars=area_columns, 
    var_name='Class', 
    value_name='Area'
)

# Replace class IDs with descriptive names for better visualization
df_long['Class'] = df_long['Class'].map(class_mapping)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Land Use Land Cover Dashboard", style={'textAlign': 'center'}),
    
    # Dropdowns for region and year selection
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            value=df['Region'].unique()[0],
            clearable=False
        ),
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in df['Year'].unique()],
            value=df['Year'].unique()[0],
            clearable=False
        )
    ], style={'width': '40%', 'margin': 'auto'}),
    
    # Graphs for pie chart and trend graph
    html.Div([
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='trend-graph')
    ])
])

# Callback to update graphs based on selected region and year
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('trend-graph', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graphs(selected_region, selected_year):
    # Filter data for the selected region and year
    filtered_data = df_long[(df_long['Region'] == selected_region) & (df_long['Year'] == selected_year)]
    
    # Pie chart for land use distribution
    pie_chart = px.pie(
        filtered_data,
        names='Class',
        values='Area',
        title=f"Land Use Distribution in {selected_region} ({selected_year})",
        labels={'Class': 'Land Class', 'Area': 'Area (sq. units)'}
    )
    
    # Filter data for trend graph (all years for the selected region)
    trend_data = df[df['Region'] == selected_region].sort_values(by='Year')
    trend_data_long = trend_data.melt(
        id_vars=['Region', 'Year'],
        value_vars=area_columns,
        var_name='Class',
        value_name='Area'
    )
    trend_data_long['Class'] = trend_data_long['Class'].map(class_mapping)
    
    # Line graph for trend over time
    trend_graph = px.line(
        trend_data_long,
        x='Year',
        y='Area',
        color='Class',
        title=f"Land Use Trend Over Time in {selected_region}",
        labels={'Year': 'Year', 'Area': 'Area (sq. units)', 'Class': 'Land Class'}
    )
    
    return pie_chart, trend_graph

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
