import json
import sys

class Config:
    @staticmethod
    def load_config():
        if sys.platform == "win32":
            with open('config.json') as f:
                config = json.load(f)
            return config.get('rsync_path')
        return "/usr/bin/rsync"
