from modules.QGraphicsViewManager import QGraphicsViewManager
from modules.core import Knoten
import modules.utils as utils
from PyQt5.QtGui import(
    QColor, 
    QMouseEvent
)

class MoveAgent:
    def __init__(
        self, 
        QGVM: QGraphicsViewManager
    ) -> None:
        """Initializes the MoveAgent"""
        self.selected_objects = []
        self.qgvm = QGVM
    
    def select_objects(
        self, 
        cursor: QMouseEvent
    ) -> None:
        """Selects all objects on the cursor position

        Args:
            cursor (QMouseEvent): Mouse cursor
        """
        node_pos = Knoten([cursor.x(), cursor.y()])
        self.selected_objects = self.qgvm.get_all_objects_on_pos(node_pos)
    
    def highlight_selected_objects(self) -> None:
        """Highlights the selected objects
        """
        for obj in self.qgvm.objects:
            if obj in self.selected_objects:
                obj.setColor(QColor(255, 0, 0, 255))
            else:
                obj.setColor(QColor(0, 0, 0, 255))
        self.qgvm.refresh_scene()
    
    def move_selected_objects(
        self, 
        cursor: QMouseEvent
    ) -> None:
        """Moves the selected objects

        Args:
            cursor (QMouseEvent): Mouse cursor
        """
        for obj in self.selected_objects:
            obj.setX(cursor.x() - 5)
            obj.setY(cursor.y() - 5)
            
            for other_point in self.qgvm.objects:
                if utils.rectangle_collide(obj, other_point):
                    obj.setX(other_point.x())
                    obj.setY(other_point.y())
        self.qgvm.refresh_scene()