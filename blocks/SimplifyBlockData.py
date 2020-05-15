import json
import os


# The ./vanilla/ folder should be populated with the data from here:
# https://github.com/gentlegiantJGC/PyMCTranslate/tree/master/PyMCTranslate/json/versions/java_1_15_2/block/blockstate/to_universal/minecraft/vanilla
from blocks.MinecraftBlocks import MinecraftBlocks


def generate_block_data_json():
    """
    Combine and convert all vanilla data into 1 json file
    """
    with open("./block_data.json", "w") as f:
        data = {}
        # Convert json into more useable format
        for file in os.listdir("./vanilla/"):
            if file.endswith(".json"):
                json_data = json.load(open("./vanilla/%s" % file))

                file_data = {}
                for obj in json_data:
                    func = obj['function']
                    options = obj['options']

                    if func == "new_block":
                        file_data["name"] = options
                    elif func == "new_properties":
                        file_data["options"] = options
                        if "material" in options:
                            file_data["material"] = options["material"]
                    elif func == "carry_properties":
                        file_data["carry_options"] = options
                    elif func == "walk_input_nbt" or func == "map_properties":
                        continue
                    else:
                        print("Unhandled func: %s" % func)
                data[file.replace(".json", "")] = file_data

        # Attach sprite ids
        for block in MinecraftBlocks:
            name = block[0]

            if name in data:
                data[name]["sprite_idx"] = block[1]
            else:
                print("Couldn't find block: (%s, %s)" % block)
                continue

        f.write(json.dumps(data, indent=2, sort_keys=True))
        f.close()


if __name__ == "__main__":
    generate_block_data_json()
