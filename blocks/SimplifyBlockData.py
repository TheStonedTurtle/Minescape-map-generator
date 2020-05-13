import json
import os


# The ./vanilla/ folder should be populated with the data from here:
# https://github.com/gentlegiantJGC/PyMCTranslate/tree/master/PyMCTranslate/json/versions/java_1_15_2/block/blockstate/to_universal/minecraft/vanilla
# This will then convert that to a more useable format for our purposes
def generate_block_data_json():
    with open("./block_data.json", "w") as f:
        data = {}
        for file in os.listdir("./vanilla/"):
            if file.endswith(".json"):
                json_data = json.load(open("./vanilla/%s" % file))
                name = None
                options = {}
                for obj in json_data:
                    func = obj['function']
                    options = obj['options']
                    if func == "new_block":
                        name = options
                    elif func == "new_properties":
                        options = options
                data[file.replace(".json", "")] = {"name": name, "options": options}
        f.write(json.dumps(data, indent=2, sort_keys=True))
        f.close()


if __name__ == "__main__":
    generate_block_data_json()
