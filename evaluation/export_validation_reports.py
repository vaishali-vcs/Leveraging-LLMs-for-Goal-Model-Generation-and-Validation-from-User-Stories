import glob
import pandas as pd

input_dir = "../../eval_newcriteria2"
story_set = [f"US{i+1}" for i in range(0, 22)]
line_numbers=[2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78]

validation_results = {}
filecounter = 1

for filepath in glob.iglob(f'{input_dir}/*'):
    with open(filepath, 'r') as fh:
        readlines = fh.readlines()
        results = []
        for linenumber in line_numbers:
           results.append(readlines[linenumber].replace("\n", ""))
        validation_results[f"US{filecounter}"] = results
        filecounter += 1

df_validation_results = pd.DataFrame.from_dict(validation_results,orient='index')
df_validation_results = df_validation_results.T

df_validation_results.to_excel("evaluationreport.xlsx")

