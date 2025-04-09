from dash import Dash, html, dcc, Input, Output, State, ctx
import dash
import plotly.express as px
import psutil
from collections import deque
import time
from threading import Thread

app = Dash(__name__)
app.title = "Real-Time Process Monitoring Dashboard"

NUM_CPUS = psutil.cpu_count(logical=True)

# Data Storage (Keep only last 10 seconds of data)
cpu_data = deque(maxlen=5)  # 5 entries, since interval is 2 sec -> 10 sec data
memory_data = deque(maxlen=5)
timestamps = deque(maxlen=5)

CARD_STYLE = {
    "backgroundColor": "#1e1e1e",
    "color": "#ffffff",
    "borderRadius": "10px",
    "padding": "15px",
    "boxShadow": "0px 4px 10px rgba(0,0,0,0.3)",
    "textAlign": "center"
}

app.layout = html.Div([
    html.H1("Real-Time Process Monitoring Dashboard", style={"textAlign": "center", "color": "#fff"}),

    html.Div([
        html.Div([
            dcc.Graph(id='memory-usage-graph', style={"height": "300px"}),
            html.P(id="memory-text", style={"textAlign": "center", "fontSize": "16px", "fontWeight": "bold"})
        ], style={**CARD_STYLE, "flex": "1", "minWidth": "400px"}),

        html.Div([
            dcc.Graph(id='cpu-usage-graph', style={"height": "300px"}),
            html.P(id="cpu-text", style={"textAlign": "center", "fontSize": "16px", "fontWeight": "bold"})
        ], style={**CARD_STYLE, "flex": "1", "minWidth": "400px"}),
    ], style={"display": "flex", "gap": "20px", "justifyContent": "center", "margin": "20px"}),

    html.Div(id='process-table', style={"width": "90%", "margin": "auto", "color": "#fff"}),

    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
], style={"backgroundColor": "#121212", "padding": "20px", "minHeight": "100vh"})


# Background Data Collection
def update_data():
    while True:
        timestamps.append(time.strftime("%H:%M:%S"))
        cpu_data.append(psutil.cpu_percent())
        memory_data.append(psutil.virtual_memory().percent)
        time.sleep(2)

Thread(target=update_data, daemon=True).start()


# Update Dashboard and Handle Process Killing
@app.callback(
    [Output('cpu-usage-graph', 'figure'),
     Output('memory-usage-graph', 'figure'),
     Output('cpu-text', 'children'),
     Output('memory-text', 'children'),
     Output('process-table', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input({'type': 'kill-btn', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'kill-btn', 'index': dash.dependencies.ALL}, 'id')]
)
def update_dashboard(n, n_clicks, button_ids):
    # Handle process termination
    if n_clicks and any(clicks is not None and clicks > 0 for clicks in n_clicks):
        for i, clicks in enumerate(n_clicks):
            if clicks and button_ids:
                pid_to_kill = button_ids[i]['index']
                try:
                    psutil.Process(pid_to_kill).terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass  # Process might have already been killed

    # Update Graphs
    cpu_fig = px.line(x=list(timestamps), y=list(cpu_data), labels={'x': 'Time', 'y': 'CPU Usage (%)'})
    cpu_fig.update_layout(template="plotly_dark")

    memory_fig = px.line(x=list(timestamps), y=list(memory_data), labels={'x': 'Time', 'y': 'Memory Usage (%)'})
    memory_fig.update_layout(template="plotly_dark")

    cpu_text = f"CPU Usage: {cpu_data[-1]:.2f}%"
    memory_text = f"Memory Usage: {memory_data[-1]:.2f}%"

    # Process Table
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            cpu_percent = proc.info['cpu_percent'] / NUM_CPUS
            processes.append(html.Tr([
                html.Td(proc.info['pid'], style={"padding": "8px", "border": "1px solid #666"}),
                html.Td(proc.info['name'], style={"padding": "8px", "border": "1px solid #666"}),
                html.Td(f"{cpu_percent:.2f}%", style={"padding": "8px", "border": "1px solid #666"}),
                html.Td(f"{proc.info['memory_percent']:.2f}%", style={"padding": "8px", "border": "1px solid #666"}),
                html.Td(html.Button('Kill', id={'type': 'kill-btn', 'index': proc.info['pid']}, n_clicks=0,
                                    style={"backgroundColor": "#FF4C4C", "color": "white", "border": "none",
                                           "padding": "6px 10px", "borderRadius": "5px", "cursor": "pointer"}))
            ]))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    process_table = html.Table([
        html.Thead(html.Tr([
            html.Th("PID", style={"padding": "10px", "border": "1px solid #888", "backgroundColor": "#333"}),
            html.Th("Name", style={"padding": "10px", "border": "1px solid #888", "backgroundColor": "#333"}),
            html.Th("CPU (%)", style={"padding": "10px", "border": "1px solid #888", "backgroundColor": "#333"}),
            html.Th("Memory (%)", style={"padding": "10px", "border": "1px solid #888", "backgroundColor": "#333"}),
            html.Th("Action", style={"padding": "10px", "border": "1px solid #888", "backgroundColor": "#333"})
        ])),
        html.Tbody(processes)
    ], style={"width": "100%", "borderCollapse": "collapse", "marginTop": "20px"})

    return cpu_fig, memory_fig, cpu_text, memory_text, process_table


if __name__ == "__main__":
    app.run(debug=True)


