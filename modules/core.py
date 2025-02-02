from PyQt5.QtGui import(
    QColor,
)
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import(
    QGraphicsLineItem,
    QGraphicsEllipseItem
)
from typing import Union

class Knoten:
    def __init__(
        self, 
        pos: list
    ) -> None:
        """Knoten is a node on the graphicsView

        Args:
            pos (list): list of x and y position
        """
        self.id = id(self) % 1000
        
        self.graphics_item = None
        self.color = QColor(0, 0, 0, 255)
        
        self.pos = pos
        
        self.width = 10
        self.height = 10
        
        self.is_start = False
        self.is_end = False
        self._set_graphics_item()
    
    def setX(
        self, 
        x: Union[int, float]
    ) -> None:
        """Changes the x value with the given int or float

        Args:
            x (Union[int, float]): new x position
        """
        self.pos[0] = x
    
    def setY(
        self, 
        y: Union[int, float]
    ) -> None:
        """Changes the y value with the given int or float

        Args:
            y (Union[int, float]): new y position
        """
        self.pos[1] = y
    
    def setColor(
        self,
        color: QColor
    ) -> None:
        """Changes the color of the node

        Args:
            color (QColor): new color
        """
        try:
            self.color = color
            self.graphics_item.setPen(self.color)
        except:
            raise BaseException(f"Error setting color {color} for {self}")
    
    def x(self) -> Union[int, float]:
        """Returns the x position of the node

        Returns:
            Union[int, float]: x position
        """
        return self.pos[0]
    
    def y(self) -> Union[int, float]:
        """Returns the x position of the node

        Returns:
            Union[int, float]: x position
        """
        return self.pos[1]
    
    def _set_graphics_item(self) -> None:
        """Creates a QGraphicsItem for the node
        """
        self.graphics_item = QGraphicsEllipseItem(self.x(), self.y(), self.width, self.height)
        self.graphics_item.setPen(self.color)
    
    def _toggle_visited(self) -> None:
        """Toggles whether or not the node was visited
        """
        self.visited = not self.visited
    
    def __repr__(self) -> str:
        """Returns a string identifying the Knoten

        Returns:
            str: the string
        """
        return f"Knoten(id={self.id}, pos={self.pos})"


class Kante:
    def __init__(
        self, 
        pos1: Knoten, 
        pos2: Knoten, 
        color: QColor = QColor(0, 0, 0, 255)
    ) -> None:
        """Creates an Kante / edge

        Args:
            pos1 (Knoten): Node on the graph
            pos2 (Knoten): Second node on the graph
            color (QColor, optional): Color of the edge. Defaults to QColor(0, 0, 0, 255) (Black).
        """
        self.id = id(self) % 1000
        
        self.pos1 = pos1
        self.pos2 = pos2
        
        self.color = color
        self.graphics_item = None
        
        self._set_graphics_item()
    
    def _set_graphics_item(self):
        """Creates a QGraphicsItem for the edge
        """
        self.graphics_item = QGraphicsLineItem(self.pos1.x(), self.pos1.y(), self.pos2.x(), self.pos2.y())
        self.graphics_item.setPen(self.color)
    
    def __repr__(self) -> str:
        """A string for identifying the edge

        Returns:
            str: string
        """
        return f"Kante(pos1={self.pos1}, pos2={self.pos2})"