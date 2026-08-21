
def get_tachy_files(data):

    list_files = []
    for i in data:
        name = i["vehicle"]["name"]
        for j in i["files"]:
            vin = j["vin"]
            url = j["url"]

        stat = {
            "Immatriculation": name,
            "VIN" : vin,
            "Fichier Tachy" : url
        }

        list_files.append(stat)

    return list_files