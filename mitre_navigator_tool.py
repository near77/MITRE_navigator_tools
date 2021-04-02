import json
import pandas as pd
import argparse

Green = "#c7e9c0"
Red = "#fca2a2"
Yellow = "#fcf3a2"

def load_navigator_data(json_file, color):
    with open(json_file) as f:
        data = json.load(f)
        coverage_df = pd.DataFrame(data["techniques"])
        coverage_df["color"] = color
    return coverage_df

def color_techniques_with_subtecnique(primary:str, color:str) -> pd.DataFrame:
    """
    :param primary: primary MITRE navigator table path (.json)
    :param color: color to fill in the cell ("#ffffff")
    """
    all_technique_df = load_navigator_data("./Navigator_tables/All_techniques.json", color)
    primary_df = load_navigator_data(primary, Green)
    primary_technique_set = [x for index, x in primary_df.iterrows()]
    primary_technique_set = list(set([x["techniqueID"] for index, x in primary_df.iterrows()]))
    lost_techniques = []
    for technique in primary_technique_set:
        if technique.split(".")[0] not in primary_technique_set:
            lost_techniques.append(technique.split(".")[0])
    lost_techniques_df = all_technique_df[all_technique_df["techniqueID"].isin(lost_techniques)]
    result_df = primary_df.append(lost_techniques_df)
    result_df["color"] = color
    return result_df


def mitre_navigator_tool(primary:str, secondary:str, store_path:str, show_meta:bool = True) -> None:
    """
    :param primary: primary MITRE navigator table path (.json)
    :param secondary: secondary MITRE navigator table path (.json)
    :param store_path: the path to store the result (.json)
    :param show_meta: if include technique of selected subtechniques
    """
    if show_meta:
        primary_df = color_techniques_with_subtecnique(primary, Green)
        secondary_df = color_techniques_with_subtecnique(secondary, Red)
    else:
        primary_df = load_navigator_data(primary, Green)
        secondary_df = load_navigator_data(secondary, Red)
    
    intersection_df = pd.merge(primary_df, secondary_df[["techniqueID", "tactic"]], on=["techniqueID", "tactic"])
    intersection_df["color"] = Yellow
    substraction_df = secondary_df.append(primary_df)
    substraction_df = substraction_df.append(primary_df)
    substraction_df = substraction_df.drop_duplicates(subset=["techniqueID", "tactic"],keep=False)
    result_df = primary_df.append(intersection_df)
    result_df = result_df.drop_duplicates(subset=["techniqueID", "tactic"], keep=False)
    result_df = result_df.append(intersection_df)
    result_df = result_df.append(substraction_df)
    result_dic = result_df.to_dict("records")
    with open(primary) as f:
        data = json.load(f)
        with open(store_path, "w") as json_f:
            data["techniques"] = result_dic
            json.dump(data, json_f, indent=4) 

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", help = "Primary MITRE navigator table path (.json)")
    parser.add_argument("--secondary", help = "Secondary MITRE navigator table path (.json)")
    parser.add_argument("--store_path", help = "The path to store the result (.json)")
    args = parser.parse_args()
    primary = args.primary
    secondary = args.secondary
    store_path = args.store_path
    mitre_navigator_tool(primary, secondary, store_path)

