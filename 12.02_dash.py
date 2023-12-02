import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# UPDATED
# Load clean data
asthma_pop_df = pd.read_csv('clean_population_data.csv')
coverage_df = pd.read_csv('coverage_df_clean.csv')
df = pd.read_csv('Asthma RPM State Coverage.csv')

# merger asthma population and insurance coverage data
combined_df = asthma_pop_df.merge(coverage_df, left_on='States', right_on='State')


# Generate asthma population choropleth graph
def generate_fig(demographic):
    fig = px.choropleth(
        asthma_pop_df,
        locations='State Code',  # State Code as locations
        color=demographic,  # Color scale on population
        locationmode='USA-states',  # Set location mode to US
        scope='usa',  # Set scope to US
        hover_name='States',  # Hover show state names
        height=600,
        color_continuous_scale='Blues',  # Use selected color scale
        # title='Asthma Prevalence in the United States',
    )

    fig.update_coloraxes(colorbar=dict(title='Population Count'))

    return fig


# Initialize the Dash app
app = dash.Dash(__name__,external_stylesheets=[
    {
        'href': 'https://fonts.googleapis.com/css?family=Montserrat',  # Link to custom font
        'rel': 'stylesheet'
    },
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',  # Bootstrap CSS
        'rel': 'stylesheet'
    }
])

# Define content for Tab 1
tab1_layout = html.Div([
    html.H1("Asthma Dashboard", style={'fontFamily': 'Montserrat', 'fontSize': '36px', 'marginLeft': '20px'}),
    html.H2("Asthma Prevalence and RPM Insurance Coverage",  style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),
    dcc.Checklist(
        id='checkboxes',
        options=[
            {'label': 'Medicare', 'value': '99454 Coverage: Medicare'},
            {'label': 'Medicaid', 'value': '99454 Coverage: Medicaid'},
            {'label': 'Top Private Insurance', 'value': '99454 Coverage: Top Private Insurance'},
            {'label': 'Second Private Insurance', 'value': '99454 Coverage: Second Private Insurance'},
        ],
        value=['99454 Coverage: Medicare',
               '99454 Coverage: Medicaid',
               '99454 Coverage: Top Private Insurance',
               '99454 Coverage: Second Private Insurance'
        ],
        style={'width': '150px', 'fontFamily': 'Montserrat', 'marginLeft': '40px'},
        inline=True,
    ),
    dcc.Graph(
        id='choropleth-map', style={'width': '100vw', 'height': '100vh'}
    ),
])

# Define content for Tab 2
tab2_layout = html.Div([
    html.H1("Asthma Population by State", style={'fontFamily': 'Montserrat', 'fontSize': '36px', 'marginLeft': '20px'}),
    # html.H2("Asthma Population by State",
    # style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),
    html.Div([
        dcc.Dropdown(
            id='top-n-dropdown',
            options=[
                {'label': f'Top {i} States', 'value': i} for i in range(5, df.shape[0] + 1, 5)
            ],
            value=5,
            multi=False,
            style={'width': '50%', 'marginLeft': '40px', 'fontFamily': 'Montserrat'}
        ),
    ], style={'marginTop': '40px'}),
    html.Div([
        dcc.Graph(id='stacked-bar-chart', style={'marginTop': '100px', 'width': '100vw', 'marginLeft': '20px'})
    ], style={'marginLeft': '20px'})
])

