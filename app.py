# %%
# import dependencies
import sys
print(sys.executable)

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# %%
# import the data
data = pd.read_csv("data1") 
data.head() # show a part of the dataset

# %%
# add a stylesheet 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define options for the dropdown
dropdown_options = [{'label': genre, 'value': genre} for genre in data['top genre'].unique()]

# Define app layout
app.layout = html.Div([
    html.H1("Top 10 Songs Analysis"),  # title
    html.H6("This dataset shows a comprehensive summary of the music industry, presenting the top 10 songs from 2010 to 2019 globally. Collected from Spotify and Billboard, it shows current music trends in various areas and among various groups of people. Spotify is one of the biggest and popular applications people use for music streaming. Both artists and producers release their singles, albums, and exclusive content through this platform. With a wide collection of data encompassing consumer preferences and listening habits, Spotify gives a valuable resource for understanding what drives viral hits in the music industry. My goal is to take the insights from this dataset to create an interactive dashboard that will allow users to dive into different genres, styles, and the overall most popular songs. This would provide personalized music recommendations based on the user preferences. Although there were many other datasets available, this dataset stood out the most because of its balance of depth and breadth of information. I concluded that this dataset aligns best and provides a solid basis for accomplishing my goals. ",
            style={'font-size': '16px', 'margin-bottom': '14px'}),  # added style for smaller font size and margin bottom
    
    # Define layout for year slider
    html.Div([
        html.Div([
            dcc.RangeSlider(
                id='year-slider',
                min=data['year'].min(),  # finds the minimum year value
                max=data['year'].max(),  # finds the maximum year value
                step=1,
                value=[data['year'].min(), data['year'].max()],  # the default value
                marks={year: str(year) for year in range(data['year'].min(), data['year'].max() + 1, 1)},
            )
        ])
    ]),
    
    # Container for word cloud
    html.Div(id='wordcloud-container'),
    
    # dropdown menu to change genre value
    html.Div([
        html.Div(children= [
            dcc.Dropdown(
                options=dropdown_options,
                id='genre-dropdown',
                placeholder='Select genre value(s)', # default value
                multi=True, # allows for multiple genre values to be chosen
            )
        ], style={'width': '50%', 'display': 'inline-block'}), # 50% of the screen
    ])
])

# Define callback to update word cloud based on selected year
@app.callback(
    Output('wordcloud-container', 'children'),
    [Input('year-slider', 'value'),
    Input('genre-dropdown', 'value')]
)
def update_wordcloud(selected_years, selected_genres):

    # Filter data based on selected years
    filtered_data = data[(data['year'] >= selected_years[0]) & (data['year'] <= selected_years[1])]
    
    # Filter data based on selected genres
    if selected_genres:
        filtered_data = filtered_data[filtered_data['top genre'].isin(selected_genres)]
    
    # Extract artist values
    text_values = filtered_data['artist'].tolist()
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(text_values))
    
    # Render word cloud as an image in the app
    return html.Img(src=wordcloud.to_image())

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


