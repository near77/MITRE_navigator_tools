import json
import pandas as pd


def load_navigator_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
        coverage_df = pd.DataFrame(data["techniques"])
    return coverage_df

coverage_json_file = "./Coverage.json"
coverage_df = load_navigator_data(coverage_json_file)# 540
APT29_json_file = "./APT29.json"
APT29_df = load_navigator_data(APT29_json_file)
# print(coverage_df)
join_cov_apt29 = pd.merge(coverage_df,APT29_df[["techniqueID", "tactic"]],on=["techniqueID", "tactic"])# 34
# print(join_cov_apt29)
tmp_df = APT29_df.append(coverage_df)
tmp_df = tmp_df.append(coverage_df)
diff_cov_apt29 = tmp_df.drop_duplicates(subset=["techniqueID", "tactic"],keep=False)# 4
# print(diff_cov_apt29)
tmp_df = coverage_df.append(join_cov_apt29) # 540 + 34 = 574
coverage_df = tmp_df.drop_duplicates(subset=["techniqueID", "tactic"], keep=False)
join_cov_apt29["color"] = "#ffe766"
coverage_df = coverage_df.append(join_cov_apt29)
coverage_df = coverage_df.append(diff_cov_apt29)

cov_dic = coverage_df.to_dict('records')

with open(coverage_json_file) as f:
    data = json.load(f)
    with open("./cov_apt29.json", "w") as json_f:
        data["techniques"] = cov_dic
        json.dump(data, json_f, indent=4)
