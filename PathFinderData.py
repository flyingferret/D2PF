import requests
import json
import time

base_url = "https://esi.evetech.net/latest"
y_scale = 1.2
x_scale = 1.2


class PathFinderSystem:
    def __init__(self, id):
        self.populate_from_esi(id)

    def __str__(self):
        return f"System(id={self.id}, name='{self.name}')"

    def to_dict(self):
        system_dict = {
            "id": self.id,
            "updated": {"updated": self.updated},
            "systemId": self.systemId,
            "name": self.name,
            "alias": self.alias,
            "type": {"id": self.type_id},
            "security": self.security,
            "trueSec": self.trueSec,
            "region": {"id": self.region_id, "name": self.region_name},
            "constellation": {"id": self.constellation_id, "name": self.constellation_name},
            "status": {"id": self.status_id},
            "locked": self.locked,
            "rallyUpdated": self.rallyUpdated,
            "rallyPoke": self.rallyPoke,
            "currentUser": self.currentUser,
            "planets": self.planets,
            "shattered": self.shattered,
            "drifter": self.drifter,
            "userCount": self.userCount,
            "position": {"x": int(float(self.position_x) * x_scale), "y": int(float(self.position_y) * y_scale)},
            "sovereignty": {
                "faction": {"id": self.sovereignty_faction_id, "name": self.sovereignty_faction_name}
            }
        }
        return system_dict

    def populate_from_esi(self, system_id):

        # Make a request to ESI to get system information by name
        response = requests.get(f"{base_url}/universe/systems/{system_id}/",
                                params={"datasource": "tranquility", "search": system_id})
        # print(response.json())
        if response.status_code == 200:
            system_data = response.json()

            if system_data:
                #                system_data = system_data[0]  # Take the first result

                # Populate the object attributes from ESI data
                self.id = system_data.get("system_id")
                self.systemId = system_data.get("system_id")
                self.name = system_data.get("name")
                self.region_id = system_data.get("region_id")
                self.security = system_data.get("security_class")
                self.trueSec = system_data.get("security_status")
                self.starGates = []
                for g in system_data.get("stargates"):
                    self.starGates.append(PathFinderStarGate(g))

                # Clear other attributes as they may not be available from ESI
                self.alias = self.name
                self.updated = int(time.time())
                self.type_id = 2
                self.region_name = ""
                self.constellation_id = 0
                self.constellation_name = ""
                self.status_id = 1
                self.locked = 1
                self.rallyUpdated = 0
                self.rallyPoke = 0
                self.currentUser = False
                self.planets = None
                self.shattered = 0
                self.drifter = 0
                self.userCount = 0
                self.sovereignty_faction_id = 0
                self.sovereignty_faction_name = ""
                return True
        return False


class PathFinderStarGate:
    def __init__(self, id):
        self.id = id
        self.populate_from_esi()

    def populate_from_esi(self):
        response = requests.get(f"{base_url}/universe/stargates/{self.id}/")

        if response.status_code == 200:
            gate_data = response.json()
            self.systemID = gate_data.get('system_id')
            self.name = gate_data.get('name')
            self.destinationSystemID = gate_data.get('destination').get('system_id')
            self.destinationStargateID = gate_data.get('destination').get('stargate_id')

    def to_dict(self):
        gate_dict = {
            "id": self.id,
            "updated": int(time.time()),
            "source": self.systemID,
            "target": self.destinationSystemID,
            "sourceName": "",
            "sourceAlias": "",
            "targetName": "",
            "targetAlias": "",
            "scope": "stargate",
            "type": [
                "stargate"
            ],
            "endpoints": {
                "source": {
                    "label": "source",
                    "types": []
                },
                "target": {
                    "label": "target",
                    "types": []
                }
            }
        }

        return gate_dict

if __name__ == "__main__":
    # Sample usage:
    system_id = 34000072
    system_obj = PathFinderSystem({})  # Initialize an empty System object
    if system_obj.populate_from_esi(system_id):
        system_json = system_obj.to_json()
        print(system_json)
    else:
        print(f"System '{system_id}' not found in EVE Online ESI.")
