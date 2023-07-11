import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown', options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                                id='payload-slider',
                                                min=0,
                                                max=10_000,
                                                step=1000,
                                                marks={0: '0',
                                                       10_000: '10000'},
                                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            data_frame=spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = site_df[site_df['class'] == 1].shape[0]
        failed_count = site_df[site_df['class'] == 0].shape[0]

        fig = px.pie(
            data_frame=site_df,
            values=[success_count, failed_count],
            names=['Success', 'Failed'],
            title='Total Success Launches By Site'
        )
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > payload_range[0]) & (spacex_df['Payload Mass (kg)'] < payload_range[1])]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites'
        )
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > payload_range[0]) & (spacex_df['Payload Mass (kg)'] < payload_range[1]) & (spacex_df['Launch Site'] == entered_site)]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for ' + entered_site
        )
        return fig


if __name__ == '__main__':
    app.run_server()
