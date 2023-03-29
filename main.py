#######
# Here we'll use the mpg.csv dataset to demonstrate
# how multiple inputs can affect the same graph.
######
from dash import html
from dash import dcc
from dash import Dash
import dash
from dash import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
app = Dash(__name__)

df = pd.read_csv('mpg.csv')

features = df.columns
image = 'assets/BITS_Hyderabad_campus_logo.gif'
logo = 'assets/images.jfif'
app.layout = html.Div( [
        html.H1("Welcome Mechanical Department at BITS HYDERABAD"),

        html.Img(src = image,),
        html.Img(src = logo),


        html.Div([

            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i.title(), 'value': i} for i in features],
                value = 'horsepower'

            ),


        ],
        style={'width': '48%', 'display': 'inline-block'}),
    html.Div([

        dcc.Dropdown(
            id='yaxis',
            options=[{'label': i.title(), 'value': i} for i in features],
            value='displacement'
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ,
       html.Div([
dcc.Graph(id ="feature-graphic"),
       ],  style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),


    html.Div([
dcc.Graph(
        id='mpg_line',
        figure={
            'data': [go.Scatter(
                x = [0,1],
                y = [0,1],
                mode = 'lines'
            )],
            'layout': go.Layout(
                title = 'acceleration',
                margin = {'l':0}
            )
        }
    ),
        dcc.Markdown(
            id = 'mpg_stats'
        )

    ], style ={'width': '20%', 'height': '50%','display': 'inline-block'}),


          dcc.RadioItems(options=[{'label': i.title(), 'value': i} for i in features], value = '', id = 'button1', style= {'display': 'block'}),
          dcc.RadioItems(options=[{'label': i.title(), 'value': i} for i in features], value = '', id = 'button2'),
          dcc.Markdown(children= '', id = 'textdis'),


           ], style = {'padding': 10})


@app.callback(
    Output('feature-graphic', 'figure'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value')],

     )



def update_graph(xaxis_name, yaxis_name):
    return {
        'data': [go.Scatter(
            x=df[xaxis_name],
            y=df[yaxis_name],
            text=df['name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_name.title()},
            yaxis={'title': yaxis_name.title()},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(Output('textdis','children'),
             [Input('button1', 'value'),
              Input('button2', 'value')],)


def update_text(user_selected,test_selected):

    return f"the radio buttons you chose are: {user_selected} {test_selected}"

@app.callback( Output('mpg_line', 'figure'),
    [Input('feature-graphic', 'hoverData')])
def callback_graph(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    fig = {
        'data': [go.Scatter(
            x = [0,1/df.iloc[v_index]['displacement']],
            y = [0,60/df.iloc[v_index]['mpg']],
            mode='lines',
            line={'width':2*df.iloc[v_index]['cylinders']}
        )],
        'layout': go.Layout(
            title = df.iloc[v_index]['name'],
            xaxis = {'visible':False},
            yaxis = {'visible':False, 'range':[0,60/df['acceleration'].min()]},
            margin = {'l':0},
            height = 300
        )
    }
    return fig

@app.callback(
    Output('mpg_stats', 'children'),
    [Input('feature-graphic', 'hoverData')])
def callback_stats(hoverData):
    df_index = hoverData['points'][0]['pointIndex']
    stats = """
        {} cylinders
        {}cc displacement
        0 to 60mph in {} seconds
        """.format(df.iloc[df_index]['cylinders'],
            df.iloc[df_index]['displacement'],
            df.iloc[df_index]['acceleration'])
    return stats

if __name__ == '__main__':
    app.run_server(debug = True, port =8081)


