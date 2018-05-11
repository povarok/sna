from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import visdcc
from app import app
from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(visdcc.Network(id='net',
             options = dict(height= '600px', 
                                    width= '100%',
                                    physics={'barnesHut': {'avoidOverlap': 0}},         
                                    )),style={'display': 'none'})
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return app1.layout
    elif pathname == '/apps/app2':
         return app2.layout
    else:
        return app1.layout

if __name__ == '__main__':
    app.run_server(debug=True)
