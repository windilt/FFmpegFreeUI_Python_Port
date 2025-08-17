from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox

class DecodingNamingTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Decoder Group
        decoder_group = QGroupBox("解码器")
        decoder_layout = QGridLayout(decoder_group)

        self.decoder_combo = QComboBox()
        self.decoder_combo.addItems(["", "auto", "cpu", "d3d11va", "d3d12va", "cuda", "amf", "qsv", "vaapi", "vulkan"])
        self.decoder_combo.setToolTip("如不设置解码器则 ffmpeg 将自行决定。")
        decoder_layout.addWidget(QLabel("解码器 (-hwaccel): "), 0, 0)
        decoder_layout.addWidget(self.decoder_combo, 0, 1)

        self.threads_input = QLineEdit()
        self.threads_input.setPlaceholderText("0")
        self.threads_input.setToolTip("指定 CPU 解码线程数，也会影响滤镜。0为自动。")
        decoder_layout.addWidget(QLabel("CPU解码线程数 (-threads): "), 1, 0)
        decoder_layout.addWidget(self.threads_input, 1, 1)

        main_layout.addWidget(decoder_group)

        # Hardware Decode Device Group
        hw_device_group = QGroupBox("硬解设备")
        hw_device_layout = QGridLayout(hw_device_group)

        self.hwaccel_device_input = QLineEdit()
        self.hwaccel_device_input.setPlaceholderText("0")
        self.hwaccel_device_input.setToolTip("NVIDIA/AMD适用，填写显卡索引号。")
        hw_device_layout.addWidget(QLabel("设备索引 (-hwaccel_device): "), 0, 0)
        hw_device_layout.addWidget(self.hwaccel_device_input, 0, 1)

        self.init_hw_device_input = QLineEdit()
        self.init_hw_device_input.setPlaceholderText("vaapi=dec:/dev/dri/card0")
        self.init_hw_device_input.setToolTip("直接指定硬件，Linux/AMD适用。")
        hw_device_layout.addWidget(QLabel("指定硬件 (-init_hw_device): "), 1, 0)
        hw_device_layout.addWidget(self.init_hw_device_input, 1, 1)

        main_layout.addWidget(hw_device_group)

        # Output Naming Group (Logic to be handled later)
        naming_group = QGroupBox("输出命名")
        naming_layout = QGridLayout(naming_group)

        self.naming_combo = QComboBox()
        self.naming_combo.addItems(["附加时间戳（默认）", "不使用（必须自定义文本）", "附加 ~1", "附加 _3fui"])
        naming_layout.addWidget(QLabel("自动命名选项:"), 0, 0)
        naming_layout.addWidget(self.naming_combo, 0, 1)

        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("输出文件强制开头")
        naming_layout.addWidget(QLabel("开头文本:"), 1, 0)
        naming_layout.addWidget(self.prefix_input, 1, 1)

        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("输出文件强制结尾")
        naming_layout.addWidget(QLabel("结尾文本:"), 2, 0)
        naming_layout.addWidget(self.suffix_input, 2, 1)

        self.no_output_checkbox = QCheckBox("不使用输出文件参数！！！")
        self.no_output_checkbox.setToolTip("新手勿用！此功能仅用于特殊场景需求，勾选后不会附加输出文件参数，常规使用必报错！")
        naming_layout.addWidget(self.no_output_checkbox, 3, 0, 1, 2)

        main_layout.addWidget(naming_group)
        main_layout.addStretch()

        # Connect signals
        self.decoder_combo.currentTextChanged.connect(lambda text: self.state_manager.set_param('-hwaccel', text))
        self.threads_input.textChanged.connect(lambda text: self.state_manager.set_param('-threads', text))
        self.hwaccel_device_input.textChanged.connect(lambda text: self.state_manager.set_param('-hwaccel_device', text))
        self.init_hw_device_input.textChanged.connect(lambda text: self.state_manager.set_param('-init_hw_device', text))
