import json
from metlib.normet.nora3 import read_winds,read_waves

if __name__ == "__main__":
    wdata=read_winds.get_metadata()
    
    vardata=wdata["variables"]
    for name, variable in vardata.items():
        if name=="projection_lambert":
            continue
        desc = variable.get("description", variable.get("long_name"))
        unit = variable.get("units")
        print(f"{name}={desc} [{unit}]")
    
    # with open("wind_metadata.json","w",encoding="utf8") as f:
    #     f.write(json.dumps(wdata, indent=4))
    # # with open("waves_metadata.json","w",encoding="utf8") as f:
    #     f.write(json.dumps(read_waves.get_metadata(), indent=4))
