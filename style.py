import json

class Style:
    def __init__(self, json_style):
        with open(json_style) as json_file:
            data = json.load(json_file)

            self.backgrounds = data["Background"] # backgrounds["Primary"] and backgrounds["Secondary"]
            self.tokens = data["Token"]

    
