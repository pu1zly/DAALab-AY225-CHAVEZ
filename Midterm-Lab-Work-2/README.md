# Route Optimization System

## Overview
The **Route Optimization System** is a Python GUI application that visualizes a network of locations and determines the most efficient route between two nodes.

Each location is represented as a **node**, and each route between locations is represented as an **edge** containing three attributes:

- **Distance** (kilometers)
- **Travel Time** (minutes)
- **Fuel Consumption** (liters)

The system allows users to select a starting node, destination node, and optimization criteria. It then calculates the optimal path and visually highlights the route in the network graph.

---

## Features

- Interactive **Graphical User Interface (GUI)** built with Tkinter  
- **Graph visualization** of nodes and routes  
- Edge labels showing **distance, time, and fuel consumption**  
- Shortest path highlighting on the network map  
- Optimization based on **distance, time, or fuel usage**

---

## Technologies Used

- **Python**
- **Tkinter** – for the graphical user interface
- **NetworkX** – for graph representation and pathfinding
- **Matplotlib** – for network visualization

---

## Algorithm Used

The program uses **Dijkstra's Algorithm**, a graph search algorithm that finds the shortest path between nodes in a weighted graph.

### How the Algorithm Works

1. The algorithm starts at the selected **start node**.
2. It evaluates all neighboring nodes and calculates the cumulative cost to reach them.
3. The node with the **lowest total cost** is selected and explored next.
4. This process continues until the **destination node** is reached.
5. The final path with the **lowest total weight** is returned.

The "weight" depends on the user's selected optimization criteria:

- **Distance** → shortest physical route
- **Time** → fastest travel route
- **Fuel** → most fuel-efficient route

---

## Installation

Install the required Python libraries before running the program.

```bash
pip install networkx matplotlib