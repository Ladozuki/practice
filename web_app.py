import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd 
import random

#creasting sample data sets 

app = dash.Dash(__name__)

# Data for route and vessel performance prediction
route_performance_df = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'ETA': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'ActualArrivalTime': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'EstFuelCons': [random.randint(80, 120) for i in range (12)], 
    'ActFuelCons': [random.randint(80, 120) for i in range (12)] 
})

# Data for safety and risk management 
safety_df = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'CollisionRisk': [0.1, 0.2, 0.15, 0.3, 0.25, 0.2, 0.18, 0.22, 0.28, 0.3, 0.25, 0.2]
})


# Data for cargo and fleet management 
# Define possible types of tankers and containers
tanker_types = ['Crude Oil', 'Chemical', 'LNG', 'LPG', 'Coastal Tanker', 'Aframax', 'Suez-Max', 'VeryLargeCrudeCarrier', 'ULCC']
container_types = ['Small Feeder', 'Feeder', 'Feeder Max', 'Panamax', 'Post-Panamax', 'Ultra Large Container Ship (ULCS)']

# Generate random types for each month
tanker_data = [random.choice(tanker_types) for a in range(12)]
container_data = [random.choice(container_types) for b in range(12)]

# Define ship categories and types
ship_types = {
    'OSV': ['Platform Supply Vessel', 'AnchorHandlingTug', 'OffshoreConstructionVeh'],
    'CONTAINER': container_types,
    'TANKER': tanker_types
}

# Define function to generate random dimensions for each ship type
def generate_dimensions(ship_type):
    if ship_type == 'Platform Supply Vessel':
        return random.randint(60, 100), random.randint(15, 25)  # Random length and breadth for PSV
    elif ship_type in container_types:
        return random.randint(200, 400), random.randint(30, 60)  # Random length and breadth for Container ship
    elif ship_type in tanker_types:
        return random.randint(150, 350), random.randint(20, 50)  # Random length and breadth for Tanker
    else:
        return None, None

# Function to generate random capacity for tankers
def generate_capacity(ship_type):
    if ship_type == 'Crude Oil':
        return random.randint(50000, 500000)  # Random capacity between 50,000 and 500,000 DWT
    elif ship_type == 'Chemical':
        return random.randint(10000, 100000)  # Random capacity between 10,000 and 100,000 DWT
    elif ship_type == 'LNG':
        return random.randint(100000, 300000)  # Random capacity between 100,000 and 300,000 DWT
    elif ship_type == 'LPG':
        return random.randint(50000, 150000)  # Random capacity between 50,000 and 150,000 DWT
    elif ship_type == 'Coastal Tanker':
        return random.randint(5000, 50000)  # Random capacity between 5,000 and 50,000 DWT
    elif ship_type == 'Aframax':
        return random.randint(80000, 120000)  # Random capacity between 80,000 and 120,000 DWT
    elif ship_type == 'Suez-Max':
        return random.randint(120000, 200000)  # Random capacity between 120,000 and 200,000 DWT
    elif ship_type == 'VeryLargeCrudeCarrier':
        return random.randint(200000, 320000)  # Random capacity between 200,000 and 320,000 DWT
    elif ship_type == 'ULCC':
        return random.randint(320000, 550000)  # Random capacity between 320,000 and 550,000 DWT
    elif ship_type == 'Small Feeder':
        return random.randint(500, 1000)  # Random capacity between 500 and 1,000 TEU
    elif ship_type == 'Feeder':
        return random.randint(1000, 2000)  # Random capacity between 1,000 and 2,000 TEU
    elif ship_type == 'Feeder Max':
        return random.randint(2000, 3000)  # Random capacity between 2,000 and 3,000 TEU
    elif ship_type == 'Panamax':
        return random.randint(3000, 5000)  # Random capacity between 3,000 and 5,000 TEU
    elif ship_type == 'Post-Panamax':
        return random.randint(5000, 10000)  # Random capacity between 5,000 and 10,000 TEU
    elif ship_type == 'Ultra Large Container Ship (ULCS)':
        return random.randint(10000, 24000)  # Random capacity between 10,000 and 24,000 TEU
    else:
        return None
