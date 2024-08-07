# PROJECT NAME: U.S.A. FOOD IMPORT DASHBOARD
# AUTHOR: MIKE MUSAS


# REQUIRED PYTHON PACKAGES TO IMPORT
import pandas as pd
import base64
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# ------------------------------------------------------------------------------------------------
# APP INITIALIZATION
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------------------------
# PRE TASKS SECTION

# Import and read data
# Import the data on us import food value in USD
food_value = pd.read_csv('data/us_food_imports_food_value.csv')
# Import the data on us import food category
food_value_categories = pd.read_csv('data/us_food_imports_food_value_categories.csv')
# Import the data on us import food volume in metric tons
food_volume = pd.read_csv('data/us_food_imports_food_volume.csv')
# Import the data on us import food category
food_volume_categories = pd.read_csv('data/us_food_imports_food_volume_categories.csv')
# Import us import food value (countries)
food_value_countries = pd.read_csv('data/countries.csv')

# Insert an image
image_file = 'assets/mmk_logo_desgin.png'
encoded_image = base64.b64encode(open(image_file, 'rb').read()).decode('ascii')


# ------------------------------------------------------------------------------------------------
# GRAPHS SECTION

# LINE PLOT for Food value
def line_plot_food_value(data, column1, column2, the_title, x_label, y_label):
    # Food Value Over Time Figure
    fig = go.Figure()
    # Food value Line plot
    fig.add_trace(go.Scatter(
        x=data[column1],
        y=data[column2] * 1000,
        mode='lines',
        line=dict(color='#D9560B', width=5), connectgaps=True)
    )

    # Adjust the graph layout
    fig.update_layout(
        # Graph's title
        title=dict(
            text=the_title,
            font=dict(size=20, color='#0C0B09')
        ),
        # X-axis Title
        xaxis_title=dict(
            text=x_label,
            font=dict(size=14, color='#595959')
        ),
        # Y-axis Title
        yaxis_title=dict(
            text=y_label,
            font=dict(size=14, color='#595959')
        ),
        # Graph background
        plot_bgcolor='white',
        # Graph legend
        showlegend=False,
        # X-axis formatting
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            ticks='outside',
            tickcolor='#595959',
            tickfont=dict(
                color='#595959'
            )
        ),
        # Y-axis formatting
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            tickfont=dict(
                color='#595959'
            )
        ),
        # Adjust the margins of the graph
        margin=dict(
            l=100,
            r=30,
            b=70,
            t=70,
            pad=4
        )
    )

    return fig


# BARCHART for the food value
def bar_plot_food_value(data, column1, column2, the_title, x_label, y_label, year_filter):
    # Filter the data
    data_new = data.loc[data["Year"] == int(year_filter)]
    # Change the food value column to Millions of dollars
    data_new[column2] = data_new[column2] * 1000
    # Sort the data in ascending order by food value
    data_new = data_new.sort_values(by=[column2])
    # Initialize the graph
    fig = go.Figure()

    # Plot the graph
    fig.add_trace(go.Bar(
        x=data_new[column2], y=data_new[column1],
        marker=dict(color=['#B4BEC9', '#B4BEC9', '#B4BEC9', '#D9560B', '#D9560B', '#D9560B', '#D9560B',
                           '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B']),
        orientation='h',
        text=['{:,}M'.format(round(i / 1000000, 1)) for i in
              data_new[column2]],
        textfont=dict(color='white', size=12),
        textposition='inside'  # more ['inside', 'outside', 'none']
    ))

    # Figure layout
    fig.update_layout(
        # Graph Title
        title=dict(
            text=the_title,
            font=dict(size=20, color='#0C0B09')
        ),
        # X-axis Label
        xaxis_title=dict(
            text=x_label,
            font=dict(size=14, color='#595959')
        ),
        # X-axis formatting
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            ticks='outside',
            tickcolor='#595959',
            tickfont=dict(
                color='#595959'
            )
        ),
        # Y-axis Label
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            tickfont=dict(
                color='#595959'
            )
        ),
        # Plot background
        plot_bgcolor='white',
        # Adjust the margins of the graph
        margin=dict(
            l=100,
            r=30,
            b=70,
            t=70,
            pad=4
        )
    )

    return fig


