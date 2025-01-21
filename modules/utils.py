from modules.core import(
    Knoten
)
from typing import Union

def rectangle_collide(pos1: Union[Knoten, tuple], pos2: Union[Knoten, tuple]) -> bool:
    RECTANGLE_WIDTH = 10
    RECTANGLE_HEIGHT = 10
    
    try:
        x1, y1 = pos1.x(), pos1.y()
    except:
        x1, y1 = pos1[0], pos1[1]
    
    try:
        x2, y2 = pos2.x(), pos2.y()
    except:
        x2, y2 = pos2[0], pos2[1]
    
    if x1 < x2 + RECTANGLE_WIDTH and x1 + RECTANGLE_WIDTH > x2 and y1 < y2 + RECTANGLE_HEIGHT and y1 + RECTANGLE_HEIGHT > y2:
        return True
    
    return False