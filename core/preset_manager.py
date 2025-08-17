import json
import os

class PresetManager:
    def __init__(self, preset_dir="presets"):
        self.preset_dir = preset_dir
        os.makedirs(self.preset_dir, exist_ok=True)

    def _get_preset_path(self, name):
        return os.path.join(self.preset_dir, f"{name}.json")

    def save_preset(self, name, params):
        path = self._get_preset_path(name)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(params, f, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Error saving preset {name}: {e}")
            return False

    def load_preset(self, name):
        path = self._get_preset_path(name)
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading preset {name}: {e}")
            return None

    def list_presets(self):
        presets = []
        for filename in os.listdir(self.preset_dir):
            if filename.endswith(".json"):
                presets.append(os.path.splitext(filename)[0])
        return sorted(presets)

    def delete_preset(self, name):
        path = self._get_preset_path(name)
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except OSError as e:
                print(f"Error deleting preset {name}: {e}")
                return False
        return False
