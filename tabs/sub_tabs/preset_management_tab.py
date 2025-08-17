from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QListWidget, QInputDialog, QMessageBox

class PresetManagementTab(QWidget):
    def __init__(self, state_manager, preset_manager, parent=None):
        super().__init__(parent)
        self.state_manager = state_manager
        self.preset_manager = preset_manager
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Save Preset Group
        save_group = QGroupBox("保存当前设置")
        save_layout = QHBoxLayout(save_group)
        self.save_preset_button = QPushButton("保存为新预设")
        save_layout.addWidget(self.save_preset_button)
        main_layout.addWidget(save_group)

        # Load/Manage Presets Group
        manage_group = QGroupBox("管理预设")
        manage_layout = QGridLayout(manage_group)

        manage_layout.addWidget(QLabel("现有预设:"), 0, 0)
        self.preset_list = QListWidget()
        manage_layout.addWidget(self.preset_list, 1, 0, 1, 2)

        self.load_preset_button = QPushButton("加载选中预设")
        manage_layout.addWidget(self.load_preset_button, 2, 0)

        self.delete_preset_button = QPushButton("删除选中预设")
        manage_layout.addWidget(self.delete_preset_button, 2, 1)

        main_layout.addWidget(manage_group)
        main_layout.addStretch()

        # Connect signals
        self.save_preset_button.clicked.connect(self.save_current_settings_as_preset)
        self.load_preset_button.clicked.connect(self.load_selected_preset)
        self.delete_preset_button.clicked.connect(self.delete_selected_preset)

        # Initial load of presets
        self.update_preset_list()

    def update_preset_list(self):
        self.preset_list.clear()
        presets = self.preset_manager.list_presets()
        self.preset_list.addItems(presets)

    def save_current_settings_as_preset(self):
        preset_name, ok = QInputDialog.getText(self, "保存预设", "输入预设名称:")
        if ok and preset_name:
            # Get current state parameters
            current_params = self.state_manager.params.copy()
            # Include input/output files if desired in preset
            current_params['_input_file'] = self.state_manager.input_file
            current_params['_output_file'] = self.state_manager.output_file

            if self.preset_manager.save_preset(preset_name, current_params):
                QMessageBox.information(self, "成功", f"预设 '{preset_name}' 已保存。")
                self.update_preset_list()
            else:
                QMessageBox.warning(self, "错误", f"无法保存预设 '{preset_name}'。")

    def load_selected_preset(self):
        selected_items = self.preset_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择一个要加载的预设。")
            return

        preset_name = selected_items[0].text()
        loaded_params = self.preset_manager.load_preset(preset_name)

        if loaded_params:
            # Apply loaded parameters to state manager
            # Clear existing params first to avoid conflicts
            for key in list(self.state_manager.params.keys()):
                self.state_manager.set_param(key, None)

            for key, value in loaded_params.items():
                if key == '_input_file':
                    self.state_manager.set_input_file(value)
                elif key == '_output_file':
                    self.state_manager.set_output_file(value)
                else:
                    self.state_manager.set_param(key, value)
            QMessageBox.information(self, "成功", f"预设 '{preset_name}' 已加载。")
        else:
            QMessageBox.warning(self, "错误", f"无法加载预设 '{preset_name}'。")

    def delete_selected_preset(self):
        selected_items = self.preset_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择一个要删除的预设。")
            return

        preset_name = selected_items[0].text()
        reply = QMessageBox.question(self, "确认删除", f"确定要删除预设 '{preset_name}' 吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.preset_manager.delete_preset(preset_name):
                QMessageBox.information(self, "成功", f"预设 '{preset_name}' 已删除。")
                self.update_preset_list()
            else:
                QMessageBox.warning(self, "错误", f"无法删除预设 '{preset_name}'。")
