import sys
import pandas as pd

class Dataset:
    def __init__(self,filepath):
        df = pd.read_csv(filepath)
        print(df.head(20))
