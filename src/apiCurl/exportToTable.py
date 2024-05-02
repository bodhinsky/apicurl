import json, os
import pandas as pd

datapath="./data/"

def export_to_dataframe(collection_info):
    if not collection_info:
        return None

    print("Data path not present right now. Creating...")
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    
    with open(f"{datapath}Collection.json", "w", encoding="utf-8") as f:
        json.dump(collection_info, f, ensure_ascii=False, indent=4)

    return pd.DataFrame(collection_info)

def export_to_xlsx(dataframe):

    print("Data path not present right now. Creating...")
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    with pd.ExcelWriter(f'{datapath}/Record_Collection.xlsx', engine='openpyxl') as writer:
        dataframe.to_excel(writer, sheet_name='All Releases')
