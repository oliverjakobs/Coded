import json

class JSONStyle:
    def __init__(self, path):
        with open(path) as style_sheet:
            style = json.load(style_sheet)

            self.backgrounds = style["Background"] # backgrounds["Primary"] and backgrounds["Secondary"]
            self.tokens = style["Token"]

    
