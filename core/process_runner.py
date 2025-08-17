import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class ProcessRunner(QThread):
    """Runs a shell command in a separate thread."""
    stdout_received = pyqtSignal(str)
    stderr_received = pyqtSignal(str)
    process_finished = pyqtSignal(int, int) # Changed: now emits (return_code, task_id)

    def __init__(self, command, task_id):
        super().__init__()
        self.command = command
        self.task_id = task_id # New: store task_id

    def run(self):
        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Read stdout and stderr streams
        if self.process.stdout:
            for line in iter(self.process.stdout.readline, ''):
                self.stdout_received.emit(line.strip())
            self.process.stdout.close()

        if self.process.stderr:
            for line in iter(self.process.stderr.readline, ''):
                self.stderr_received.emit(line.strip())
            self.process.stderr.close()

        self.process.wait()
        self.process_finished.emit(self.process.returncode, self.task_id) # Changed: emit task_id
