import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit, QLabel, QTextEdit, QGroupBox, QGridLayout
from PyQt6.QtGui import QColor

# Import core components
from core.state_manager import StateManager
from core.command_builder import CommandBuilder
from core.process_runner import ProcessRunner
from core.queue_processor import QueueProcessor # New import

# Import tab widgets
from tabs.main_tab import MainTab
from tabs.merge_tab import MergeTab
from tabs.mix_tab import MixTab
from tabs.queue_tab import QueueTab # New import

class FFmpegFreeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FFmpegFreeUI - Python Edition')
        self.setGeometry(100, 100, 1200, 800)
        self.process_runner = None

        # Core components
        self.state_manager = StateManager()
        self.command_builder = CommandBuilder(self.state_manager)
        self.queue_processor = QueueProcessor(self.state_manager) # New
        self.queue_processor.start() # Start the queue processor thread

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Input/Output Path Selection
        self.setup_io_widgets(main_layout)

        # Create Tab Widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create tabs and pass state manager
        self.main_tab = MainTab(self.state_manager)
        self.merge_tab = MergeTab(self.state_manager)
        self.mix_tab = MixTab(self.state_manager)
        self.queue_tab = QueueTab(self.state_manager) # New

        # Add tabs
        self.tabs.addTab(self.main_tab, "常规")
        self.tabs.addTab(self.merge_tab, "合并")
        self.tabs.addTab(self.mix_tab, "混流")
        self.tabs.addTab(self.queue_tab, "任务队列") # New

        # Log output
        log_group = QGroupBox("FFmpeg 日志")
        log_layout = QVBoxLayout(log_group)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        main_layout.addWidget(log_group)

        # Connect signals
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.state_manager.param_changed.connect(self.update_command_preview)
        self.state_manager.input_file_changed.connect(self.update_command_preview_no_args)
        self.state_manager.output_file_changed.connect(self.update_command_preview_no_args)

        # Connect queue processor signals to log output
        self.queue_processor.stdout_received.connect(self.log_output.append)
        self.queue_processor.stderr_received.connect(self.append_error_log)
        self.queue_processor.task_status_updated.connect(self.on_task_status_updated)

        self.show()
        self.on_tab_changed(0) # Set initial state

    def setup_io_widgets(self, layout):
        io_group = QGroupBox("文件和控制")
        io_layout = QGridLayout(io_group)
        layout.addWidget(io_group)

        # Input
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("输入文件路径 (常规模式使用)")
        self.input_path_edit.textChanged.connect(self.state_manager.set_input_file)
        browse_input_button = QPushButton("浏览")
        browse_input_button.clicked.connect(self.browse_input_file)
        io_layout.addWidget(QLabel("输入文件:"), 0, 0)
        io_layout.addWidget(self.input_path_edit, 0, 1)
        io_layout.addWidget(browse_input_button, 0, 2)

        # Output
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("输出文件路径 (所有模式使用)")
        self.output_path_edit.textChanged.connect(self.state_manager.set_output_file)
        browse_output_button = QPushButton("浏览")
        browse_output_button.clicked.connect(self.browse_output_file)
        io_layout.addWidget(QLabel("输出文件:"), 1, 0)
        io_layout.addWidget(self.output_path_edit, 1, 1)
        io_layout.addWidget(browse_output_button, 1, 2)

        # Control Button
        self.start_button = QPushButton()
        self.start_button.clicked.connect(self.add_current_task_to_queue) # Changed
        io_layout.addWidget(self.start_button, 0, 3, 2, 1)

    def on_tab_changed(self, index):
        self.update_command_preview()
        if index == 0:
            self.start_button.setText("添加到队列 (编码)")
            self.input_path_edit.setEnabled(True)
        elif index == 1:
            self.start_button.setText("添加到队列 (合并)")
            self.input_path_edit.setEnabled(False)
        elif index == 2:
            self.start_button.setText("添加到队列 (混流)")
            self.input_path_edit.setEnabled(False)
        elif index == 3:
            self.start_button.setText("管理队列") # Queue tab
            self.input_path_edit.setEnabled(False)

    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择输入文件")
        if file_path:
            self.input_path_edit.setText(file_path)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择输出文件")
        if file_path:
            self.output_path_edit.setText(file_path)

    def add_current_task_to_queue(self):
        command = ""
        task_type = ""
        current_tab = self.tabs.currentIndex()

        if current_tab == 0: # Regular Encoding
            command = self.command_builder.build_encoding_command()
            task_type = "编码"
        elif current_tab == 1: # Merge
            command = self.command_builder.build_merge_command()
            task_type = "合并"
        elif current_tab == 2: # Mix
            command = self.command_builder.build_mix_command()
            task_type = "混流"
        elif current_tab == 3: # Queue tab, do nothing or special action
            return

        self.log_output.append(f"> {command}\n")
        if command.startswith("# Error"):
            return

        task_id = self.state_manager.add_task(task_type, command, self.state_manager.input_file, self.state_manager.output_file)
        self.log_output.append(f"任务 {task_id} ({task_type}) 已添加到队列。\n")

    def on_task_status_updated(self, task_id, status, message=None):
        task = self.state_manager.get_task(task_id)
        if task:
            self.log_output.append(f"任务 {task_id} ({task['type']}) 状态: {status}")
            if message: self.log_output.append(message)
            self.log_output.append("\n")

    def append_error_log(self, text):
        self.log_output.setTextColor(QColor("red"))
        self.log_output.append(text)
        self.log_output.setTextColor(QColor("white"))

    def update_command_preview(self, _=None, __=None):
        custom_tab = self.main_tab.custom_params_tab
        if self.tabs.currentIndex() == 0:
            command = self.command_builder.build_encoding_command()
            custom_tab.command_preview.setText(command)
        else:
            custom_tab.command_preview.clear()

    def update_command_preview_no_args(self, val):
        self.update_command_preview()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = FFmpegFreeUI()
    sys.exit(app.exec())