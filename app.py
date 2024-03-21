# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   Graph DOES NOT need to interact with dropdown or slider
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# %%
# import the data
gdp_data = pd.read_csv("gdp_pcap.csv")
gdp_data.head()

# %%
# add a stylesheet 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# cleaning up the dataset 
gdp = gdp_data.melt(id_vars='country', var_name='year', value_name='gdp')

# convert the gdp values to thousands by getting rid of the k value 
gdp['gdp'] = gdp['gdp'].apply(lambda x: float(x.rstrip('k')) * 1000 if isinstance(x, str) and 'k' in x else float(x))

# confirm that gdp values have correctly changed 
print(gdp)

# Convert year values to integers and gdp values to float
gdp['year'] = gdp['year'].astype(int)
gdp['gdp'] = gdp['gdp'].astype(float)

# confirm that the datatype has changed to int and float
print(gdp.dtypes)

# create a graph that can be called back after users using the app select countries and year values
fig = px.line(gdp, x="year", y="gdp", color="country") 
fig.update_layout(title='GDP Value for Selected Years', xaxis_title='Years', yaxis_title='GDP')

# initialize app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define options for the dropdown
dropdown_options = [{'label': country, 'value': country} for country in gdp['country'].unique()]

# 1. A dropdown menu that allows the user to select `country`
# define layout 
app.layout = html.Div([
    html.H1("GDP Per Capita Analysis"), # title
    html.H4(" This dataset shows different countries and columns representing different years from year 1800 to 2100. It is organized in a format where each row represents a different country and each column represents a different year. Each cell in the table contains the GDP per capita value for a specific country in a specific year. In this specific app, a line graph will be generated when countries and year(s) are selected to show GDP change over time."), # description below the title

    # 1. A dropdown menu that allows the user to select `country`
    # define layout
    html.Div([
        html.Div(children= [
            dcc.Dropdown(
                options=dropdown_options,
                id='dropdown',
                placeholder='Select country value(s)', # default value
                multi=True, # allows for multiple country values to be chosen
            )
        ], style={'width': '50%', 'display': 'inline-block'}), # 50% of the screen

    # 2. A slider that allows the user to select `year`
    # define layout
        html.Div([
            dcc.RangeSlider(
                id='slider',
                min = gdp['year'].min(), # originally hard coded but changed to find the minimum year value
                max = gdp['year'].max(), # originally hard coded but changed to find the maximum year value
                step = 1,
                value=[gdp['year'].min(), gdp['year'].max()], # the default value, originally hard coded again but changed
                marks= {year: str(year) for year in range(gdp['year'].min(), gdp['year'].max() + 1, 20)}, # intervals of 20 because it would be too crowded and hard to read visually
            )
        ], style={'width': '50%', 'display': 'inline-block'}), # 50% of the screen

    # 3. A graph that displays the `gdpPercap` for the selected countries over the selected years
    # define layout
        html.Div(children = [ 
            dcc.Graph( 
                id = 'graph', #creating a graph that can be called back for updates
                figure= fig 
            )
        ])
    ])
])

@app.callback( #callback values
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
     Input('slider', 'value')]
)

def update_graph(selected_countries, selected_years):
    if selected_countries is None or selected_years is None: #if no value is selected, it will show the default graph image
        return fig

    filtered_gdp = gdp[gdp['year'].between(selected_years[0], selected_years[1])] #graph is updated by the years the user has selected in the slider

    if selected_countries is not None:
        filtered_gdp = filtered_gdp[filtered_gdp['country'].isin(selected_countries)] #graph is updated by the countries the user has selected in the dropdown option
    
    updated_fig = px.line(filtered_gdp, x="year", y="gdp", color="country") 
    updated_fig.update_layout(title='GDP Value for Selected Years', xaxis_title='Years', yaxis_title='GDP')
    return updated_fig #returns the updated version of the graph with all of the user inputs such as year and country values

# run app
if __name__ == '__main__':
    app.run_server(debug=True)


