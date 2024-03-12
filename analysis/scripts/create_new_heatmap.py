import csv
from pathlib import Path
import matplotlib as mpl
import sys
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# cmap = mpl.colormaps['GnBu']

# def get_color(score: int):
#     assert 0 <= score <= 4
#     normalized_score = (score + 4) / 10
#     cm_color = cmap(normalized_score)
#     # Interpolate between white and the color from the colormap
#     # score = 0 -> white
#     # score = 5 -> color from colormap
#     factor = score/4
#     return [1 - factor + factor * cm_color[0], 1 - factor + factor * cm_color[1], 1 - factor + factor * cm_color[2]]

# for i in [0, 1, 2, 3]:
#     color = get_color(i)
#     print(f"\definecolor{{cell{i}}}{{rgb}}{{{color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}}}")
# print()

data_path = '../results/significant_features_table.csv'

with open(data_path) as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)

value_headers = [
    'Hu-Co',
    'Hu-Ex',
    'Hu-Cr',
    'Co-Ex',
    'Co-Cr',
    'Ex-Cr'
]

value_letters = {0:'\mspace', 1:'En', 2:'x', 3:'De'}

table_strs = []
for row in data:
    # print(row)
    # get the value of the dictionary
    row_values = list(row.values())
    # print(row_values)
    feature_name = row_values[0]
    feature_name = features_to_visualize_dict[feature_name]
    # replace the underscores with latex underscores
    feature_name = feature_name.replace("_", "\\_")
    # convert the values to integers
    values = [int(float(value)) for value in row_values[1:]]
    print(values)
    print(feature_name)
    if "(bold)" in feature_name:
        feature_name = "\\textbf{" + feature_name.replace("(bold)", "") + "}"
    values = [int(float(row[header])) for header in value_headers]
    cells_str = " & ".join([f"\\cellcolor{{cell{value}}}\\textcolor{{{'black' if value >= 0 else 'black'}}}{value_letters[value]}" for value in values])
    table_str = f"{feature_name} & {cells_str} \\\\"
    table_strs.append(table_str)

print("\n".join(table_strs))
# print()

totals = [0] * len(value_headers)
for row in data:
    for i, header in enumerate(value_headers):
        totals[i] += int(float(row[header]))
print(" & ".join([str(total) for total in totals]))
