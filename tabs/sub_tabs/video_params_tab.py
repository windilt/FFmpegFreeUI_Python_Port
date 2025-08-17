from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox

class VideoParamsTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Encoder Data (Simplified for common codecs)
        self.codec_categories = {
            "H.264": ["libx264", "h264_nvenc", "h264_qsv"],
            "H.265": ["libx265", "hevc_nvenc", "hevc_qsv"],
            "AV1": ["libsvtav1", "av1_nvenc"],
            "VP9": ["libvpx-vp9"],
            "MPEG2": ["mpeg2video"],
            "Copy": ["copy"]
        }
        self.presets = {
            "libx264": ["ultrafast", "superfast", "fast", "medium", "slow", "slower", "veryslow"],
            "libx265": ["ultrafast", "superfast", "fast", "medium", "slow", "slower", "veryslow"],
            "libsvtav1": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            "h264_nvenc": ["default", "slow", "medium", "fast", "hp", "hq", "bd", "ll", "llhp", "llhq", "lossless", "losslesshp"],
            "hevc_nvenc": ["default", "slow", "medium", "fast", "hp", "hq", "bd", "ll", "llhp", "llhq", "lossless", "losslesshp"],
            "av1_nvenc": ["default", "slow", "medium", "fast", "hp", "hq", "bd", "ll", "llhp", "llhq", "lossless", "losslesshp"],
            "libvpx-vp9": ["ultrafast", "superfast", "fast", "hp", "hq", "bd", "ll", "llhp", "llhq", "lossless", "losslesshp"]
        }
        self.profiles = {
            "libx264": ["baseline", "main", "high", "high10", "high422", "high444"],
            "libx265": ["main", "main10", "main12"],
            "h264_nvenc": ["main", "high"],
            "hevc_nvenc": ["main", "main10"],
            "av1_nvenc": ["main"],
            "libvpx-vp9": ["profile0", "profile1", "profile2", "profile3"]
        }

        # Encoder Settings
        encoder_group = QGroupBox("编码器设定")
        encoder_layout = QGridLayout(encoder_group)

        encoder_layout.addWidget(QLabel("编码类别:"), 0, 0)
        self.codec_category_combo = QComboBox()
        self.codec_category_combo.addItems(self.codec_categories.keys())
        encoder_layout.addWidget(self.codec_category_combo, 0, 1)

        encoder_layout.addWidget(QLabel("具体编码 (-c:v):"), 0, 2)
        self.codec_combo = QComboBox()
        encoder_layout.addWidget(self.codec_combo, 0, 3)

        encoder_layout.addWidget(QLabel("编码预设 (-preset):"), 1, 0)
        self.preset_combo = QComboBox()
        encoder_layout.addWidget(self.preset_combo, 1, 1)

        encoder_layout.addWidget(QLabel("配置 Profile (-profile:v):"), 1, 2)
        self.profile_combo = QComboBox()
        encoder_layout.addWidget(self.profile_combo, 1, 3)

        main_layout.addWidget(encoder_group)

        # Resolution and Frame Rate
        res_fps_group = QGroupBox("分辨率和帧率")
        res_fps_layout = QGridLayout(res_fps_group)

        res_fps_layout.addWidget(QLabel("分辨率 (-s):"), 0, 0)
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["source", "1920x1080", "1280x720"])
        res_fps_layout.addWidget(self.resolution_combo, 0, 1)

        res_fps_layout.addWidget(QLabel("帧速率 (-r):"), 1, 0)
        self.framerate_combo = QComboBox()
        self.framerate_combo.addItems(["source", "24", "30", "60"])
        res_fps_layout.addWidget(self.framerate_combo, 1, 1)

        main_layout.addWidget(res_fps_group)

        # Bitrate Control
        bitrate_group = QGroupBox("比特率控制")
        bitrate_layout = QGridLayout(bitrate_group)

        bitrate_layout.addWidget(QLabel("控制方式:"), 0, 0)
        self.bitrate_mode_combo = QComboBox()
        self.bitrate_mode_combo.addItems(["CRF", "ABR", "CQP"])
        bitrate_layout.addWidget(self.bitrate_mode_combo, 0, 1)

        bitrate_layout.addWidget(QLabel("基础比特率/质量值:"), 1, 0)
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setPlaceholderText("例如: 23 (CRF) 或 4000k (ABR)")
        bitrate_layout.addWidget(self.bitrate_input, 1, 1)

        main_layout.addWidget(bitrate_group)
        main_layout.addStretch()

        # Connect signals
        self.codec_category_combo.currentTextChanged.connect(self.update_codec_combo)
        self.codec_combo.currentTextChanged.connect(self.update_preset_profile_combos)
        self.codec_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-c:v', text))
        self.preset_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-preset', text))
        self.profile_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-profile:v', text))
        self.framerate_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-r', text) if text != "source" else self.state_manager.set_param('-r', None))
        self.resolution_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-s', text) if text != "source" else self.state_manager.set_param('-s', None))
        self.bitrate_input.textChanged.connect(self.update_bitrate_param)
        self.bitrate_mode_combo.currentTextChanged.connect(self.update_bitrate_param)

        # Initial population
        self.update_codec_combo(self.codec_category_combo.currentText())

    def update_codec_combo(self, category):
        self.codec_combo.clear()
        if category in self.codec_categories:
            self.codec_combo.addItems(self.codec_categories[category])

    def update_preset_profile_combos(self, codec):
        self.preset_combo.clear()
        self.profile_combo.clear()

        if codec in self.presets:
            self.preset_combo.addItems(self.presets[codec])
        if codec in self.profiles:
            self.profile_combo.addItems(self.profiles[codec])

    def update_bitrate_param(self, _=None):
        mode = self.bitrate_mode_combo.currentText()
        value = self.bitrate_input.text()
        # Clear old bitrate params
        self.state_manager.set_param('-crf', None)
        self.state_manager.set_param('-b:v', None)
        self.state_manager.set_param('-qp', None)

        if mode == "CRF":
            self.state_manager.set_param('-crf', value)
        elif mode == "ABR":
            self.state_manager.set_param('-b:v', value)
        elif mode == "CQP":
            self.state_manager.set_param('-qp', value)