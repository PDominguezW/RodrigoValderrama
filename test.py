# Open dealernet.json

import json

with open('dealernet.json') as json_file:
    data = json.load(json_file)

print(list(data["empresa"]["AL DIA E IMPAGOS <30 DIAS"].keys()))