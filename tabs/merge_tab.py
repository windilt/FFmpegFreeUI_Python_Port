from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QListWidget, QAbstractItemView, QFileDialog

class MergeTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Info Label
        info_label = QLabel("此功能为扩展，不走编码队列，直接让 ffmpeg 以原样运行。\n仅提供最基础的合并，仅复制流，要求多个参数一致；高级需求请直接用剪辑软件")
        info_label.setStyleSheet("color: gray;")
        main_layout.addWidget(info_label)

        # File List Group
        list_group = QGroupBox("要合并的文件 (可拖动排序)")
        list_layout = QVBoxLayout(list_group)

        # Action buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加文件")
        self.remove_button = QPushButton("移除")
        self.move_up_button = QPushButton("上移")
        self.move_down_button = QPushButton("下移")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.move_up_button)
        button_layout.addWidget(self.move_down_button)
        button_layout.addStretch()
        list_layout.addLayout(button_layout)

        # File list widget
        self.file_list = QListWidget()
        self.file_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.file_list.model().rowsMoved.connect(self.update_state_from_list)
        list_layout.addWidget(self.file_list)

        main_layout.addWidget(list_group)

        # Output Group (Handled by main window)

        # Connect signals
        self.add_button.clicked.connect(self.add_files)
        self.remove_button.clicked.connect(self.remove_selected_file)
        self.move_up_button.clicked.connect(self.move_file_up)
        self.move_down_button.clicked.connect(self.move_file_down)
        self.state_manager.merge_files_changed.connect(self.update_list_from_state)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择要合并的文件")
        if files:
            self.state_manager.add_merge_files(files)

    def remove_selected_file(self):
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            self.state_manager.remove_merge_file(current_row)

    def move_file_up(self):
        current_row = self.file_list.currentRow()
        if current_row > 0:
            self.file_list.insertItem(current_row - 1, self.file_list.takeItem(current_row))
            self.file_list.setCurrentRow(current_row - 1)
            self.update_state_from_list()

    def move_file_down(self):
        current_row = self.file_list.currentRow()
        if 0 <= current_row < self.file_list.count() - 1:
            self.file_list.insertItem(current_row + 1, self.file_list.takeItem(current_row))
            self.file_list.setCurrentRow(current_row + 1)
            self.update_state_from_list()

    def update_list_from_state(self, files):
        self.file_list.clear()
        self.file_list.addItems(files)

    def update_state_from_list(self):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        self.state_manager.set_merge_files(files)
