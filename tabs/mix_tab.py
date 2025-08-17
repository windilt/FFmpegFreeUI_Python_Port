from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QFileDialog, QTableWidgetItem
from core.media_inspector import MediaInspector

class MixTab(QWidget):
    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Info Label
        info_label = QLabel("此功能为扩展，不走编码队列，直接让 ffmpeg 以原样运行。\n高级功能请移步 MKVToolNix GUI。")
        info_label.setStyleSheet("color: gray;")
        main_layout.addWidget(info_label)

        # File List Group
        list_group = QGroupBox("输入文件和流选择")
        list_layout = QVBoxLayout(list_group)

        # Action buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加文件")
        self.remove_button = QPushButton("移除所选")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()
        list_layout.addLayout(button_layout)

        # File and stream table
        self.stream_table = QTableWidget()
        self.stream_table.setColumnCount(4) # Path, Video, Audio, Subtitle
        self.stream_table.setHorizontalHeaderLabels(["文件路径", "视频流", "音频流", "字幕流"])
        self.stream_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        list_layout.addWidget(self.stream_table)

        # Stream mapping
        map_group = QGroupBox("流映射 (-map)")
        map_layout = QHBoxLayout(map_group)
        map_layout.addWidget(QLabel("视频流索引:"))
        self.video_map_input = QLineEdit("0:v:0")
        map_layout.addWidget(self.video_map_input)
        map_layout.addWidget(QLabel("音频流索引:"))
        self.audio_map_input = QLineEdit("0:a:0")
        map_layout.addWidget(self.audio_map_input)
        map_layout.addWidget(QLabel("字幕流索引:"))
        self.subtitle_map_input = QLineEdit("0:s:0")
        map_layout.addWidget(self.subtitle_map_input)
        list_layout.addWidget(map_group)

        main_layout.addWidget(list_group)

        # Output Group (Handled by main window)

        main_layout.addStretch()

        # Connect signals
        self.add_button.clicked.connect(self.add_files)
        self.remove_button.clicked.connect(self.remove_selected_file)
        self.state_manager.mix_files_changed.connect(self.update_table_from_state)
        self.video_map_input.textChanged.connect(lambda text: self.state_manager.set_param('_mix_video_map', text))
        self.audio_map_input.textChanged.connect(lambda text: self.state_manager.set_param('_mix_audio_map', text))
        self.subtitle_map_input.textChanged.connect(lambda text: self.state_manager.set_param('_mix_subtitle_map', text))

    def add_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择要混流的文件")
        if file_paths:
            for file_path in file_paths:
                probe_data = MediaInspector.probe(file_path)
                if probe_data:
                    video_streams = []
                    audio_streams = []
                    subtitle_streams = []
                    for stream in probe_data.get('streams', []):
                        if stream.get('codec_type') == 'video':
                            video_streams.append(str(stream.get('index')))
                        elif stream.get('codec_type') == 'audio':
                            audio_streams.append(str(stream.get('index')))
                        elif stream.get('codec_type') == 'subtitle':
                            subtitle_streams.append(str(stream.get('index')))
                    
                    file_info = {
                        'path': file_path,
                        'video_streams': video_streams,
                        'audio_streams': audio_streams,
                        'subtitle_streams': subtitle_streams
                    }
                    self.state_manager.add_mix_file(file_info)

    def remove_selected_file(self):
        selected_rows = sorted(set(index.row() for index in self.stream_table.selectedIndexes()), reverse=True)
        for row in selected_rows:
            self.state_manager.remove_mix_file(row)

    def update_table_from_state(self, mix_files):
        self.stream_table.setRowCount(0) # Clear existing rows
        for i, file_info in enumerate(mix_files):
            self.stream_table.insertRow(i)
            self.stream_table.setItem(i, 0, QTableWidgetItem(file_info['path']))
            self.stream_table.setItem(i, 1, QTableWidgetItem(", ".join(file_info['video_streams'])))
            self.stream_table.setItem(i, 2, QTableWidgetItem(", ".join(file_info['audio_streams'])))
            self.stream_table.setItem(i, 3, QTableWidgetItem(", ".join(file_info['subtitle_streams'])))
