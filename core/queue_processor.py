from PyQt6.QtCore import QThread, pyqtSignal, QMutex
import time
from core.process_runner import ProcessRunner

class QueueProcessor(QThread):
    stdout_received = pyqtSignal(str)
    stderr_received = pyqtSignal(str)
    task_status_updated = pyqtSignal(int, str, str) # task_id, status, message

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.running = False
        self.current_process_runner = None
        self.mutex = QMutex()

    def run(self):
        self.running = True
        while self.running:
            self.mutex.lock()
            pending_tasks = [task for task in self.state_manager.task_queue if task['status'] == 'pending']
            self.mutex.unlock()

            if pending_tasks:
                current_task = pending_tasks[0]
                task_id = current_task['id']

                self.state_manager.update_task_status(task_id, 'running')
                self.task_status_updated.emit(task_id, 'running', f"开始执行任务: {current_task['output']}")

                self.current_process_runner = ProcessRunner(current_task['command'], task_id) # Changed: pass task_id
                self.current_process_runner.stdout_received.connect(self.stdout_received)
                self.current_process_runner.stderr_received.connect(self.stderr_received)
                self.current_process_runner.process_finished.connect(self.on_process_finished) # Changed: on_process_finished now receives task_id
                
                self.current_process_runner.start()
                self.current_process_runner.wait() # Wait for the process to finish

            else:
                time.sleep(1) # Wait a bit if no tasks

    def on_process_finished(self, return_code, task_id): # Changed: now receives task_id
        # Disconnect signals to prevent multiple connections
        try:
            self.current_process_runner.stdout_received.disconnect(self.stdout_received)
            self.current_process_runner.stderr_received.disconnect(self.stderr_received)
            self.current_process_runner.process_finished.disconnect(self.on_process_finished)
        except TypeError: # Signal already disconnected
            pass

        if return_code == 0:
            self.state_manager.update_task_status(task_id, 'completed', "任务完成")
            self.task_status_updated.emit(task_id, 'completed', "任务完成")
        else:
            self.state_manager.update_task_status(task_id, 'failed', f"任务失败，返回代码: {return_code}")
            self.task_status_updated.emit(task_id, 'failed', f"任务失败，返回代码: {return_code}")
        
        self.current_process_runner = None

    def stop(self):
        self.running = False
        if self.current_process_runner and self.current_process_runner.isRunning():
            self.current_process_runner.terminate() # Terminate current process
            self.current_process_runner.wait() # Wait for it to finish
        self.wait() # Wait for the thread to finish
