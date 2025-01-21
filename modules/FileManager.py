import json
import modules.core as core

class FileManager:
    def __init__(self, objects: list[core.Knoten]):
        """Initializes the FileManager

        Args:
            objects (list[core.Knoten]): Every node on the graph
        """
        self.nodes = objects
        self.json = {
            'points': {}
        }
    
    def convert_to_json(
        self, 
        filename: str
    ) -> None:
        """ Converts the nodes into a .json-style format

        Args:
            filename (str): Filename
        """
        self.json['points'].clear()
        
        for i, node in enumerate(self.nodes):
            json_obj = {
                'id': node.id,
                'x': node.x(),
                'y': node.y(),
                'is_start': node.is_start,
                'is_end': node.is_end
            }
            self.json['points'][i] = json_obj
        
        with open(f"{filename}", "w") as j:
            json.dump(self.json, j)
    
    def convert_to_list(self, filename: str) -> None:
        """Converts the .json back into a list of objects

        Args:
            filename (str): Filename
        """
        with open(f"{filename}", "r") as j:
            json_nodes = json.load(j)
        
        for i, node in json_nodes['points'].items():
            new_node = core.Knoten((node['x'], node['y']))
            new_node.id = node['id']
            new_node.is_start = node['is_start']
            new_node.is_end = node['is_end']
            
            self.nodes.append(new_node)