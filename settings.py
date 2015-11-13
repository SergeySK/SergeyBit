import xml.etree.ElementTree as Et


class AppSettings:
    """Class that works with application settings"""

    def __init__(self, settings_file):
        self.settings = {}
        self.settings_file = settings_file
        self.bCached = False

    def read_settings(self):
        if self.bCached:
            return self.settings

        tree = Et.parse(self.settings_file)
        root = tree.getroot()
        if 'settings' != root.tag:
            print('Invalid document')
            return

        settings_root = root.find('app_settings')
        self.settings['client_id'] = settings_root.find('client_id').text
        self.settings['client_key'] = settings_root.find('client_key').text
        self.settings['client_secret'] = settings_root.find('client_secret').text
        self.settings['api_version'] = settings_root.find('api_version').text
        self.settings['api_url'] = settings_root.find('api_url').text

        print('SETTINGS read:')
        print(self.settings.items())
        self.bCached = True
        return self.settings