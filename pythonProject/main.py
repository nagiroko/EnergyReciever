import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from supabase import create_client, Client
import pandas as pd

# Supabase setup
SUPABASE_URL = 'https://ahugqjdzucmanyidnkvr.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFodWdxamR6dWNtYW55aWRua3ZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTk3NzU4NTAsImV4cCI6MjAzNTM1MTg1MH0.IuXYrEZNedL3KUJs40Ur4BVXsien7BlgbB9CJmUPp4I'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_data():
    response = supabase.table('SurveyResults').select('*').execute()
    if hasattr(response, 'data'):
        return pd.DataFrame(response.data)
    else:
        raise ValueError("Error fetching data from Supabase: {}".format(getattr(response, 'error', 'Unknown error')))

# Dash app setup
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Caffine Results" ,style={'textAlign': 'center'}),
    dcc.Graph(id='donut-chart'),
    dcc.Graph(id='bar-chart'),
    html.Button('Refresh Data', id='refresh-button', n_clicks=0)
])

@app.callback(
    [Output('donut-chart', 'figure'), Output('bar-chart', 'figure')],
    [Input('refresh-button', 'n_clicks')]
)
def update_graph(n_clicks):
    try:
        df = fetch_data()

        if 'EnergyDrinkName' not in df.columns or 'DrinksPerDay' not in df.columns or 'SleepAverageNight' not in df.columns:
            raise ValueError("Required columns are missing in the data.")

        # Donut Chart
        donut_fig = px.pie(df, names='EnergyDrinkName', hole=0.4)
        donut_fig.update_layout(annotations=[dict(text='Total: {}'.format(len(df)), x=0.5, y=0.5, font_size=20, showarrow=False)])

        # Bar Chart for Average Sleep
        avg_sleep = df.groupby('EnergyDrinkName', as_index=False)['SleepAverageNight'].mean()
        bar_fig = px.bar(avg_sleep, x='EnergyDrinkName', y='SleepAverageNight', title='Average Sleep per Energy Drink')

        return donut_fig, bar_fig

    except Exception as e:
        print(f"Error updating graphs: {e}")
        return {}, {}

if __name__ == '__main__':
    app.run_server(debug=True)





