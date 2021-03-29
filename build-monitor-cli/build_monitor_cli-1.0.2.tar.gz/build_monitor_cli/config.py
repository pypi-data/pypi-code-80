from configparser import ConfigParser

class AppConfig:
    def __init__(self, config_file_path, organization) -> None:
        super().__init__()
        self.config_file_path = config_file_path
        self.organization = organization
        self.config = ConfigParser()
        self._initialize()
    
    def _initialize(self):
        self.config.read(self.config_file_path)
        self.get_organization_config(self.organization)
    
    def get_organization_config(self, organization):
        org_config = None
        org_sections = [s for s in self.config.sections() if s.startswith('org:')]
        if organization is None:
            if not org_sections:
                raise Exception('please add organization')
            if len(org_sections) > 1:
                raise Exception('please specify organization')
            org_config = org_sections[0]
        elif f'org:{organization}' not in org_sections:
            raise Exception('can not find such organization')
        else:
            org_config = self.config[f'org:{organization}']
        return org_config


    def get_config(self, key):
        org_config = self.get_organization_config(self.organization)
        return org_config[key]
