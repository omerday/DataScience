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

location_dict = [{"label": row["Launch Site"], "value": row["Launch Site"]} for index, row in spacex_df[["Launch Site"]].drop_duplicates(inplace=False).iterrows()]
location_dict.append({'label': 'All Sites', 'value': 'ALL'})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),                                
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                    options=location_dict,
                                    value="ALL",
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # html.Div(id="success-pie-chart", className="chart-grid", style={"display":"flex"}),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id="payload-slider",
                                                        min=0, max=10000, step=1000,
                                                        value=[min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    successes = []
    for index, row in filtered_df.iterrows():
        if row["class"] == 1:
            successes.append("Success")
        else:
            successes.append("Failed")
    filtered_df["success"] = successes
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names="Launch Site", 
        title='Successful Launches by Launch Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.pie(filtered_df, values='Flight Number', 
        names='success', 
        title='Percentage of Successful Launches in the Selected Launch Site')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property="figure"),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, entered_payload):
    filtered_data = spacex_df[(spacex_df["Payload Mass (kg)"] >= entered_payload[0]) & (spacex_df["Payload Mass (kg)"] <= entered_payload[1])]
    if entered_site != "ALL":
        filtered_data = filtered_data[filtered_data["Launch Site"] == entered_site]
    fig = px.scatter(filtered_data, 
            y="class", 
            x="Payload Mass (kg)", 
            color="Booster Version Category",
            title="Payload Mass Affect on Launch Success")
    return fig
        

# Run the app
if __name__ == '__main__':
    app.run_server()
