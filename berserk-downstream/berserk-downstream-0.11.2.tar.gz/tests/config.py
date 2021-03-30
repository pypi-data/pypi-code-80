API_KEYS = {
    "DISCORD_TOKEN": 'Nzg0NTE0NzA0NDA4MDUxNzMz.X8qaQQ.CSCqskFQmf1zdQWVQxgq-Ek9NjI',
    "ADMIN_LICHESS_TOKEN": 'wzcigIznavpHCRM1'
}

"""STEPS FOR REUPLOADING TO PYPI
    1. PUSH TO GITHUB
    2. DELETE DIST FOLDER
    3. setup.py sdist bdist_wheel
    4. python -m twine upload dist/*
    5. Enter username
    6. Enter password
    7. Profit
"""
