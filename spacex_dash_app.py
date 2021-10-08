# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                options=[{"label": "Cape Canaveral LC-40", "value": "CCAFS LC-40"},
                                         {"label": "Cape Canaveral SLC-40", "value": "CCAFS SLC-40"},
                                         {"label": "Kennedy Space Center LC-39A", "value": "KSC LC-39A"},
                                         {"label": "Vandenberg SLC-4E", "value": "VAFB SLC-4E"},
                                         {"label": "All sites", "value": "all"}],
                                placeholder="Select launch site",
                                searchable=True,
                                value="all"),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={x: f"{x}" for x in range(0, 11000, 1000)}, value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"))
def get_pie_chart(launch_site):
    if launch_site == 'all':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='All sites launch success rates')
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == launch_site]
        fig = px.pie(filtered_df, names='class', title=f'Launch success rates for {launch_site}')

    return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"),
              [Input(component_id="site-dropdown", component_property="value"),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(launch_site, payload_range):
    if launch_site == 'all':
        filtered = spacex_df[(spacex_df["Payload Mass (kg)"] >= payload_range[0]) & \
                             (spacex_df["Payload Mass (kg)"] <= payload_range[1])]
    else:
        filtered = spacex_df[spacex_df["Launch Site"] == launch_site]
        filtered = filtered[(filtered["Payload Mass (kg)"] >= payload_range[0]) & \
                             (filtered["Payload Mass (kg)"] <= payload_range[1])]
    
    fig = px.scatter(filtered, x="Payload Mass (kg)", y="class", color="Booster Version Category")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
