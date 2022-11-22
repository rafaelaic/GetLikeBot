import json

'''Import the settings from config.json file'''

class Settings:
    def __init__(self, config_path :str) -> None:
        with open(config_path) as config_file:
            settings = json.load(config_file)
        self.getlike_account = settings['getlike_account']
        self.vk_accounts = settings['vk_accounts']
        self.allowed_tasks = settings['allowed_tasks']
        self.time_between_tasks = settings['time_between_tasks']
        self.time_between_profiles= settings['time_between_profiles']

if __name__ == '__main__':
    pass