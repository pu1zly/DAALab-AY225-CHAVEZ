"""Traveling Salesman / Shortest Path GUI

This program loads a fixed network of nodes (from the provided table) and
allows the user to visualize the graph and compute shortest paths based on
Distance, Time, or Fuel.

Usage:
    python travelingsalesman.py

Requires:
    - networkx
    - matplotlib
    - tkinter (standard library)

"""

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    import networkx as nx
except ImportError as e:
    raise SystemExit(
        "Missing dependency: networkx. Install with `pip install networkx`"
    )


# ---------------------------------------------------------------------------
# Network definition
# ---------------------------------------------------------------------------

# Each tuple is: (from_node, to_node, distance_km, time_min, fuel_liters)
# EDIT EDGE LABEL DISTANCES HERE: Modify the distance_km value (3rd element in each tuple)
EDGE_DATA = [
    ("IMUS", "BACOOR", 10, 15, 1.2),
    ("BACOOR", "DASMA", 12, 25, 1.5),
    ("DASMA", "KAWIT", 12, 25, 1.5),
    ("KAWIT", "INDANG", 12, 25, 1.2),
    ("INDANG", "SILANG", 14, 25, 1.5),
    ("SILANG", "GENTRI", 10, 25, 1.3),
    ("GENTRI", "NOVELETA", 10, 25, 1.5),
    ("NOVELETA", "IMUS", 10, 15, 1.2),
    ("BACOOR", "SILANG", 10, 25, 1.3),
    ("DASMA", "SILANG", 12, 25, 1.5),
    ("SILANG", "BACOOR", 10, 25, 1.3),
    ("NOVELETA", "BACOOR", 10, 15, 1.2),
    ("SILANG", "KAWIT", 14, 25, 1.2),
    ("IMUS", "NOVELETA", 10, 15, 1.2),
]

NODE_LABELS = sorted({x for edge in EDGE_DATA for x in (edge[0], edge[1])})

# Approximate layout positions for the nodes to make the graph visually similar to
# the expected map (reduces edge overlap and follows the roughly circular route).
NODE_POSITIONS = {
    "IMUS": (-1.3, 0.6),
    "BACOOR": (-0.6, 1.0),
    "DASMA": (0.0, 0.8),
    "KAWIT": (0.7, 0.8),
    "INDANG": (1.2, 0.2),
    "SILANG": (0.9, -0.5),
    "GENTRI": (0.0, -0.7),
    "NOVELETA": (-0.9, -0.2),
}


def build_graph() -> nx.Graph:
    """Create an undirected graph from the table data.

    The table includes bidirectional road entries (e.g., IMUS->NOVELETA and
    NOVELETA->IMUS). To avoid drawing duplicate lines, we treat the network as
    undirected and merge duplicate edges.
    
    Edits/Changes:
    - Creates and returns an undirected NetworkX graph
    - Adds all nodes from EDGE_DATA to the graph
    - Adds edges with attributes: distance, time, fuel, and label (formatted string)
    """

    G = nx.Graph()

    for (u, v, dist, time, fuel) in EDGE_DATA:
        G.add_node(u)
        G.add_node(v)

        # For undirected graphs, adding the same edge twice simply updates
        # attributes, so we don't need an explicit duplicate check.
        G.add_edge(
            u,
            v,
            distance=dist,
            time=time,
            fuel=fuel,
            # Use a multi-line label to improve readability in tightened graph views.
            label=f"{dist}km\n{time}min\n{fuel}L",
        )

    return G


