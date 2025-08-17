from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox

class AudioParamsTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Audio Codec
        codec_group = QGroupBox("音频编码器")
        codec_layout = QGridLayout(codec_group)

        codec_layout.addWidget(QLabel("音频编码器 (-c:a):"), 0, 0)
        self.codec_combo = QComboBox()
        self.codec_combo.addItems(["copy", "aac", "ac3", "opus", "flac"])
        codec_layout.addWidget(self.codec_combo, 0, 1)

        main_layout.addWidget(codec_group)

        # Bitrate
        bitrate_group = QGroupBox("比特率")
        bitrate_layout = QGridLayout(bitrate_group)

        bitrate_layout.addWidget(QLabel("控制方式:"), 0, 0)
        self.bitrate_mode_combo = QComboBox()
        self.bitrate_mode_combo.addItems(["VBR", "CBR"])
        bitrate_layout.addWidget(self.bitrate_mode_combo, 0, 1)

        bitrate_layout.addWidget(QLabel("比特率/质量值:"), 1, 0)
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setPlaceholderText("例如: 192k (CBR) or 5 (VBR)")
        bitrate_layout.addWidget(self.bitrate_input, 1, 1)

        main_layout.addWidget(bitrate_group)

        # Channel and Sample Rate
        channel_group = QGroupBox("声道和采样率")
        channel_layout = QGridLayout(channel_group)

        channel_layout.addWidget(QLabel("声道布局 (-ac):"), 0, 0)
        self.channel_combo = QComboBox()
        self.channel_combo.addItems(["source", "1", "2", "6"])
        self.channel_combo.setItemText(0, "原版")
        self.channel_combo.setItemText(1, "Mono")
        self.channel_combo.setItemText(2, "Stereo")
        self.channel_combo.setItemText(3, "5.1")
        channel_layout.addWidget(self.channel_combo, 0, 1)

        channel_layout.addWidget(QLabel("采样率 (-ar):"), 1, 0)
        self.samplerate_combo = QComboBox()
        self.samplerate_combo.addItems(["source", "22050", "44100", "48000"])
        channel_layout.addWidget(self.samplerate_combo, 1, 1)

        main_layout.addWidget(channel_group)
        main_layout.addStretch()

        # Connect signals
        self.codec_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-c:a', text))
        self.channel_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-ac', text) if text != "source" else self.state_manager.set_param('-ac', None))
        self.samplerate_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-ar', text) if text != "source" else self.state_manager.set_param('-ar', None))
        self.bitrate_input.textChanged.connect(self.update_bitrate_param)
        self.bitrate_mode_combo.currentTextChanged.connect(self.update_bitrate_param)

    def update_bitrate_param(self, _=None):
        mode = self.bitrate_mode_combo.currentText()
        value = self.bitrate_input.text()
        # Clear old bitrate params
        self.state_manager.set_param('-q:a', None)
        self.state_manager.set_param('-b:a', None)

        if self.codec_combo.currentText() == "copy": return

        if mode == "VBR":
            self.state_manager.set_param('-q:a', value)
        elif mode == "CBR":
            self.state_manager.set_param('-b:a', value)
