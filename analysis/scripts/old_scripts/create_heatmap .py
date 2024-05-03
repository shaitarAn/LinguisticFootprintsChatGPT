import csv
from pathlib import Path

import matplotlib as mpl

cmap = mpl.colormaps['GnBu']


def get_color(score: int):
    assert 0 <= score <= 5
    normalized_score = (score + 5) / 10
    cm_color = cmap(normalized_score)
    # Interpolate between white and the color from the colormap
    # score = 0 -> white
    # score = 5 -> color from colormap
    factor = score/5
    return [1 - factor + factor * cm_color[0], 1 - factor + factor * cm_color[1], 1 - factor + factor * cm_color[2]]

for i in [0, 1, 2, 3, 4, 5]:
    color = get_color(i)
    print(f"\definecolor{{cell{i}}}{{rgb}}{{{color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}}}")
print()

data_path = Path(__file__).parent / 'data' / 'selected_feature_distribution - Sheet1.tsv'
assert data_path.exists()

with open(data_path) as f:
    reader = csv.DictReader(f, delimiter='\t')
    data = list(reader)

data = [row for row in data if not "(skip)" in row['feature full name']]

value_headers = [
    'HU_de',
    'HU_en',
    'CO_de',
    'CO_en',
    'EX_de',
    'EX_en',
    'CR_de',
    'CR_en',
]

table_strs = []
for row in data:
    feature_name = row['feature full name'].replace("_", "\\_")
    if "(bold)" in feature_name:
        feature_name = "\\textbf{" + feature_name.replace("(bold)", "") + "}"
    values = [int(row[header]) for header in value_headers]
    cells_str = " & ".join([f"\\cellcolor{{cell{value}}}\\textcolor{{{'black' if value >= 0 else 'black'}}}{value}" for value in values])
    table_str = f"{feature_name} & {cells_str} \\\\"
    table_strs.append(table_str)

print("\n".join(table_strs))
print()

totals = [0] * len(value_headers)
for row in data:
    for i, header in enumerate(value_headers):
        totals[i] += int(row[header])
print(" & ".join([str(total) for total in totals]))
