from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .sub_tabs.decoding_naming_tab import DecodingNamingTab
from .sub_tabs.video_params_tab import VideoParamsTab
from .sub_tabs.audio_params_tab import AudioParamsTab
from .sub_tabs.advanced_video_params_tab import AdvancedVideoParamsTab
from .sub_tabs.custom_params_tab import CustomParamsTab
from .sub_tabs.preset_management_tab import PresetManagementTab
from core.preset_manager import PresetManager

class MainTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        self.preset_manager = PresetManager() # Instantiate PresetManager here
        layout = QVBoxLayout(self)
        
        # Create the sub-tab widget
        self.sub_tabs = QTabWidget()
        layout.addWidget(self.sub_tabs)

        # Create and add sub-tabs, passing the state manager
        self.decoding_tab = DecodingNamingTab(self.state_manager)
        self.video_params_tab = VideoParamsTab(self.state_manager)
        self.audio_params_tab = AudioParamsTab(self.state_manager)
        self.advanced_video_tab = AdvancedVideoParamsTab(self.state_manager)
        self.custom_params_tab = CustomParamsTab(self.state_manager)
        self.preset_management_tab = PresetManagementTab(self.state_manager, self.preset_manager)

        self.sub_tabs.addTab(self.decoding_tab, "解码和命名")
        self.sub_tabs.addTab(self.video_params_tab, "视频参数")
        self.sub_tabs.addTab(self.audio_params_tab, "音频参数")
        self.sub_tabs.addTab(self.advanced_video_tab, "高级视频参数")
        self.sub_tabs.addTab(self.custom_params_tab, "自定义参数")
        self.sub_tabs.addTab(self.preset_management_tab, "预设管理")
