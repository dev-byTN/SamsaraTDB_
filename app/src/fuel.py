from datetime import timedelta, date

week = (date.today() - timedelta(days=7)).isocalendar()[1]

def get_fuel_info(data):
    list_fuel = []
    list_missing = []
    list_abusive = []

    abusive = 50

    for i in data: 
        immat = i["vehicle"]["name"] 
        if i["efficiencyMpge"] == 0:
            efficacite = 0
        else : efficacite = 235 / i["efficiencyMpge"] 
        carburant_consomme = i["fuelConsumedMl"] / 1000 
        distance = i["distanceTraveledMeters"] / 1000 
        emission_carbonne = i["estCarbonEmissionsKg"]
        
        if efficacite > 50:
            abusif = "True"
        else : abusif = False
        
        stat = {
            "Immatriculation" : immat, 
            "Efficacite" : round(efficacite,1), 
            "Abusif" : abusif,
            "Carburant consomme" : round(carburant_consomme,1),
            "Distance parcouru" : round(distance,1), 
            "Emission de carbonne" : round(emission_carbonne,1),
            "Semaine" : week,
        }
        
        if efficacite == 0:
            list_missing.append(stat)
        elif efficacite >= abusive:
            list_abusive.append(stat)
        list_fuel.append(stat)

    return list_missing, list_abusive, list_fuel