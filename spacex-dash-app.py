# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# --------------------------------------------
# LAYOUT
# --------------------------------------------
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={
            int(min_payload): str(int(min_payload)),
            int(max_payload): str(int(max_payload))
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter chart for correlation between payload and success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# --------------------------------------------
# CALLBACKS
# --------------------------------------------

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_success_pie(selected_site):
    if selected_site == 'ALL':
        # Successful launches for all sites
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        # Success vs Failed for selected site
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        outcome_counts = site_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['Outcome'] = outcome_counts['class'].map({1: 'Success', 0: 'Failed'})

        fig = px.pie(
            outcome_counts,
            names='Outcome',
            values='count',
            title=f'Total Launch Outcomes for site {selected_site}'
        )

    return fig


# TASK 4: Scatter chart callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    # Filter by payload range
    mask = (
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    )
    filtered_df = spacex_df[mask]

    # Filter by site if not ALL
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Correlation between Payload and Success for {"All Sites" if selected_site == "ALL" else selected_site}',
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run()
	
# --------------------------------------------
# CALLBACKS
# --------------------------------------------

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_success_pie(selected_site):
    if selected_site == 'ALL':
        # Successful launches for all sites
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        # Success vs Failed for selected site
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        outcome_counts = site_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['Outcome'] = outcome_counts['class'].map({1: 'Success', 0: 'Failed'})

        fig = px.pie(
            outcome_counts,
            names='Outcome',
            values='count',
            title=f'Total Launch Outcomes for site {selected_site}'
        )

    return fig


# TASK 4: Scatter chart callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    # Filter by payload range
    mask = (
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    )
    filtered_df = spacex_df[mask]

    # Filter by site if not ALL
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Correlation between Payload and Success for {"All Sites" if selected_site == "ALL" else selected_site}',
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run()