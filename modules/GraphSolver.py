import math
import heapq
import modules.core as core
from PyQt5.QtGui import(
    QColor,
)
from typing import Union
from modules.QGraphicsViewManager import QGraphicsViewManager

class GraphSolver:
    def __init__(
        self, 
        start: core.Knoten, 
        end: core.Knoten, 
        points: list, 
        lines: list,
        graphicsView: QGraphicsViewManager
    ):
        """Handles solving the graph

        Args:
            start (core.Knoten): Start node
            end (core.Knoten): End node
            points (list): list of nodes
            lines (list): list of lines
            graphicsView (QGraphicsViewManager): QGraphicsView
        """
        self.start = start
        self.start_index = 0
        self.end = end
        self.end_index = 0
        self.points = points
        self.lines = lines
        self.weights = {i: {} for i in range(len(self.points))}
        self.graphicsView = graphicsView
        
        self.current_line = None
    
    def extract_end_nodes(
        self, 
        start: tuple[int, core.Knoten], 
        end: tuple[int, core.Knoten]
    ) -> None:
        """Extracts the start and end node into a node and index

        Args:
            start (tuple[int, core.Knoten]): Start node
            end (tuple[int, core.Knoten]): End node
        """
        self.start_index = start[0]
        self.end_index = end[0]
        
        self.start = start[1]
        self.end = end[1]
    
    def calculate_distance(
        self, 
        point1: core.Knoten, 
        point2: core.Knoten
    ) -> Union[int, float]:
        """Calculates the distance between two node

        Args:
            point1 (core.Knoten): First node
            point2 (core.Knoten): Second node

        Returns:
            Union[int, float]: Distance between first and second node
        """
        return round(math.sqrt(math.pow(point2.x() - point1.x(), 2) + math.pow(point2.y() - point1.y(), 2)), 4)
    
    def calculate_weights(self) -> None:
        """Calculates the weight of each edge and appends it to the weights
        """
        for i, p in enumerate(self.points):
            for neighbor in self.weights[i]['neighbors']:
                distance = self.calculate_distance(p, neighbor)
                self.weights[i]['weights'].append(distance)
    
    def set_neighbors(self):
        """Sets the neighbor nodes of each node
        """
        for i, p1 in enumerate(self.points):
            for line in self.lines:
                if line.pos1.pos[0] == p1.pos[0] and line.pos1.pos[1] == p1.pos[1]:
                    neighbor_index = self.graphicsView.find_object(line.pos2, self.points)
                    weight = self.calculate_distance(p1, line.pos2)
                    self.weights[i][neighbor_index] = weight
                
                elif line.pos2.pos[0] == p1.pos[0] and line.pos2.pos[1] == p1.pos[1]:
                    neighbor_index = self.graphicsView.find_object(line.pos1, self.points)
                    weight = self.calculate_distance(p1, line.pos1)
                    self.weights[i][neighbor_index] = weight
    
    def draw_connections(self) -> None:
        """Draw connection between each node and neighbor node
        """
        for i, p in enumerate(self.points):
            for neighbor in self.weights[i]['neighbors']:
                self.connect_points(p, neighbor, QColor(0, 255, 255, 255))
    
    def draw_net(self) -> None:
        """Connects every node with each node
        
        Was added purely for fun
        """
        for point in enumerate(self.points):
            for remaining_point in self.points:
                self.connect_points(point[1], remaining_point)
    
    def connect_points(
        self, 
        point1: core.Knoten, 
        point2: core.Knoten, 
        color: QColor = None
    ) -> None:
        """Connect two nodes with each other with a given color

        Args:
            point1 (core.Knoten): First node
            point2 (core.Knoten): Second node
            color (QColor, optional): QColor. Defaults to None.
        """
        kante = core.Kante(point1, point2, color)
        self.graphicsView.add_item(kante)
    
    def solve_graph(self) -> tuple[list, float]:
        """Creates a list of nodes containing the path from the start node
        
        until the end node.

        Returns:
            tuple[list, float]: List with the path and float with the distance in pixels
        """
        nodes_traveled = 0
        
        distances = {node: math.inf for node in self.weights} # shortest distance to each node
        predecessors = {node: None for node in self.weights} # predecessor for each node
        distances[self.start_index] = 0
        priority_queue = [(0, self.start_index)] # min-heap queue
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_node == self.end_index:
                break
            
            for neighbor, weight in self.weights[current_node].items():
                nodes_traveled += 1
                
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return self.finalize_pathing(predecessors, distances, nodes_traveled)
    
    def finalize_pathing(
        self, 
        predecessors: list, 
        distances: list,
        nodes_traveled: int
    ) -> tuple[list, float]:
        """Puts the path together and returns it

        Args:
            predecessors (list): List of predecessors
            distances (list): List of distances of nodes to each other

        Returns:
            tuple[list, float]: Path and total distance
        """
        path = []
        current = self.end_index
        
        while current is not None:
            path.append(self.points[current])
            current = predecessors[current]
        
        path.reverse()
        return (path, distances[self.end_index], nodes_traveled)