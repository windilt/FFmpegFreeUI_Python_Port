from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QTextEdit

class CustomParamsTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Note: This tab's -vf and -af will override the ones from other tabs for simplicity.
        # A more advanced implementation would merge them.

        # Custom Filters
        filter_group = QGroupBox("自定义滤镜 (将覆盖其他滤镜设置)")
        filter_layout = QGridLayout(filter_group)

        filter_layout.addWidget(QLabel("视频滤镜 (-vf): "), 0, 0)
        self.video_filter_input = QLineEdit()
        filter_layout.addWidget(self.video_filter_input, 0, 1)

        filter_layout.addWidget(QLabel("音频滤镜 (-af): "), 1, 0)
        self.audio_filter_input = QLineEdit()
        filter_layout.addWidget(self.audio_filter_input, 1, 1)

        main_layout.addWidget(filter_group)

        # Custom Arguments
        args_group = QGroupBox("自定义参数")
        args_layout = QGridLayout(args_group)

        args_layout.addWidget(QLabel("开头参数:"), 0, 0)
        self.start_args_input = QLineEdit()
        self.start_args_input.setToolTip("在 -i <input> 之前添加")
        args_layout.addWidget(self.start_args_input, 0, 1)

        args_layout.addWidget(QLabel("结尾参数:"), 1, 0)
        self.end_args_input = QLineEdit()
        self.end_args_input.setToolTip("在所有参数之后、输出文件之前添加")
        args_layout.addWidget(self.end_args_input, 1, 1)

        main_layout.addWidget(args_group)

        # Full Command Preview
        preview_group = QGroupBox("完整命令预览")
        preview_layout = QVBoxLayout(preview_group)
        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        preview_layout.addWidget(self.command_preview)
        main_layout.addWidget(preview_group)

        main_layout.addStretch()

        # Connect signals
        self.video_filter_input.textChanged.connect(lambda text: self.state_manager.set_param('-vf', text))
        self.audio_filter_input.textChanged.connect(lambda text: self.state_manager.set_param('-af', text))
        self.start_args_input.textChanged.connect(lambda text: self.state_manager.set_param('_start_args', text))
        self.end_args_input.textChanged.connect(lambda text: self.state_manager.set_param('_end_args', text))
