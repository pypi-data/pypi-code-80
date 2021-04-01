class XPBoardsPlan:

    def __init__(self, user_dict):

        datasets_limit = user_dict['customer']['datasets_limit']
        datasets_count = user_dict['customer']['datasets_count']
        datasets_limit = 0 if datasets_limit == None else datasets_limit
        datasets_count = 0 if datasets_count == None else datasets_count
        self._avaiable_datasets=(datasets_limit - datasets_count)

        devices_limit = user_dict['customer']['devices_limit']
        devices_count = user_dict['customer']['devices_count']
        devices_limit = 0 if devices_limit == None else devices_limit
        devices_count = 0 if devices_count == None else devices_count
        self._avaiable_devices=(devices_limit - devices_count)


        dashboards_limit = user_dict['customer']['dashboards_limit']
        dashboards_count = user_dict['customer']['dashboards_count']
        dashboards_limit = 0 if dashboards_limit == None else dashboards_limit
        dashboards_count = 0 if dashboards_count == None else dashboards_count
        self._avaiable_dashboards=(dashboards_limit - dashboards_count)
        
        self._is_active=user_dict['customer']['is_active']

    @property
    def avaiable_datasets(self):
        return self._avaiable_datasets

    @property
    def avaiable_devices(self):
        return self._avaiable_devices

    @property
    def avaiable_dashboards(self):
        return self._avaiable_dashboards