# BARCHART for the food value (Countries, category types)
def bar_plot_food_value_others(data, column1, column2, the_title, x_label, y_label, year_filter=None, category_filter=None):

    # Filter the data by the specified year
    if year_filter is None:

        if category_filter is None:
            data_new = data.copy()
        elif category_filter is not None:
            data_new = data.loc[data["Food Category"] == category_filter]
    else:
        if category_filter is None:
            data_new = data.loc[data["Year"] == year_filter]
        elif category_filter is not None:
            data_new = data.loc[data["Food Category"] == category_filter]

    #
    data_new[column2] = data_new[column2] * 1000

    # Pivot the data
    data_new = data_new.groupby(column1)[column2].sum().reset_index().sort_values(by=column2)
    data_new = pd.DataFrame(data_new)

    # Initialize the bar chart
    fig = go.Figure()

    # Plot the graph
    fig.add_trace(go.Bar(
        x=data_new[column2], y=data_new[column1],
        marker=dict(color=['#B4BEC9', '#B4BEC9', '#B4BEC9', '#D9560B', '#D9560B', '#D9560B', '#D9560B',
                           '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B', '#D9560B']),
        orientation='h',
        text=['{:,}M'.format(round(i / 1000000, 1)) for i in data_new[column2]],
        textfont=dict(color='white', size=12),
        textposition='inside'
    ))

    # Figure layout
    fig.update_layout(
        title=dict(text=the_title, font=dict(size=20, color='#0C0B09')),
        xaxis_title=dict(text=x_label, font=dict(size=14, color='#595959')),
        xaxis=dict(showline=True, showgrid=False, showticklabels=True, linecolor='#D9D9D9', linewidth=2,
                   ticks='outside', tickcolor='#595959', tickfont=dict(color='#595959')),
        yaxis=dict(showline=False, showgrid=False, showticklabels=True, linecolor='#D9D9D9', linewidth=2,
                   tickfont=dict(color='#595959')),
        plot_bgcolor='white',
        margin=dict(l=100, r=30, b=70, t=70, pad=4)
    )

    return fig


