import json
import pandas as pd
import argparse

def load_navigator_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
        coverage_df = pd.DataFrame(data["techniques"])
    return coverage_df


def mitre_navigator_tool(primary:str, secondary:str, store_path:str) -> None:
    """
    :param primary: primary MITRE navigator table path (.json)
    :param secondary: secondary MITRE navigator table path (.json)
    :param store_path: the path to store the result (.json)
    """
    primary_df = load_navigator_data(primary)
    secondary_df = load_navigator_data(secondary)
    intersection_df = pd.merge(primary_df, secondary_df[["techniqueID", "tactic"]], on=["techniqueID", "tactic"])
    intersection_df["color"] = "#ffe766"
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
    parser.add_argument("--primary",help = "Primary MITRE navigator table path (.json)")
    parser.add_argument("--secondary", help = "Secondary MITRE navigator table path (.json)")
    parser.add_argument("--store_path", help = "The path to store the result (.json)")
    args = parser.parse_args()
    primary = args.primary
    secondary = args.secondary
    store_path = args.store_path
    mitre_navigator_tool(primary, secondary, store_path)

