import matplotlib.pyplot as plt
class UI:
    def UI(self, dataframes):
        self.dataframes = dataframes
    def plot_dataframes(self):
        for name, df in self.dataframes:
            x = df['X']
            y = df['Y']
            plt.plot(x, y, label='name')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('DataFrames Graph')
        plt.legend()
        plt.show()