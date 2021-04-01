import os
url_db_pre = 'https://docs.google.com/spreadsheets/d/e/2PACX-' \
             '1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB' \
             '-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single' \
             '=true&output=csv'

path_target = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",
                           "data", "bicycle_db.csv")

url_vis = ['https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H19070220_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20042632_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20042633_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20042634_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20042635_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20063161_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20063162_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_XTH19101158_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20063163_archive.json',
           'https://data.montpellier3m.fr/sites/default/files/ressources/'
           'MMM_EcoCompt_X2H20063164_archive.json']

C_names = ['Beracasa', 'Laverune', 'Celleneuve', 'Lattes 2', 'Lattes 1',
           'Vieille-Poste', 'Gerhardt', 'Albert 1er', 'Delmas 1', 'Delmas 2']