# # Define the layout of the app with dropdown and graph
# app.layout = html.Div([
#     html.H1("Asthma Dashboard", style={'fontFamily': 'Montserrat', 'fontSize': '36px', 'marginLeft': '20px'}),
#     html.H2("Asthma Prevalence and RPM Insurance Coverage",  style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),
#     dcc.Checklist(
#         id='checkboxes',
#         options=[
#             {'label': 'Medicare', 'value': '99454 Coverage: Medicare'},
#             {'label': 'Medicaid', 'value': '99454 Coverage: Medicaid'},
#             {'label': 'Top Private Insurance', 'value': '99454 Coverage: Top Private Insurance'},
#             {'label': 'Second Private Insurance', 'value': '99454 Coverage: Second Private Insurance'},
#         ],
#         value=['99454 Coverage: Medicare',
#                '99454 Coverage: Medicaid',
#                '99454 Coverage: Top Private Insurance',
#                '99454 Coverage: Second Private Insurance'
#         ],
#         style={'width': '150px', 'fontFamily': 'Montserrat', 'marginLeft': '40px'},
#         inline=True,
#     ),
#     dcc.Graph(
#         id='choropleth-map', style={'width': '100vw', 'height': '100vh'}
#     ),
#     html.H2("Asthma Population by State", style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),
#     html.Div([
#         dcc.Dropdown(
#             id='top-n-dropdown',
#             options=[
#                 {'label': f'Top {i} States', 'value': i} for i in range(5, df.shape[0] + 1, 5)
#             ],
#             value=5,
#             multi=False,
#             style={'width': '50%', 'marginLeft': '40px', 'fontFamily': 'Montserrat'}
#         ),
#     ], style={'marginTop': '40px'}),
#     html.Div([
#         dcc.Graph(id='stacked-bar-chart', style={'marginTop': '100px', 'width': '100vw', 'marginLeft': '20px'})
#     ], style={'marginLeft': '20px'})
# ])


# UPDATED !!!
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('checkboxes', 'value')]
)
def update_choropleth(selected_checkboxes):
    filtered_df = combined_df[combined_df[selected_checkboxes].sum(axis=1) == len(selected_checkboxes)]

    # Create choropleth map
    fig = px.choropleth(
        filtered_df,
        locations='State Code_x',
        locationmode="USA-states",
        color='Population',
        hover_name='State',
        scope="usa",
        # title='Remote Patient Monitoring Coverage, CPT: 99454',
        labels={'Sum': 'Selected Columns Sum'},
        color_continuous_scale='Blues',
        )

    return fig


# Melt the DataFrame to have 'State' as a column and 'Adult' and 'Child' as values
melted_df = pd.melt(df, id_vars=['US States'],
                    value_vars=['Adult Asthma Population Number', 'Child Asthma \nPopulation Number'],
                    var_name='Age Group', value_name='Population')

# Remove commas and convert 'Population' to numeric for correct counting
melted_df['Population'] = pd.to_numeric(melted_df['Population'].str.replace(',', ''), errors='coerce')


# Define callback to update the chart based on the selected top-n value
@app.callback(
    dash.dependencies.Output('stacked-bar-chart', 'figure'),
    [dash.dependencies.Input('top-n-dropdown', 'value')]
)
def update_chart(top_n):
    sorted_df = df.copy()
    sorted_df['Total Asthma Population'] = sorted_df['Total Asthma Population'].str.replace(',', '').astype(int)
    sorted_df = sorted_df.sort_values(by='Total Asthma Population', ascending=False).head(top_n)

    melted_sorted_df = pd.melt(sorted_df, id_vars=['US States'],
                                value_vars=['Adult Asthma Population Number', 'Child Asthma \nPopulation Number'],
                                var_name='Age Group', value_name='Population')

    melted_sorted_df['Population'] = pd.to_numeric(melted_sorted_df['Population'].str.replace(',', ''),
                                                    errors='coerce')

    fig = px.bar(
        melted_sorted_df,
        x='US States',
        y='Population',
        color='Age Group',
        # title=f'Top {top_n} States - Asthma Population by Age Group',
        labels={'Population': 'Population'},
        color_discrete_map={'Adult Asthma Population Number': 'blue', 'Child Asthma Population Number': 'purple'},
        barmode='stack'
    )

    # Adjust the figure height and rotate x-axis labels
    fig.update_layout(height=600, width=1200, xaxis_tickangle=-45)

    return fig


# Create app layout with tabs
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Asthma Population and Insurance', value='tab-1'),
        dcc.Tab(label='Asthma Population Demographic by State', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])


# Define callback to update tab content
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1_layout
    elif tab == 'tab-2':
        return tab2_layout


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)