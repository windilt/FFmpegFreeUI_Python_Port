from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel, QProgressBar
from PyQt6.QtCore import Qt

class QueueTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)

        # Control buttons
        control_layout = QHBoxLayout()
        self.start_queue_button = QPushButton("启动队列")
        self.stop_queue_button = QPushButton("停止队列")
        self.clear_completed_button = QPushButton("清除已完成")
        control_layout.addWidget(self.start_queue_button)
        control_layout.addWidget(self.stop_queue_button)
        control_layout.addWidget(self.clear_completed_button)
        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["ID", "类型", "输入文件", "输出文件", "状态/进度"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.task_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.task_table)

        main_layout.addStretch()

        # Connect signals
        self.state_manager.task_queue_changed.connect(self.update_task_table)

    def update_task_table(self, tasks):
        self.task_table.setRowCount(0) # Clear existing rows
        for i, task in enumerate(tasks):
            self.task_table.insertRow(i)
            self.task_table.setItem(i, 0, QTableWidgetItem(str(task['id'])))
            self.task_table.setItem(i, 1, QTableWidgetItem(task['type']))
            self.task_table.setItem(i, 2, QTableWidgetItem(task['input']))
            self.task_table.setItem(i, 3, QTableWidgetItem(task['output']))
            
            status_item = QTableWidgetItem(task['status'])
            if task['status'] == 'running':
                progress_bar = QProgressBar()
                progress_bar.setValue(int(task['progress'] * 100))
                self.task_table.setCellWidget(i, 4, progress_bar)
            else:
                self.task_table.setItem(i, 4, status_item)
