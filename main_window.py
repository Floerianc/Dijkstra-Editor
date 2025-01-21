import sys
import random
import modules.core as core
import modules.GraphSolver as gs
import modules.QGraphicsViewManager as Q_GVM
import modules.FileManager as fm
import modules.GraphGenerator as gg
import PyQt5.QtWidgets as QtWidgets
from typing import Union
import time
from PyQt5.QtGui import(
    QMouseEvent, 
    QColor
)
from PyQt5.QtWidgets import(
    QGraphicsScene,
    QCheckBox,
    QSpinBox,
    QFileDialog
)
from ui.editor_ui import *

class Editor(Ui_MainWindow):
    def __init__(
        self, 
        Form
    ) -> None:
        """Initializes the window and connects the functions

        Args:
            Form (_type_): Window UI
        """
        super().__init__()
        self.setupUi(Form)
        
        self.QGVM = Q_GVM.QGraphicsViewManager(self.graphicsView)
        self.file_manager = fm.FileManager(self.QGVM.objects)
        self.selected_object = None
        self.status = 0
        
        self.max_nodes = 25
        self.max_connections = 3
        
        self.connect_functions()
        self.set_defaults()
    
    def connect_functions(self) -> None:
        """Gives each button its function
        """
        self.centralwidget.mouseMoveEvent = self.refresh_scene
        self.graphicsView.mouseMoveEvent = self.mouseMoveEvent
        self.graphicsView.mousePressEvent = self.click_handler
        
        self.pointButton.clicked.connect(lambda: self.change_status(0))
        self.selectionButton.clicked.connect(lambda: self.change_status(1))
        
        self.startCheck.clicked.connect(lambda: self.change_point_status(self.startCheck))
        self.endCheck.clicked.connect(lambda: self.change_point_status(self.endCheck))
        
        self.clearButton.clicked.connect(self.clear_all)
        self.startButton.clicked.connect(self.initialize_solution)
        self.generateButton.clicked.connect(self.generate_graph)
        
        self.maxNodeSpin.valueChanged.connect(lambda: self.change_generator_config(self.maxNodeSpin))
        self.maxConSpin.valueChanged.connect(lambda: self.change_generator_config(self.maxConSpin))
        
        self.saveAction.triggered.connect(self.save_file)
        self.openAction.triggered.connect(self.open_file)
    
    def set_defaults(self) -> None:
        """Sets the default values for a lot of widgets and variables that are likely to change
        """
        self.debugLabel.setText("0 | 0")
        self.status = 0
        self.statusLabel.setText("Drawing Nodes")
        
        self.selectionFrame.setVisible(False)
        
        self.maxNodeSpin.setValue(self.max_nodes)
        self.maxConSpin.setValue(self.max_connections)
    
    
    def save_file(self) -> None:
        """Lets the user save the currently drawn nodes and lines
        
        in a file.
        """
        filename = QFileDialog().getSaveFileName(
            directory =".\\", 
            filter = "Editor node system (*.ens)" # editor node system
        )
        self.file_manager.convert_to_json(filename[0])
    
    def open_file(self) -> None:
        """Lets the user open a file containing nodes and lines
        """
        self.QGVM.objects.clear()
        
        filename = QFileDialog().getOpenFileName(
            directory = ".\\",
            filter = "Editor node system (*.ens)"
        )
        self.file_manager.convert_to_list(filename[0])
        self.QGVM.redraw_objects()
    
    def mouseMoveEvent(
        self, 
        event: QMouseEvent
    ) -> None:
        """Refreshes selection and sets text on debug label

        Args:
            event (QMouseEvent): Mouse position / event
        """
        self.refresh_selection()
        self.debugLabel.setText(f"{event.x()} | {event.y()}")
    
    def click_handler(
        self, 
        event: QMouseEvent
    ) -> None:
        """Handles which function should be called when clicking

        Args:
            event (QMouseEvent): Mouse click
        """
        if self.status == 0:
            self.selected_object = None
            self.QGVM.add_point(event)
        
        elif self.status == 1:
            obj = self.QGVM.get_clicked_object(event)
            
            if obj:
                self.selected_object = obj
                self.show_properties(obj)
        
        self.refresh_selection()
    
    def clear_all(self) -> None:
        """Clears everything
        """
        self.selected_object = None
        self.QGVM.scene.clear()
        self.QGVM.objects.clear()
    
    def show_properties(
        self, 
        obj: core.Knoten
    ) -> None:
        """Shows properties of selected node

        Args:
            obj (core.Knoten): Node
        """
        self.load_properties(obj)
        self.nameLabel.setText(str(obj.id))
    
    def load_properties(
        self, 
        obj: core.Knoten
    ) -> None:
        """Loads properties of selected node

        Args:
            obj (core.Knoten): Node
        """
        self.startCheck.setChecked(obj.is_start)
        self.endCheck.setChecked(obj.is_end)
    
    def refresh_selection(self) -> None:
        """Refreshes the selection frame
        """
        if self.selected_object is None:
            self.selectionFrame.setVisible(False)
        else:
            self.selectionFrame.setVisible(True)
    
    def change_status(
        self, 
        status: int
    ) -> None:
        """Changes status code and label

        Args:
            status (int): status change
        """
        self.status = status
        
        if self.status == 0:
            self.statusLabel.setText("Drawing nodes")
        
        elif self.status == 1:
            self.statusLabel.setText("Selecting nodes")
    
    def refresh_scene(
        self, 
        event: QMouseEvent
    ) -> None:
        """Refreshes the scene

        Args:
            event (QMouseEvent): Mouse event. Not used.
        """
        self.QGVM.scene.clear()
        self.QGVM.refresh_objects()
        self.QGVM.redraw_objects()
    
    def change_point_status(
        self, 
        checkBox: QCheckBox
    ) -> None:
        """Changes the property of the node given which checkBox was (un)checked.

        Args:
            checkBox (QCheckBox): Clicked checkBox
        """
        if checkBox == self.startCheck:
            self.selected_object.is_start = self.startCheck.isChecked()
            
            if self.selected_object.is_start:
                self.selected_object.color = QColor(0, 255, 0, 255)
            else:
                self.selected_object.color = QColor(0, 0, 0, 255)
        
        elif checkBox == self.endCheck:
            self.selected_object.is_end = self.endCheck.isChecked()
            
            if self.selected_object.is_end:
                self.selected_object.color = QColor(255, 0, 0, 255)
            else:
                self.selected_object.color = QColor(0, 0, 0, 255)
        
        self.refresh_scene(None)
    
    def _set_start_end(self) -> Union[int, core.Knoten, None, None]:
        """Sets the start and end node and returns them including their index in the nodes list

        Returns:
            Union[(int, core.Knoten), (None, None)]: Either returns the index and node or None
        """
        for i, node in enumerate(self.QGVM.objects):
            if node.is_start:
                start = (i, node)
            
            elif node.is_end:
                end = (i, node)
        
        try:
            start, end
        except:
            self.statusLabel.setText("Start or End node is not defined!")
            return (None, None)
        return (start, end)
    
    def initialize_solution(self) -> None:
        """Initializes the pathfinding
        """
        self.refresh_scene(None)
        start, end = self._set_start_end()
        
        if start and end:
            graph_solver = gs.GraphSolver(
                start = start, 
                end = end, 
                points = self.QGVM.objects,
                lines = self.QGVM.lines,
                graphicsView = self.QGVM
            )
            graph_solver.extract_end_nodes(start, end)
            graph_solver.set_neighbors()
            self.finalize_solution(graph_solver)
    
    def finalize_solution(
        self, 
        gs: gs.GraphSolver
    ) -> None:
        """Finalizes the path finding

        Args:
            gs (gs.GraphSolver): GraphSolver
        """
        timestamp_start = time.time()
        path, distance, nodes_traveled = gs.solve_graph()
        timestamp_end = time.time()
        
        for i in range(len(path)):
            if i > 0:
                gs.connect_points(path[i - 1], path[i], QColor(255, 0, 128, 255))
        
        self.statusLabel.setText(f"Total distance: {round(distance, 2)}px.\tTime: {timestamp_end - timestamp_start}s\nNodes traveled: {nodes_traveled}")
    
    def change_generator_config(
        self, 
        widget: QSpinBox
    ) -> None:
        """Changes the configuration for the .GraphGenerator

        Args:
            widget (QSpinBox): The Spinbox whose value has been changed
        """
        if widget == self.maxNodeSpin:
            self.max_nodes = self.maxNodeSpin.value()
        
        elif widget == self.maxConSpin:
            self.max_connections = self.maxConSpin.value()
    
    def generate_graph(self) -> None:
        """Generates a random graph utilizing the GraphGenerator
        """
        self.clear_all()
        graph_gen = gg.GraphGenerator(
            random.randint(10, self.max_nodes),
            random.randint(1, self.max_connections),
            self.QGVM
        )
        graph_gen.generate_nodes()
        graph_gen.set_connections()
        graph_gen.create_lines()
        graph_gen.insert_to_graphicsview()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    
    ui = Editor(Form)
    Form.show()
    sys.exit(app.exec_())