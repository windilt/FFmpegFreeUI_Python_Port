import os

class CommandBuilder:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def build_encoding_command(self):
        """Build the FFmpeg command string for regular encoding."""
        input_file = self.state_manager.input_file
        output_file = self.state_manager.output_file

        if not input_file or not output_file:
            return "# Error: Input or Output file not specified"

        params = self.state_manager.params.copy()
        command = ["ffmpeg"]

        start_args = params.pop('_start_args', None)
        if start_args:
            command.append(start_args)

        command.append(f'-i "{input_file}"')

        for key, value in params.items():
            if key.startswith('_'):
                continue
            command.append(f'{key} "{value}"')

        end_args = params.pop('_end_args', None)
        if end_args:
            command.append(end_args)

        command.append(f'-y "{output_file}"')
        return " ".join(command)

    def build_merge_command(self):
        """Build the FFmpeg command for merging files."""
        files = self.state_manager.merge_files
        output_file = self.state_manager.output_file

        if len(files) < 2:
            return "# Error: Please add at least two files to merge."
        if not output_file:
            return "# Error: Please specify an output file."

        # Create a temporary file list for ffmpeg's concat demuxer
        list_path = os.path.abspath("mergelist.txt")
        try:
            with open(list_path, 'w', encoding='utf-8') as f:
                for file_path in files:
                    # FFmpeg requires paths to be escaped
                    sanitized_path = file_path.replace("'", "'\\''")
                    f.write(f"file '{sanitized_path}'\n")
        except IOError as e:
            return f"# Error: Failed to write merge list file: {e}"

        command = [
            "ffmpeg",
            "-f concat",
            "-safe 0",
            f'-i "{list_path}"'
            "-c copy",
            f'-y "{output_file}"'
        ]
        return " ".join(command)

    def build_mix_command(self):
        """Build the FFmpeg command for mixing streams from multiple files."""
        mix_files = self.state_manager.mix_files
        output_file = self.state_manager.output_file

        if not mix_files:
            return "# Error: Please add at least one input file for mixing."
        if not output_file:
            return "# Error: Please specify an output file."

        command = ["ffmpeg"]

        # Add input files
        for file_info in mix_files:
            command.append(f'-i "{file_info["path"]}"')

        # Add map arguments
        video_map = self.state_manager.params.get('_mix_video_map', '')
        audio_map = self.state_manager.params.get('_mix_audio_map', '')
        subtitle_map = self.state_manager.params.get('_mix_subtitle_map', '')

        if video_map: command.append(f'-map {video_map}')
        if audio_map: command.append(f'-map {audio_map}')
        if subtitle_map: command.append(f'-map {subtitle_map}')

        command.append("-c copy") # Copy streams by default
        command.append(f'-y "{output_file}"')

        return " ".join(command)