# ------------------------------------------------------------------------------------------------
# APPLICATION LAYOUT
app.layout = html.Div(children=[
    # ------------------------------------------------------------------------------------------------
    # TITLE SECTION
    dbc.Row(children=[
        dbc.Col([
            html.Div(children=[
                # The Title of the dashboard
                html.Div("U.S.A. Food Imports Dashboard",
                         style={'font-size': '54px', 'font-family': 'ApparatCond', 'font-weight': 'bold',
                                'margin-top': '5px', 'color': 'white'}
                         ),
                # The Subtitle of the dashboard
                html.Div("The data includes US imports from the year 2010 to 2023",
                         style={'font-size': '20px', 'font-family': 'Lato', 'font-weight': 'regular',
                                'margin-top': '0px', 'color': '#F2A444'}
                         )
            ])
        ],
            width={'size': 10},
            xs=8, sm=8, md=8, lg=10, xl=10
        )
    ],
        justify='center',
        style={'background-color': '#023E73', 'padding': '10px 0 20px 10px'}),

    # Line Break
    dbc.Row(dbc.Col(html.Br())),

    # ------------------------------------------------------------------------------------------------
    # DASHBOARD BODY SECTION
    dbc.Row(children=[

        # --------------------------------------------------------------------------------------------
        # FILTERS SECTION
        dbc.Col([
            # Filter Title
            html.Div(children=[
                html.Div('Filters',
                         style={'font-size': '18px', 'font-weight': 'bold', 'color': '#000000',
                                'padding': '15px 0 0 15px'}),
                html.Hr(style={'color': '#D9D9D9'}),
            ]),

            # Year Filter Title
            html.Div(children=[
                # The title
                html.Div('Year',
                         style={'font-size': '16px', 'color': '#000000',
                                'padding': '5px 30px 10px 15px'}),
                # Year Filters Choice Dropdown Menu
                html.Div(dcc.Dropdown(
                    id='year-input',
                    options=[{'label': i, 'value': i}
                             for i in ['All', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016',
                                       '2015', '2014', '2013', '2012', '2011', '2010']],
                    value='All'
                ), style={'width': '90%', 'margin-left': '10px'})
            ]),

            # Line break
            html.Div(html.Br()),

            # Food Category
            html.Div(children=[
                # The title
                html.Div('Food Category',
                         style={'font-size': '16px', 'color': '#000000',
                                'padding': '5px 30px 10px 15px'}),
                # Year Filters Choice Dropdown Menu
                html.Div(dcc.Dropdown(
                    id='category-input',
                    options=[{'label': i, 'value': i}
                             for i in ['All', 'Beverages', 'Cocoa and chocolate', 'Coffee, tea, and spices', 'Dairy',
                                       'Fish and shellfish', 'Fruits', 'Grains', 'Live meat animals', 'Meats', 'Nuts',
                                       'Sugar and candy', 'Vegetable oils', 'Vegetables', 'Other edible products']],
                    value='All'
                ), style={'width': '90%', 'margin-left': '10px'})
            ]),

        ],
            width={'size': 2},
            style={'background-color': '#E8E8E8',
                   'border-radius': '12px', 'padding': '0 0 100px 0',  # padding [top right bottom left]
                   'margin-right': '30px', 'height': '400px'},
            xs=6, sm=6, md=6, lg=2, xl=2
        ),

        # --------------------------------------------------------------------------------------------
        # DASHBOARD ANALYSIS SECTION
        dbc.Col(children=[

            # ----------------------------------------------------------------------------------------
            # OVERVIEW SECTION
            dbc.Row(children=[
                # Total Food Value
                dbc.Col([
                    # Total Food Value
                    html.Div([
                        html.Div(id='total-food-value',
                                 style={'font-size': '38px', 'font-weight': 'bold', 'color': '#D94B2B'}),

                        html.Div('Total Food Value',
                                 style={'color': '#000000'})
                    ],
                        style={'text-align': 'center', 'padding': '30px 0 30px 0',
                               'background-color': '#D9D9D9', 'border-radius': '12px'}
                    )
                ],
                    width={'size': 4},
                    style={'padding-right': '10px', 'padding-top': '10px'},
                    xs=8, sm=8, md=8, lg=4, xl=4
                ),

                # Average Food Value
                dbc.Col([
                    # Average Food Value
                    html.Div([
                        html.Div(id='average-food-value',
                                 style={'font-size': '38px', 'font-weight': 'bold', 'color': '#D94B2B'}),

                        html.Div('Average Food Value',
                                 style={'color': '#000000'})
                    ],
                        style={'text-align': 'center', 'padding': '30px 0 30px 0',
                               'background-color': '#D9D9D9', 'border-radius': '12px'}
                    )
                ],
                    width={'size': 4},
                    style={'padding-right': '10px', 'padding-top': '10px'},
                    xs=8, sm=8, md=8, lg=4, xl=4
                ),

                # Total Food Volume
                dbc.Col([
                    # Total Food Value
                    html.Div([
                        html.Div(id='total-food-volume',
                                 style={'font-size': '38px', 'font-weight': 'bold', 'color': '#D94B2B'}),

                        html.Div('Total Food Volume',
                                 style={'color': '#000000'})
                    ],
                        style={'text-align': 'center', 'padding': '30px 0 30px 0',
                               'background-color': '#D9D9D9', 'border-radius': '12px'}
                    )
                ],
                    width={'size': 4},
                    style={'padding-right': '10px', 'padding-top': '10px'},
                    xs=8, sm=8, md=8, lg=4, xl=4
                )
            ], justify='center'),

            # Space Break
            dbc.Row(dbc.Col(html.Br())),

            # ----------------------------------------------------------------------------------------
            # FIRST ROW CHARTS
            dbc.Row(children=[
                # Chart 1
                dbc.Col([
                    # Total Food Value Over Time
                    dcc.Graph(id='food-value-overtime',
                              style={'border-radius': '12px', 'overflow': 'hidden'})
                ],
                    width={'size': 6},
                    style={'padding-right': '10px', 'padding-bottom': '20px'},
                    xs=12, sm=12, md=12, lg=6, xl=6
                ),

                # Chart 2
                dbc.Col([
                    html.Div([
                        # Total Food Volume Over Time
                        html.Div(dcc.Graph(id='food-volume-overtime',
                                           style={'border-radius': '12px', 'overflow': 'hidden'})),
                    ])
                ],
                    width={'size': 6},
                    xs=12, sm=12, md=12, lg=6, xl=6
                )
            ], justify='center'
            ),

            # Space Break
            dbc.Row(dbc.Col(html.Br())),

            # ----------------------------------------------------------------------------------------
            # SECOND ROW CHARTS
            dbc.Row(children=[
                # Chart 1
                dbc.Col([
                    html.Div([
                        # Total ...
                        html.Div(dcc.Graph(id='food-value-countries',
                                           style={'border-radius': '12px', 'overflow': 'hidden',
                                                  'height': '700px'})),
                    ])
                ],
                    width={'size': 6},
                    style={'padding-right': '10px', 'padding-bottom': '20px'},
                    xs=12, sm=12, md=12, lg=6, xl=6
                ),

                # Chart 2
                dbc.Col([
                    html.Div([
                        # Total ...
                        html.Div(dcc.Graph(id='food-value-types',
                                           style={'border-radius': '12px', 'overflow': 'hidden',
                                                  'height': '700px'})),
                    ])
                ],
                    width={'size': 6},
                    style={'padding-right': '10px', 'padding-bottom': '20px'},
                    xs=12, sm=12, md=12, lg=6, xl=6
                )
            ])

        ],
            width={'size': 8}
        )

    ], justify='center'),

    # Space Break
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Br())),

    # ------------------------------------------------------------------------------------------------
    # FOOTER SECTION
    dbc.Row(children=[
        # Copyright and Data Source
        dbc.Col([
            html.Div([
                # Copyright
                html.Div('Made by',
                         style={'color': 'white', 'margin-right': '5px'}),
                html.Div('Mike Musas',
                         style={'color': 'white', 'font-family': 'Lato', 'font-weight': 'bold',
                                'margin-right': '5px'}),
                html.Div('|',
                         style={'color': 'white', 'font-family': 'Lato', 'font-weight': 'regular',
                                'margin-right': '5px'}),

                # Data Source
                html.Div('Data Source:',
                         style={'color': 'white', 'font-family': 'Lato', 'font-weight': 'regular',
                                'margin-right': '5px'}),
                html.Div(html.A("data.gov", href='https://catalog.data.gov/dataset/u-s-food-imports',
                                style={'color': '#F2A444', 'font-family': 'Lato', 'font-weight': 'bold'}))

            ], style={'display': 'flex', 'padding-top': '15px'})
        ],
            width={'size': 9},
            xs=8, sm=8, md=8, lg=9, xl=9
        ),

        # Logo Section
        dbc.Col(children=[
            html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                              style={'width': '50%', 'height': '50%'}))
        ],
            width={'size': 1},
            style={'float': 'right'},
            xs=2, sm=2, md=2, lg=1, xl=1
        )
    ],
        justify='center',
        style={'background-color': '#023E73', 'padding': '10px 0 20px 10px'}
    )

], style={'background-color': '#F5F5F5'})


