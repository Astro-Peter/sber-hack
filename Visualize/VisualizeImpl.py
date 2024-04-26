import matplotlib.pyplot as plt
import pandas as pd

from Visualize import VisualizeAbstract


class VisualizeImpl(VisualizeAbstract.VisualizeAbstract):
    def compare_single(self, data: pd.DataFrame, topic_name: str, time_frame: str, save_as: str):
        topic_data = data[data['name'] == topic_name]

        if topic_data.empty:
            print(f"No data available for the topic '{topic_name}'.")
            return

        if 'rating' not in topic_data.columns:
            print("Error: 'rating' data is not available to plot.")
            return

        if 'year' in topic_data.columns:
            if 'month' in topic_data.columns:
                topic_data['time'] = topic_data['year'].astype(str) + "-" + topic_data['month'].astype(str).str.zfill(2)
            else:
                topic_data['time'] = topic_data['year'].astype(str)
        else:
            print("No 'year' data available for plotting.")
            return

        if 'time' in topic_data.columns:
            topic_data = topic_data.groupby('time').agg({'rating': 'sum'}).reset_index()

        plt.figure(figsize=(15, 8))
        ax = topic_data.plot.bar(x='time', y='rating', color='skyblue', width=0.8)
        plt.title(f'Rating of {topic_name} over {time_frame}', fontsize=18)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Rating', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
        plt.savefig(save_as)
        plt.close()

    def compare_multiple(self, data: pd.DataFrame, time_frame: str, save_as: str):
        if 'rating' not in data.columns:
            print("Error: 'rating' column is missing from the data. Check the database query.")
            return

        if 'month' in data.columns or 'year' in data.columns:
            data = data.groupby('name').agg({'rating': 'sum'}).reset_index()

        plt.figure(figsize=(15, 8))
        ax = data.plot.bar(x='name', y='rating', color='skyblue', width=0.8)
        plt.title(f'Comparison of All Topics over {time_frame}', fontsize=18)
        plt.xlabel('Topic Name', fontsize=14)
        plt.ylabel('Rating', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
        plt.savefig(save_as)
        plt.close()

