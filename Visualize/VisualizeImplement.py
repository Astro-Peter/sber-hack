import matplotlib.pyplot as plt
import pandas as pd

from Visualize import VisualizeAbstract


class VisualizeImpl(VisualizeAbstract.VisualizeAbstract):
    def compare_single(self, data: pd.DataFrame, save_as: str):
        data2=data.copy()
        data2['name'] = data2['name'] + "-" + data2['year'].astype(str) + "-" + data2['month'].astype(str)
        data2.plot.bar(x='name', y='rating')
        plt.savefig(save_as)

    def compare_multiple(self, data: pd.DataFrame, save_as: str):
        data.plot.bar(x='name', y='rating')
        plt.savefig(save_as)
