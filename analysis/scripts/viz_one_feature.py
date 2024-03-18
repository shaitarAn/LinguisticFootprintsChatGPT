import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
from viz_helper import *

features = [
    "flesch_reading_ease",
    "flesch_kincaid_grade",
    "gunning_fog",
    "automated_readability_index",
    "coleman_liau_index",
    "lix",
    "rix"
]

for f in features:

    feature = f"../../feature_extraction/results/per_feature/{f}/pubmed_de.csv"

    df = pd.read_csv(feature)

    # plot the means

    plot_means("../../viz", df, f, 0.05)

