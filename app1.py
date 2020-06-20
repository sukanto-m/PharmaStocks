import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
from datetime import datetime
import pandas as pd
import os
from iexfinance.stocks import get_historical_data




app = dash.Dash()
server = app.server



app.layout = html.Div([
                html.H1(' Pharma Stock Ticker Dashboard'),
                html.Div([html.H3('Enter a stock symbol:', style={'paddingRight':'30px'}),
                dcc.Dropdown(id='my_ticker_symbol',
                            options=[
                                {'label': 'MRNA Moderna Inc.', 'value': 'MRNA'},
                                {'label': 'GILD Gilead Sciences,Inc.', 'value': 'GILD'},
                                {'label':'AMZN Amazon.com,Inc.','value':'AMZN'},
                                {'label':'GOOGL Alphabet Inc', 'value': 'GOOGL'}

                            ],
                            value=['MRNA'],
                            multi=True)

                            ],style={'display':'inline-block','verticalAlign':'top','width':'30%'}),
                            html.Div([html.H3('Select a start and end date:'),
                            dcc.DatePickerRange(id='my_date_picker',
                                                    min_date_allowed=datetime(2015,1,1),
                                                    max_date_allowed=datetime.today(),
                                                    start_date = datetime(2018,1,1),
                                                    end_date = datetime.today())
                                                    ],style={'display':'inline-block'}),
                            html.Div([
                                  html.Button(id='submit-button',
                                                n_clicks=0,
                                                children='Submit',
                                                style={'fontSize':24,'marginLeft':'30px'})
                            ],style={'display':'inline-block'}),

                dcc.Graph(id='my_graph',
                            figure={'data':[
                                    {'x':[1,2],'y':[3,1]}
                            ],'layout':{'title':'Default Title'}}
                            )

])

@app.callback(Output('my_graph','figure'),
                [Input('submit-button','n_clicks')],
                [State('my_ticker_symbol','value'),
                       State('my_date_picker','start_date'),
                       State('my_date_picker','end_date')
                       ])

def update_graph(n_clicks,stock_ticker,start_date,end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        os.environ['IEX_TOKEN'] = 'xxxxxxxxxxxxxxxxx' #IEX token goes here
        df = get_historical_data(tic, start=start, end=end, close_only=True, output_format='pandas')
        traces.append({'x':df.index, 'y': df.close, 'name':tic})

    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
