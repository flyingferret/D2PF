import xml.etree.ElementTree as ET
from PathFinderData import PathFinderSystem
import time
import json
import os


def parse_svg(region):
    # Parse the SVG file
    tree = ET.parse(f'SVG/{region}.svg')
    root = tree.getroot()
    return root


def extract_systems(root):
    # Define the namespace
    namespace = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
    pf_systems = []

    # Find the systems element in the SVG file from dotlan
    svg_systems_element = root.find('.//svg:g[@id="sysuse"]', namespaces=namespace)

    # Iterate over all systems in SVG getting ID and position to create EveSystem Object
    for s in svg_systems_element:
        id = s.get('id')[3:]
        svg_x = s.get('x')
        svg_y = s.get('y')

        eve_sys = PathFinderSystem(id)
        eve_sys.position_x = svg_x
        eve_sys.position_y = svg_y

        pf_systems.append(eve_sys)

    return pf_systems


def write_json_file(region, path_finder_systems):
    with open(f"{region}.json", "a") as f:

        map_dict = {}

        # Write the JSON structure for the configuration
        config_dict = {
            "id": 10,
            "name": region,
            "scope": {
                "id": 1
            },
            "icon": "fa-desktop",
            "type": {
                "id": 4
            },
            "created": int(time.time()),
            "updated": int(time.time())
        }
        map_dict["config"] = config_dict

        map_dict["data"] = {}
        map_dict["data"]["systems"] = []
        map_dict["data"]["connections"] = []

        for count, sys in enumerate(path_finder_systems):
            map_dict["data"]["systems"].append(sys.to_dict())

            if count == 99:  # Limiting to 100 systems for brevity
                break

        # Create a dictionary to store connections between systems
        scanned_systems_ids = []

        # Iterate through each system
        for system in path_finder_systems:
            system_id = system.id
            scanned_systems_ids.append(system_id)

            # Iterate through each stargate in the system
            for stargate in system.starGates:
                # Add the connection to the dictionary if the destination system is not already scanned
                if stargate.destinationSystemID not in scanned_systems_ids:
                    map_dict["data"]["connections"].append(stargate.to_dict())

        f.write(json.dumps(map_dict, indent=4))

def main():
    # Check if the "SVG" folder exists
    if not os.path.exists("SVG"):
        os.mkdir("SVG")

    # Prompt the user for the SVG file name
    svg_file_name = input("Please enter the name of the SVG file (without the .svg extension): ")

    # Construct the full path to the SVG file
    svg_file_path = os.path.join("SVG", f"{svg_file_name}.svg")

    # Check if the SVG file exists in the "SVG" folder
    if os.path.exists(svg_file_path):
        # Prompt the user for the name of the region
        region_name = input("Please enter the name of the region: ")

        # Perform any desired actions with the SVG file and region name here

        print(f"SVG file '{svg_file_name}.svg' for the region '{region_name}' exists.")
        print(f"Running Conversion")
        root = parse_svg(svg_file_name)
        PF_systems = extract_systems(root)
        write_json_file(region_name, PF_systems)
    else:
        print(f"SVG file '{svg_file_name}.svg' does not exist in the 'SVG' folder.")

if __name__ == "__main__":
    main()
