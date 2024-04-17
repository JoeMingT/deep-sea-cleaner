# To change settings
# To save progress
# To save player data or collectibles

import json as js

class Json:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_data()
    
    def load_data(self):
        try:
            with open(self.file_name, 'r') as f:
                data = f.read()
        except Exception as e:
            print(e)
            print("Error loading Data. Exiting Program")
            exit()

        return js.loads(data)

    def dump_data(self):
        try:
            with open(self.file_name, 'w') as f:
                new_data = js.dumps(self.data, indent = 4)
                f.write(new_data)
        except Exception as e:
            print(e)
            print("Error loading Data. Exiting Program")
            exit()

    def reload_data(self):
        self.data = self.load_data()