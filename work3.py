dict = {"к1": "з1", "к2": "з2", "к3": "з3", "к4": "з4", "к5": "з5", "к6": "з6", "к7": "з7", "к8": "з8", "к9": "з9", "к10": "з10"}

dict["к2"] = "нз2"
dict["к7"] = "нз7"

del dict["к3"]

dict["к4"] = None

print(dict)