# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site = list(spacex_df['Launch Site'].unique())
launch_site.insert(0, "ALL")
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': i, 'value': i} for i in launch_site], value="ALL",
                                    placeholder="Select Launch Site here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000,
                                    marks={
                                        0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                        },step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_value):
    if site_value is None:
        raise Exception()
    elif site_value == "ALL":
        fig_pie = px.pie(spacex_df, names="Launch Site", values="class",
            title="Total Successful Launches by Sites")
    else:
        site = spacex_df[spacex_df["Launch Site"]==site_value]
        fig_pie= px.pie(site, names="class",
            title='Total Success Launches By Site')
    return fig_pie
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(site_value, payload_value):
    if site_value is None:
        raise Exception()
    elif site_value == "ALL":
        sliced_df = spacex_df[spacex_df["Payload Mass (kg)"].between(left=payload_value[0], right=payload_value[1])]
        fig_scatter = px.scatter(sliced_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    else:
        sliced_df = spacex_df[(spacex_df['Payload Mass (kg)'].between(left=payload_value[0], right=payload_value[1]))
                                & (spacex_df['Launch Site'] == site_value)]
        fig_scatter = px.scatter(sliced_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig_scatter


# Run the app
if __name__ == '__main__':
    app.run_server()
