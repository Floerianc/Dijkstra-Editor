from PyQt5.QtWidgets import QGraphicsLineItem
from modules.QGraphicsViewManager import QGraphicsViewManager
import modules.core as core
import random

class GraphGenerator:
    def __init__(
        self, 
        max_points: int, 
        max_connections: int,
        graphicsView: QGraphicsViewManager
    ) -> None:
        """Initializes the GraphGenerator

        Args:
            max_points (int): Maxmimum amount of nodes
            max_connections (int): Maxmimum amount of connections between each individual node
            graphicsView (QGraphicsViewManager): QGraphicsViewManager
        """
        self.max_points = max_points
        self.max_connections = max_connections
        
        self.start_index = 0
        self.end_index = max_points - 1
        
        self.gv = graphicsView
        self.gv_width = graphicsView.graphicsView.width()
        self.gv_height = graphicsView.graphicsView.height()
        
        self.nodes = {i: {'node': {}, 'connections': {}} for i in range(self.max_points)}
        self.lines = []
    
    def generate_nodes(self) -> None:
        """Generates randomly placed nodes on the graph
        """
        for i in range(self.max_points):
            node = core.Knoten((random.randint(10, self.gv_width - 10), random.randint(10, self.gv_height - 10)))
            
            if i == self.start_index:
                node.is_start = True
            elif i == self.end_index:
                node.is_end = True
            self.nodes[i]['node'] = node
    
    def set_connections(self) -> None:
        """Connects each node with another random node
        
        this system utilizes the max_connections variable to ensure,
        
        that there aren't too many connections
        """
        for i, node in enumerate(self.nodes):
            connections = []
            
            for _ in range(random.randint(1, self.max_connections)):
                connect_node = random.choice(self.nodes)
                
                if not connect_node in connections:
                    connections.append(connect_node)
            
            self.nodes[i]['connections'] = connections
    
    def create_lines(self) -> None:
        """Converts every node and connected node into a list of lines 
        
        that can be drawn on the graphicsView and used to calculate
        
        the shortest route using the algorithm in .GraphSolver
        """
        for i, node in self.nodes.items():
            for connection in node['connections']:
                line = core.Kante(
                    core.Knoten((node['node'].x(), node['node'].y())),
                    core.Knoten((connection['node'].x(), connection['node'].y()))
                )
                self.lines.append(line)
    
    def insert_to_graphicsview(self) -> None:
        """Inserts each individual node into the graphicsView and then lets it draw them
        """
        for line in self.lines:
            self.gv.objects.append(line.pos1)
            self.gv.objects.append(line.pos2)
        self.gv.redraw_objects()