from PyQt5.QtWidgets import(
    QGraphicsScene,
    QGraphicsView,
)
from PyQt5.QtGui import QMouseEvent
from typing import Union
import modules.core as core
import modules.utils as utils
import random

class QGraphicsViewManager:
    def __init__(
        self, 
        graphicsView: QGraphicsView
    ) -> None:
        """Initializes QGraphicsViewManager

        Args:
            graphicsView (QGraphicsView): GraphicsView object
        """
        self.objects = []
        self.lines = []
        self.graphicsView = graphicsView
        
        self.scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(self.graphicsView.x(), self.graphicsView.y(), self.graphicsView.width(), self.graphicsView.height())
    
    def add_point(
        self, 
        event: QMouseEvent
    ) -> None:
        """Adds a node to the graphicsView

        Args:
            event (QMouseEvent): Mouse cursor
        """
        point = core.Knoten([event.x() - 5, event.y() - 5])
        
        for other_point in self.objects:
            if utils.rectangle_collide(point, other_point):
                point.setX(other_point.x())
                point.setY(other_point.y())
                point._set_graphics_item()
        
        self.objects.append(point)
        self.redraw_objects()
    
    def add_item(
        self, 
        obj: Union[core.Knoten, core.Kante]
    ) -> None:
        """Adds item to the scene

        Args:
            obj (Union[core.Knoten, core.Kante]): Knoten or Kante / Edge or Node
        """
        self.scene.addItem(obj.graphics_item)
    
    def erase_lines(self) -> None:
        """Erases all lines from the scene
        """
        for line in self.lines: self.scene.removeItem(line.graphics_item)
    
    def get_lines(self) -> list:
        """Returns a list of edges

        Returns:
            list: List of edges
        """
        lines = []
        
        for i, obj in enumerate(self.objects):
            if i > 0:
                line = core.Kante(
                    core.Knoten([obj.x(), obj.y()]),
                    core.Knoten([self.objects[i - 1].x(), self.objects[i - 1].y()])
                )
                lines.append(line)
        return lines
    
    def get_clicked_object(
        self, 
        event: QMouseEvent
    ) -> Union[bool, core.Knoten, core.Kante]:
        """Returns the object you clicked on

        Args:
            event (QMouseEvent): Mouse cursor

        Returns:
            Union[bool, core.Knoten, core.Kante]: False if no object found. Else either Knoten or Kante
        """
        for obj in self.objects:
            if utils.rectangle_collide((event.x(), event.y()), obj):
                return obj
        
        return False
    
    def get_all_objects_on_pos(self, pos: core.Knoten) -> list:
        """Returns all objects on a position

        Args:
            pos (core.Knoten): Position

        Returns:
            list: List of objects
        """
        objects = []
        
        for obj in self.objects:
            if utils.rectangle_collide(pos, obj.pos):
                objects.append(obj)
        return objects
    
    def find_object(
        self, 
        pos: core.Knoten, 
        points: list[core.Knoten]
    ) -> int:
        """Returns index of node in a list of nodes

        Args:
            pos (core.Knoten): node
            points (list[core.Knoten]): list of nodes

        Returns:
            int: Index
        """
        for i, point in enumerate(points):
            if pos.pos[0] == point.pos[0] and pos.pos[1] == point.pos[1]:
                return i
    
    def refresh_scene(
        self,
    ) -> None:
        """Refreshes the scene

        Args:
            event (QMouseEvent): Mouse event. Not used.
        """
        self.scene.clear()
        self.refresh_objects()
        self.redraw_objects()
    
    def refresh_objects(self) -> None:
        """Refreshes the graphics_item of each object in self.objects
        """
        for obj in self.objects: obj._set_graphics_item()
    
    def redraw_objects(self) -> None:
        """Redraws every object in lines and objects
        """
        self.lines = self.get_lines()
        
        for line in self.lines:
            if not line.graphics_item.scene() == self.scene:
                self.scene.addItem(line.graphics_item)
        
        for obj in self.objects:
            if not obj.graphics_item.scene() == self.scene:
                self.scene.addItem(obj.graphics_item)