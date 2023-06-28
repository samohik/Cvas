import requests
import json
import os
import pandas
import matplotlib.pyplot as plt


class PlotDrawer:
    def __init__(self):
        self.paths_plots = None
        self.pandas_data = None
        self.url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
        self.data_file = 'data.json'
        self.plots_folder = 'plots'

        # Create the plots folder if it doesn't exist
        if not os.path.exists(self.plots_folder):
            os.makedirs(self.plots_folder)

    def get_data_from_req(self):
        data_file = requests.get(self.url).json()
        with open(self.data_file, 'w') as j_file:
            json.dump(data_file, j_file)

    def draw_plots(self, pandas_data):
        self.paths_plots = []

        # Plot and save each column in the dataframe
        for column in pandas_data.columns:
            plot_path = os.path.join(self.plots_folder, f"{column}.png")
            plt.figure(figsize=(8, 6))
            plt.plot(pandas_data[column])
            plt.title(column)
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.savefig(plot_path)
            plt.close()
            self.paths_plots.append(plot_path)

    def read_json_file(self):
        # Read the JSON file into a pandas dataframe
        pandas_data = pandas.read_json(self.data_file)
        return pandas_data

    def main(self):
        # Get data from request
        self.get_data_from_req()

        # Read the JSON file into a dataframe
        pandas_data = self.read_json_file()

        # Draw plots and get the paths
        self.draw_plots(pandas_data)

        return self.paths_plots


if __name__ == '__main__':
    x = PlotDrawer()
    paths = x.main()
    print(*[f'{x}\n' for x in paths])
