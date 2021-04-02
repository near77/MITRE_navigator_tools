# MITRE_navigator_tools
Show the intersection, subtraction of 2 MITRE navigator table in different colors.
## Requirements
```
Python3
Pandas
```
## Usage
The source MITRE Navigator table json file can be obtained from MITRE navigator website
(https://mitre-attack.github.io/attack-navigator/)
```bash
python mitre_navigator_tool.py --primary <primary table> --secondary <secondary table> --store_path <result path>
```
## Demo
Intersection and Subtraction of a sample coverage table and a APT29 table

Sample coverage table
![](https://i.imgur.com/20374BR.png)
APT29 table
![](https://i.imgur.com/5op7T5y.png)
Result table
![](https://i.imgur.com/OluXVGy.png)
