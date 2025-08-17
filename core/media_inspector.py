import subprocess
import json

class MediaInspector:
    @staticmethod
    def probe(file_path):
        """Use ffprobe to get media file information in JSON format."""
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            f'"{file_path}"'
        ]
        command_str = " ".join(command)
        
        try:
            result = subprocess.run(command_str, shell=True, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error probing file {file_path}: {e}")
            return None
