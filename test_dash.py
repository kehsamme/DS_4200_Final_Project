import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Assuming 'asthma_df' is your pandas DataFrame
asthma_pop_df = pd.read_csv('clean_population_data.csv')


# Function to generate the initial Plotly figure
def generate_fig(demographic):
    fig = px.choropleth(
        asthma_pop_df,
        locations='State Code',  # State Code as locations
        color=demographic,  # Color scale on population
        locationmode='USA-states',  # Set location mode to US
        scope='usa',  # Set scope to US
        hover_name='States',  # Hover show state names
        height=600,
        color_continuous_scale='Purples',  # Use selected color scale
        title='Asthma Prevalence in the United States'
    )
    return fig


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the color options for the dropdown
populations = ['Population', 'Adult Number', 'Child Number']

# Define the layout of the app with dropdown and graph
app.layout = html.Div([
    html.H1("Asthma Prevalence Dashboard"),
    dcc.Dropdown(
        id='color-dropdown',
        options=populations,
        value='Population',  # Default color scale
        style={'width': '200px'}
    ),
    dcc.Graph(id='my-choropleth-graph'),  # Adding an ID to the graph
])


# Define a callback to update the graph when the dropdown value changes
@app.callback(
    Output('my-choropleth-graph', 'figure'),
    [Input('color-dropdown', 'value')]
)
def update_graph(demographic):
    # Generate the figure with the selected color scale
    updated_fig = generate_fig(demographic)
    return updated_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)