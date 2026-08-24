import pandas as pd
from datetime import timedelta, date

# Left join two lists of dictionaries on a primary key
def gather_data(left_list, right_list, key):

    if not isinstance(left_list, list) or not isinstance(right_list, list):
        raise TypeError("Both left_list and right_list must be lists of dictionaries.")
    
    # Build a lookup dictionary for the right list
    right_lookup = {}
    for row in right_list:
        if not isinstance(row, dict):
            raise TypeError("All elements in right_list must be dictionaries.")
        if key not in row:
            raise KeyError(f"Key '{key}' missing in right_list element: {row}")
        right_lookup[row[key]] = row

    # Perform the left join
    joined = []
    for left_row in left_list:
        if not isinstance(left_row, dict):
            raise TypeError("All elements in left_list must be dictionaries.")
        if key not in left_row:
            raise KeyError(f"Key '{key}' missing in left_list element: {left_row}")
        
        # Copy to avoid mutating original data
        merged_row = left_row.copy()
        
        # Merge matching data from right list (excluding the key to avoid overwriting)
        right_row = right_lookup.get(left_row[key])
        if right_row:
            merged_row.update({k: v for k, v in right_row.items() if k != key})
        
        joined.append(merged_row)
    
    return joined
    


def get_platform():

    samsara_site = []
    sip2_site = []

    dt = pd.read_excel("../ressource/rattachement PLF.xlsx", sheet_name = 'rattachement PF')
    dt = dt.to_numpy()

    for i in dt:
        samsara = i[0]
        site = i[1]
        sip2 = i[2]
        site2 = i[3]

        set1 = {
            "Samsara" : samsara,
            "Site" : site
        }
        set2 = {
            "SIP2" : sip2,
            "Site" : site2
        }

        samsara_site.append(set1)
        sip2_site.append(set2)

    return samsara_site, sip2_site


def get_correspondant_site(conso, site, sip2):

    for i in conso:
        for j in site:
            try:
                if i["Site"].upper() == j["Samsara"].upper() :
                    new_site = j["Site"]
                    break
            except:
                for k in sip2:
                    if i["Immatriculation"] == k["Immatriculation"]:
                        new_site = k["Etablissement opérationnel"]
                        break
                    new_site = "No site attributed"

                for l in site:
                    if new_site == l["Site SIP2"]:
                        new_site = l["Sites(2)"]
                        break

        i.update({"site" : new_site})   

    return conso


def get_last_week_date():

    today = date.today()
    last_week = today - timedelta(days=7)
    last_week_number = last_week.weekday() + 1

    day_to_monday = last_week_number - 1
    monday = last_week - timedelta(days=day_to_monday)

    return monday