# CALLBACK SECTION

# OVERVIEW VALUES
@app.callback([
    Output(component_id='total-food-value', component_property='children'),
    Output(component_id='average-food-value', component_property='children'),
    Output(component_id='total-food-volume', component_property='children')
], [
    Input(component_id='year-input', component_property='value'),
    Input(component_id='category-input', component_property='value'),
],
)
def update_food_value(year_input, category_input):
    # Filter for year
    if year_input == 'All':
        # For this case 'All' is selected the category input
        if category_input == 'All':
            total_food_value = food_value['Total foods Value'].sum()
            average_food_value = food_value['Total foods Value'].mean()
            total_food_volume = food_volume['Total foods Volume'].sum()

            return (
                '{:,}M'.format(round(total_food_value / 1000, 1)),
                '{:,}M'.format(round(average_food_value / 1000, 1)),
                '{:,}M'.format(round(total_food_volume / 1000, 1))
            )
        # For cases where a specific category is selected
        else:
            total_food_value = food_value[category_input].sum()
            average_food_value = food_value[category_input].mean()
            total_food_volume = food_volume[category_input].sum()

            return (
                '{:,}M'.format(round(total_food_value / 1000, 1)),
                '{:,}M'.format(round(average_food_value / 1000, 1)),
                '{:,}M'.format(round(total_food_volume / 1000, 1))
            )

    # Other Year Selected
    else:
        # If all the food categories are included
        if category_input == 'All':
            total_food_value = food_value.loc[food_value['Year'] == int(year_input), 'Total foods Value'].sum()
            average_food_value = food_value.loc[food_value['Year'] == int(year_input), 'Average Food Value'].mean()
            total_food_volume = food_volume.loc[food_volume['Year'] == int(year_input), 'Total foods Volume'].sum()

            # Returns the results
            return (
                '{:,}M'.format(round(total_food_value / 1000, 1)),
                '{:,}M'.format(round(average_food_value / 1000, 1)),
                '{:,}M'.format(round(total_food_volume / 1000, 1))
            )

        # If a specific category is selected
        else:
            total_food_value = food_value.loc[food_value['Year'] == int(year_input), category_input].sum()
            average_food_value = food_value.loc[food_value['Year'] == int(year_input), category_input].mean()
            total_food_volume = food_volume.loc[food_volume['Year'] == int(year_input), category_input].sum()

            # Returns the results
            return (
                '{:,}M'.format(round(total_food_value / 1000, 1)),
                '{:,}M'.format(round(average_food_value, 1000)),
                '{:,}M'.format(round(total_food_volume / 1000, 1))
            )


