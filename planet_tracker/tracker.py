import numpy as np
from skyfield.api import load
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import time

# Load planetary data
ts = load.timescale()
eph = load('de421.bsp')  # NASA JPL ephemeris data

# Define celestial bodies
bodies = {
    "Sun": eph["sun"],
    "Mercury": eph["mercury"],
    "Venus": eph["venus"],
    "Earth": eph["earth"],
    "Mars": eph["mars"],
    "Jupiter": eph["jupiter barycenter"],
    "Saturn": eph["saturn barycenter"],
    "Uranus": eph["uranus barycenter"],
    "Neptune": eph["neptune barycenter"]
}


# Function to calculate planetary positions
def get_planet_positions():
    t = ts.now()  # Current time
    earth = bodies["Earth"]

    positions = {"x": [], "y": [], "z": [], "labels": [], "colors": []}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body).apparent()
        ra, dec, distance = astrometric.radec()

        # Convert RA/DEC to Cartesian coordinates (keeping Earth at the center)
        x = distance.au * np.cos(dec.radians) * np.cos(ra.radians)
        y = distance.au * np.cos(dec.radians) * np.sin(ra.radians)
        z = distance.au * np.sin(dec.radians)

        positions["x"].append(x)
        positions["y"].append(y)
        positions["z"].append(z)
        positions["labels"].append(name)

        # Assign colors
        color_map = {
            "Sun": "gold",
            "Mercury": "gray",
            "Venus": "yellow",
            "Earth": "blue",
            "Mars": "red",
            "Jupiter": "orange",
            "Saturn": "brown",
            "Uranus": "cyan",
            "Neptune": "purple"
        }
        positions["colors"].append(color_map.get(name, "white"))

    # Ensure Earth is always at (0,0,0)
    positions["x"][positions["labels"].index("Earth")] = 0
    positions["y"][positions["labels"].index("Earth")] = 0
    positions["z"][positions["labels"].index("Earth")] = 0

    return positions


# Dash Web App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("🌍 Live 3D Planet Tracker"),
    html.P("Earth is at the center, and planets move around it in real time."),
    dcc.Graph(id='planet-graph'),
    dcc.Interval(id='interval', interval=500000, n_intervals=0)  # Refresh every 5 sec
])


@app.callback(Output('planet-graph', 'figure'), Input('interval', 'n_intervals'))
def update_graph(_):
    positions = get_planet_positions()

    fig = go.Figure()

    # Add planets as 3D scatter points
    fig.add_trace(go.Scatter3d(
        x=positions["x"], y=positions["y"], z=positions["z"],
        mode='markers+text',
        marker=dict(size=10, color=positions["colors"], opacity=0.8),
        text=positions["labels"], textposition="top center"
    ))

    # Improve visuals
    fig.update_layout(
        title="🌍 Live 3D Solar System Model",
        scene=dict(
            xaxis_title="X (AU)", yaxis_title="Y (AU)", zaxis_title="Z (AU)",
            xaxis=dict(showgrid=True), yaxis=dict(showgrid=True), zaxis=dict(showgrid=True),
            aspectmode="cube"  # Keep the proportions realistic
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig


# Run the web app
if __name__ == "__main__":
    app.run(debug=True)
