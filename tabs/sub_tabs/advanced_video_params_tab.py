from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox

class AdvancedVideoParamsTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Color Management
        color_group = QGroupBox("色彩管理")
        color_layout = QGridLayout(color_group)

        color_layout.addWidget(QLabel("色彩范围 (-color_range):"), 0, 0)
        self.color_range_combo = QComboBox()
        self.color_range_combo.addItems(["", "tv", "pc"])
        color_layout.addWidget(self.color_range_combo, 0, 1)

        color_layout.addWidget(QLabel("色域 (-colorspace):"), 1, 0)
        self.color_space_combo = QComboBox()
        self.color_space_combo.addItems(["", "bt709", "bt2020"])
        color_layout.addWidget(self.color_space_combo, 1, 1)

        color_layout.addWidget(QLabel("传输特性 (-color_trc):"), 2, 0)
        self.color_transfer_combo = QComboBox()
        self.color_transfer_combo.addItems(["", "bt709", "smpte2084"])
        color_layout.addWidget(self.color_transfer_combo, 2, 1)

        main_layout.addWidget(color_group)

        # Filters (Denoise, Sharpen) - This is a simplified approach
        filter_group = QGroupBox("滤镜 (-vf)")
        filter_layout = QGridLayout(filter_group)

        filter_layout.addWidget(QLabel("降噪:"), 0, 0)
        self.denoise_combo = QComboBox()
        self.denoise_combo.addItems(["", "hqdn3d", "nlmeans"])
        filter_layout.addWidget(self.denoise_combo, 0, 1)

        filter_layout.addWidget(QLabel("锐化 (unsharp):"), 1, 0)
        self.sharpen_input = QLineEdit()
        self.sharpen_input.setPlaceholderText("luma_msize_x:luma_msize_y:luma_amount")
        filter_layout.addWidget(self.sharpen_input, 1, 1)

        main_layout.addWidget(filter_group)
        main_layout.addStretch()

        # Connect signals
        self.color_range_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-color_range', text))
        self.color_space_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-colorspace', text))
        self.color_transfer_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-color_trc', text))
        self.denoise_combo.currentTextChanged.connect(self.update_video_filters)
        self.sharpen_input.textChanged.connect(self.update_video_filters)

    def update_video_filters(self, _=None):
        filters = []
        denoise = self.denoise_combo.currentText()
        sharpen = self.sharpen_input.text()

        if denoise:
            filters.append(denoise)
        if sharpen:
            filters.append(f"unsharp={sharpen}")
        
        self.state_manager.set_param('-vf', ",".join(filters))