# Create DataFrame
cargo_df = pd.DataFrame({
    'Month': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'CargoCapacity': [random.randint(900, 1200) for _ in range(12)],
    'VesselCategory': ['OSV', 'CONTAINER', 'TANKER'] * 4  # Use keys from ship_types dictionary
})

# Add ship type column
cargo_df['ship_type'] = cargo_df['VesselCategory'].apply(lambda x: random.choice(ship_types[x]))

# Add dimensions column
cargo_df['Dimensions'] = cargo_df['ship_type'].apply(generate_dimensions)
cargo_df['Dimensions'] = cargo_df['Dimensions'].apply(lambda x : str(x))

# Add capacity column
cargo_df['Capacity (DWT)'] = cargo_df['ship_type'].apply(generate_capacity)


print(cargo_df)


# Data for logistics optimization
port_data = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'PortCongestion': [0.1, 0.2, 0.15, 0.3, 0.25, 0.2, 0.18, 0.22, 0.28, 0.3, 0.25, 0.2]
})

app.layout = html.Div([
    html.H1("Maritime Operations Optimisation Dashboard"),
    
    #add components here
    html.Div([
        html.H2("Route and Vessell Perfomance Prediction"),
        dash_table.DataTable(data = route_performance_df.to_dict('records'),
                             columns = [{"name": j, "id": j}for j in route_performance_df.columns]),
        #Safety/Risk mgt related graphs / components
        dcc.Graph(id = 'safety-risk')
    ]),

    html.Div([
        html.H2("Cargo and Fleet Management"),
        #Graphs/ Other components re: fleet/cargo mgt
        dash_table.DataTable(data = cargo_df.to_dict('records'),
                             columns = [{"name": i, "id": i} for i in cargo_df.columns]),
        dcc.Graph(id = 'Carg-fleet')
    ]),

    html.Div([
        html.H2("Port Logisitics Optimisation"),
        #Add graphs or other components related to logistics optimisation
        dcc.Graph(id = 'Port-Log-ops')
    ])
])

#Callbacks to update graphs with sample data
@app.callback(
    Output('safety-risk', 'figure'),
    Input('safety-risk', 'id')
)
def update_route_vessel(graph_id):
    traces = [
        go.Scatter( x = route_performance_df['Date'], y = route_performance_df['EstFuelCons'],
                   mode = 'lines', name = ' Estimated Fuel Consumption'),
        go.Scatter(x = route_performance_df['Date'], y = route_performance_df['ActFuelCons'], 
                    mode = 'lines', name = 'Actual Fuel Consumption')
    ]
    layout = go.Layout(title = 'Route and Vess Perfomance Prediction'
                       ,xaxis = dict(title = 'Date'),
                       yaxis = dict(title='Fuel Consumption'))
    return {'data': traces, 'layout': layout}


@app.callback(
    Output('Carg-fleet', 'figure'),
    Input('Carg-fleet', 'id')
)
def update_cargo_graph(graph_id):
    traces = [
        go.Bar(x = cargo_df['Month'], y = cargo_df['CargoCapacity'], name = 'Cargo Capacity'),
        #go.Bar(x = cargo_df['Month'], y = cargo_df['DemandForecast'], name = 'Demand')
    ]
    
    layout = go.Layout(title = 'Cargo and Fleet Management',
                        xaxis = dict(title='Month'),
                        yaxis = dict(title = 'Quantity (Tons)'))
    
    return {'data': traces, 'layout': layout}

@app.callback(Output('Port-Log-ops', 'figure'),
              Input('Port-Log-ops', 'id'))

def update_port_logs_graph(graph_id):
    traces = [
        go.Scatter(x = port_data['Date'], y = port_data['PortCongestion'], 
                   mode = 'lines', name = 'PortCongestion')]
    
    layout = go.Layout(title = 'Port Logisitics Optimisation',
                       xaxis = dict(title= 'Date'),
                       yaxis = dict(title = 'Congestion Level'))
    
    return {'data': traces, 'layout': layout}

            
if __name__ == '__main__':
    app.run_server(debug= True)