def shortest_path(graph: nx.Graph, start: str, end: str, weight: str):
    """Return shortest path and aggregated values for the chosen weight.
    
    Uses Dijkstra's algorithm to find the optimal path between two nodes.
    
    Edits/Changes:
    - Validates that start and end nodes exist in the graph
    - Computes shortest path using the specified weight (distance)
    - Calculates totals for all three metrics (distance, time, fuel) along the path
    - Returns the path as a list of nodes and a dictionary of aggregated totals
    """

    if start not in graph or end not in graph:
        raise KeyError("Start or end node not in graph")

    path = nx.dijkstra_path(graph, start, end, weight=weight)
    totals = {"distance": 0.0, "time": 0.0, "fuel": 0.0}

    for a, b in zip(path, path[1:]):
        edge = graph[a][b]
        totals["distance"] += edge["distance"]
        totals["time"] += edge["time"]
        totals["fuel"] += edge["fuel"]

    return path, totals


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class TravelingSalesmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Map + Shortest Path Explorer")
        self.state('zoomed')  # Start in maximized/fullscreen windowed mode
        self.resizable(True, True)

        self.graph = build_graph()
        self._create_widgets()
        self._draw_graph()

    def _create_widgets(self):
        # Controls frame
        # Edits/Changes:
        # - Creates control panel with start/end node dropdowns
        # - Adds "Redraw Graph" and "Find Shortest Path" buttons
        # - Creates matplotlib canvas for graph visualization
        # - Creates text widget for displaying results
        control_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        control_frame.pack(side="top", fill="x")

        ttk.Label(control_frame, text="Start node:").grid(row=0, column=0, sticky="w")
        self.start_entry = ttk.Combobox(
            control_frame, values=NODE_LABELS, width=14, state="readonly"
        )
        self.start_entry.grid(row=0, column=1, padx=(4, 14))
        self.start_entry.set(NODE_LABELS[0])

        ttk.Label(control_frame, text="End node:").grid(row=0, column=2, sticky="w")
        self.end_entry = ttk.Combobox(
            control_frame, values=NODE_LABELS, width=14, state="readonly"
        )
        self.end_entry.grid(row=0, column=3, padx=(4, 14))
        self.end_entry.set(NODE_LABELS[1])

        draw_btn = ttk.Button(control_frame, text="Redraw Graph", command=self._draw_graph)
        draw_btn.grid(row=0, column=4, padx=(4, 4))

        run_btn = ttk.Button(control_frame, text="Find Shortest Path", command=self._on_run)
        run_btn.grid(row=0, column=5, padx=(4, 4))

        # Output and plot
        output_frame = ttk.Frame(self, padding=(10, 0, 10, 10))
        output_frame.pack(side="top", fill="both", expand=True)

        # Left: graph plot
        plot_panel = ttk.LabelFrame(output_frame, text="Graph View")
        plot_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.figure = Figure(figsize=(6.3, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Right: output area
        info_panel = ttk.LabelFrame(output_frame, text="Shortest Path Output")
        info_panel.pack(side="left", fill="both", expand=False)

        self.output_text = tk.Text(
            info_panel, width=40, height=24, wrap="word", state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, padx=6, pady=6)

    def _draw_graph(self, highlight_path=None):
        """Render the graph in the matplotlib figure.
        
        Edits/Changes:
        - Clears the previous graph from the canvas
        - Draws all nodes (light blue circles) with labels
        - Draws all edges (gray lines for normal, red for highlighted path)
        - Adds edge labels showing distance, time, and fuel for each edge
        - Adds a legend to distinguish shortest path from other routes
        - Refreshes the canvas to display the updated visualization
        """

        self.ax.clear()
        self.ax.axis("off")

        # Layout and draw using fixed positions to reduce overlap and match the
        # expected visual layout from the assignment screenshot.
        pos = NODE_POSITIONS

        # Draw nodes and labels
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            ax=self.ax,
            node_size=1100,
            node_color="#88ccee",
            edgecolors="#333333",
            linewidths=1.2,
        )
        nx.draw_networkx_labels(
            self.graph,
            pos,
            ax=self.ax,
            font_size=10,
            font_weight="bold",
            font_family="sans-serif",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8),
        )

        # Title with criteria information
        self.ax.set_title(
            "Node Map - Shortest Path Explorer",
            fontsize=12,
            fontweight="bold",
            pad=14,
        )

        # Draw all edges
        edge_colors = []
        edge_widths = []

        for u, v in self.graph.edges():
            if highlight_path and frozenset((u, v)) in highlight_path:
                edge_colors.append("#e41a1c")
                edge_widths.append(2.8)
            else:
                edge_colors.append("#555555")
                edge_widths.append(1.2)

        nx.draw_networkx_edges(
            self.graph,
            pos,
            ax=self.ax,
            edge_color=edge_colors,
            width=edge_widths,
            arrowsize=18,
            connectionstyle="arc3,rad=0.08",
        )

        # Edge labels (distance/time/fuel)
        # NOTE: Edit edge distances in EDGE_DATA at line ~40-53 (3rd element of each tuple)
        # The label format shows: distance_km\ntime_min\nfuel_liters
        edge_labels = {
            (u, v): self.graph[u][v]["label"] for u, v in self.graph.edges()
        }
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels,
            font_size=10,
            font_weight="bold",
            label_pos=0.42,
            rotate=False,
            ax=self.ax,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8),
        )

        # Legend for edge meaning
        from matplotlib.lines import Line2D

        legend_items = [
            Line2D(
                [0],
                [0],
                color="#e41a1c",
                lw=2.8,
                marker="",
                label="Shortest path",
            ),
            Line2D(
                [0],
                [0],
                color="#555555",
                lw=1.2,
                marker="",
                label="Other routes",
            ),
        ]
        self.ax.legend(
            handles=legend_items,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=2,
            frameon=True,
            framealpha=0.9,
            edgecolor="#444444",
        )

        self.canvas.draw_idle()

    def _on_run(self):
        # Event handler for "Find Shortest Path" button
        # Edits/Changes:
        # - Retrieves selected start and end nodes from dropdowns
        # - Validates inputs (different nodes, exists in graph)
        # - Calls shortest_path() to compute the optimal route
        # - Updates output text box with results
        # - Highlights the shortest path in red on the graph
        start = self.start_entry.get().strip().upper()
        end = self.end_entry.get().strip().upper()
        criteria = "distance"

        if start == end:
            messagebox.showinfo(
                "Info", "Start and end nodes are the same. Choose different nodes."
            )
            return

        if start not in self.graph.nodes or end not in self.graph.nodes:
            messagebox.showerror(
                "Error", "Invalid start/end node. Please select nodes from the dropdown."
            )
            return

        try:
            path, totals = shortest_path(self.graph, start, end, weight=criteria)
        except nx.NetworkXNoPath:
            messagebox.showwarning(
                "No path",
                f"No path exists between {start} and {end} in the current network.",
            )
            self._write_output("No path found.")
            self._draw_graph(highlight_path=None)
            return

        self._write_output(start, end, path, totals)
        # For an undirected graph, highlight edges without directionality.
        highlight_edges = {frozenset((a, b)) for a, b in zip(path, path[1:])}
        self._draw_graph(highlight_path=highlight_edges)

    def _write_output(self, *args):
        """Write the result into the output text box.
        
        Edits/Changes:
        - Clears previous output from text widget
        - Displays the shortest path as a sequence of nodes
        - Shows total distance, time, and fuel consumption for the route
        - Disables text box to prevent user editing
        """

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")

        if not args:
            self.output_text.insert("end", "No results yet. Click 'Find Shortest Path'.")
        else:
            start, end, path, totals = args
            self.output_text.insert(
                "end",
                f"Shortest Path from {start} to {end}:\n",
            )
            self.output_text.insert("end", f"  Path: {' -> '.join(path)}\n")
            self.output_text.insert("end", f"  Total Distance: {totals['distance']} km\n")
            self.output_text.insert("end", f"  Total Time: {totals['time']} mins\n")
            self.output_text.insert("end", f"  Total Fuel: {totals['fuel']:.2f} L\n")

        self.output_text.configure(state="disabled")


def main():
    # Entry point for the application
    # Edits/Changes:
    # - Creates root Tkinter window
    # - Initializes TravelingSalesmanApp GUI
    # - Starts the event loop to handle user interactions
    app = TravelingSalesmanApp()
    app.mainloop()


if __name__ == "__main__":
    main()
