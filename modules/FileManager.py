from PyQt5.QtWidgets import(
    QListWidget, 
    QListWidgetItem
)
import json
import os
import modules.core as core
from modules.QGraphicsViewManager import QGraphicsViewManager

class FileManager:
    def __init__(self, QGVM: QGraphicsViewManager) -> None:
        """Initializes the FileManager

        Args:
            objects (list[core.Knoten]): Every node on the graph
        """
        self.qgvm = QGVM
        self.nodes = self.qgvm.objects
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
            json.dump(self.json, j, indent=4)
    
    def convert_to_list(self, filename: str) -> None:
        """Converts the .json back into a list of objects

        Args:
            filename (str): Filename
        """
        with open(f"{filename}", "r") as j:
            json_nodes = json.load(j)
        
        for i, node in json_nodes['points'].items():
            new_node = core.Knoten([node['x'], node['y']])
            new_node.id = node['id']
            new_node.is_start = node['is_start']
            new_node.is_end = node['is_end']
            
            self.nodes.append(new_node)
    
    def get_ens_files(self) -> list:
        """Returns a list of all .ens files in the current directory

        Returns:
            list: List of .ens files
        """
        ens = []
        for cdir, subdirs, files in os.walk("."):
            for file in files:
                if file.endswith(".ens"):
                    ens.append(f"{cdir}/{file}")
        return ens
    
    def load_ens_files(
        self, 
        listWidget: QListWidget
    ) -> None:
        """Loads all .ens files into the QListWidget

        Args:
            listWidget (QListWidget): QListWidget
        """
        ens_files = self.get_ens_files()
        for file in ens_files:
            listWidget.addItem(QListWidgetItem(file))
    
    def load_selected_file(
        self, 
        listWidget: QListWidget
    ) -> None:
        """Loads the selected file into the QGraphicsView

        Args:
            listWidget (QListWidget): QListWidget
        """
        self.qgvm.objects.clear()
        self.convert_to_list(listWidget.currentItem().text())
        self.qgvm.refresh_scene()