# ------------------------------------------------------------------------------------------------
# GRAPH 1: TOTAL FOOD VALUE OVER TIME
@app.callback(
    Output(component_id='food-value-overtime', component_property='figure')
    , [
        Input(component_id='year-input', component_property='value'),
        Input(component_id='category-input', component_property='value')
    ]
)
def food_value_over_time(year_input, category_input):
    if year_input == 'All':
        # In case all categories are included
        if category_input == 'All':
            return line_plot_food_value(data=food_value, column1="Year", column2="Total foods Value",
                                        the_title="Total Value of Food Imported per Year",
                                        x_label="Year", y_label="Total Food Value ($)")
        # In case one category is selected
        else:
            return line_plot_food_value(data=food_value, column1="Year", column2=category_input,
                                        the_title="Total Value of Food Imported per Year",
                                        x_label="Year", y_label="Total Food Value ($)")

    # In case a specific year is selected
    else:
        # In case all categories are included
        if category_input == 'All':
            return bar_plot_food_value(data=food_value_categories, column1="Food Category", column2="Food Value",
                                       the_title="Total Value of Food Imported per Category",
                                       y_label="Food Category", x_label="Total Food Value ($)", year_filter=year_input)

        # In case one category is selected
        else:
            return line_plot_food_value(data=food_value, column1="Year", column2=category_input,
                                        the_title="Total Value of Food Imported per Year",
                                        x_label="Year", y_label="Total Food Value ($)")


# ------------------------------------------------------------------------------------------------
# GRAPH 2: TOTAL FOOD VOLUME OVER TIME
@app.callback(
    Output(component_id='food-volume-overtime', component_property='figure')
    , [
        Input(component_id='year-input', component_property='value'),
        Input(component_id='category-input', component_property='value')
    ]
)
def food_volume_over_time(year_input, category_input):
    # Includes all the years
    if year_input == 'All':
        # In case all categories are included
        if category_input == 'All':
            return line_plot_food_value(data=food_volume, column1="Year", column2="Total foods Volume",
                                        the_title="Total Volume of Food Imported per Year",
                                        x_label="Year", y_label="Total Volume Value (Metric Tons)")
        # In case one category is selected
        else:
            return line_plot_food_value(data=food_volume, column1="Year", column2=category_input,
                                        the_title="Total Volume of Food Imported per Year",
                                        x_label="Year", y_label="Total Volume Value (Metric Tons)")

    # In case a specific year is selected
    else:
        # In case all categories are included
        if category_input == 'All':
            return bar_plot_food_value(data=food_volume_categories, column1="Food Category", column2="Food Volume",
                                       the_title="Total Volume of Food Imported per Year",
                                       y_label="Food Category", x_label="Total Volume Value (Metric Tons)",
                                       year_filter=year_input)

        # In case one category is selected
        else:
            return line_plot_food_value(data=food_volume, column1="Year", column2=category_input,
                                        the_title="Total Volume of Food Imported per Year",
                                        x_label="Year", y_label="Total Volume Value (Metric Tons)")


# ------------------------------------------------------------------------------------------------

# GRAPH 3: TOTAL FOOD VALUE BY COUNTRIES
@app.callback(
    Output(component_id='food-value-countries', component_property='figure'),
    [
        Input(component_id='year-input', component_property='value'),
        Input(component_id='category-input', component_property='value')
    ]
)
def food_value_countries_func(year_input, category_input):
    if year_input == 'All':
        if category_input == 'All':
            return bar_plot_food_value_others(data=food_value_countries, column1="Country", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=None,
                                              category_filter=None)
        else:
            return bar_plot_food_value_others(data=food_value_countries, column1="Country", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=None,
                                              category_filter=category_input)

    else:
        if category_input == 'All':
            return bar_plot_food_value_others(data=food_value_countries, column1="Country", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=year_input,
                                              category_filter=None)
        else:
            return bar_plot_food_value_others(data=food_value_countries, column1="Country", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=year_input,
                                              category_filter=category_input)


# ------------------------------------------------------------------------------------------------
# GRAPH 4: TOTAL FOOD VOLUME BY CATEGORY TYPE
@app.callback(
    Output(component_id='food-value-types', component_property='figure'),
    [
        Input(component_id='year-input', component_property='value'),
        Input(component_id='category-input', component_property='value')
    ]
)
def food_value_types_func(year_input, category_input):
    if year_input == 'All':
        if category_input == 'All':
            return bar_plot_food_value_others(data=food_value_countries, column1="Category Type", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=None,
                                              category_filter=None)
        else:
            return bar_plot_food_value_others(data=food_value_countries, column1="Category Type", column2='Food Value',
                                              the_title=f"Total Value of Food Imported per Country",
                                              x_label="Total Food Value ($)", y_label="Country", year_filter=None,
                                              category_filter=category_input)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
