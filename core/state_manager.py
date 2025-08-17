from PyQt6.QtCore import QObject, pyqtSignal

class StateManager(QObject):
    """Manages the shared state of the application."""
    param_changed = pyqtSignal(str, str)
    input_file_changed = pyqtSignal(str)
    output_file_changed = pyqtSignal(str)
    merge_files_changed = pyqtSignal(list)
    mix_files_changed = pyqtSignal(list)
    task_queue_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._params = {}
        self._input_file = ""
        self._output_file = ""
        self._merge_files = []
        self._mix_files = [] # List of dicts: [{'path': str, 'streams': dict, 'maps': dict}]
        self._task_queue = [] # List of dicts: [{'id': int, 'type': str, 'command': str, 'input': str, 'output': str, 'status': str, 'progress': float}]
        self._next_task_id = 0

    @property
    def params(self):
        return self._params

    @property
    def input_file(self):
        return self._input_file

    @property
    def output_file(self):
        return self._output_file

    @property
    def merge_files(self):
        return self._merge_files

    @property
    def mix_files(self):
        return self._mix_files

    @property
    def task_queue(self):
        return self._task_queue

    def set_param(self, key, value):
        if value:
            self._params[key] = value
        elif key in self._params:
            del self._params[key]
        self.param_changed.emit(key, value)

    def set_input_file(self, path):
        self._input_file = path
        self.input_file_changed.emit(path)

    def set_output_file(self, path):
        self._output_file = path
        self.output_file_changed.emit(path)

    # Merge methods
    def add_merge_files(self, paths):
        self._merge_files.extend(paths)
        self.merge_files_changed.emit(self._merge_files)

    def remove_merge_file(self, index):
        if 0 <= index < len(self._merge_files):
            del self._merge_files[index]
            self.merge_files_changed.emit(self._merge_files)

    def set_merge_files(self, files):
        self._merge_files = files
        self.merge_files_changed.emit(self._merge_files)

    # Mix methods
    def add_mix_file(self, file_info):
        self._mix_files.append(file_info)
        self.mix_files_changed.emit(self._mix_files)

    def remove_mix_file(self, index):
        if 0 <= index < len(self._mix_files):
            del self._mix_files[index]
            self.mix_files_changed.emit(self._mix_files)

    # Task Queue methods
    def add_task(self, task_type, command, input_path, output_path):
        task = {
            'id': self._next_task_id,
            'type': task_type,
            'command': command,
            'input': input_path,
            'output': output_path,
            'status': 'pending',
            'progress': 0.0
        }
        self._next_task_id += 1
        self._task_queue.append(task)
        self.task_queue_changed.emit(self._task_queue)
        return task['id']

    def remove_task(self, task_id):
        self._task_queue = [task for task in self._task_queue if task['id'] != task_id]
        self.task_queue_changed.emit(self._task_queue)

    def update_task_status(self, task_id, status, progress=None):
        for task in self._task_queue:
            if task['id'] == task_id:
                task['status'] = status
                if progress is not None:
                    task['progress'] = progress
                self.task_queue_changed.emit(self._task_queue)
                return

    def get_task(self, task_id):
        for task in self._task_queue:
            if task['id'] == task_id:
                return task
        return None
