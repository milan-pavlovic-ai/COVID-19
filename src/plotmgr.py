
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import seaborn as sns

from datamgr import DataMgr
from chart import BarhChart, MapChart


class PlotMgr:
    """
    Plotting data
    """
    def __init__(self):
        self.data = DataMgr.load_build_data(info=False)
        self.chart = None


    def barh_plot(self, top, target_col, anim, day, title, xlabel, bar_color, ratio, stable, plot_name, save):
        """
        General function for plotting horizontal bar chart for target column by cities/municipalities
        """
        # Set target data
        target_data = self.data[self.data[target_col].notna()]
        target_data = target_data.sort_values(target_col, ascending=True).groupby(DataMgr.DATE).tail(top)
        
        # Create chart
        self.chart = BarhChart(title, xlabel, ratio, bar_color, stable)
        if stable:
            max_val = target_data[target_col].max()
            self.chart.set_xlim(0, max_val)

        # Draw plot
        if anim:
            target_data = target_data.groupby(DataMgr.DATE)
            the_anim = animation.FuncAnimation(self.chart.fig, 
                                                self.chart.draw_anim,
                                                fargs=(target_data, target_col), 
                                                frames=len(target_data), 
                                                interval=1000, 
                                                blit=False, 
                                                repeat=False)
            self.chart.anim = the_anim
        else:
            # Setting data for choosen day
            days = target_data.sort_index().loc[:pd.Timestamp(day)]
            the_day = days.tail(1).index if len(days) > 0 else target_data.sort_index().head(1).index
            target_data = target_data.loc[the_day]
            # Drawing
            self.chart.draw_img(target_data, target_col)

        self.chart.display(save, plot_name)
        return

    def infected_barh_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting horizontal bar chart for infected cases by cities/municipalities
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.barh_plot(top=top,
                        target_col=DataMgr.INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_INFECTED,
                        xlabel=DataMgr.XLABEL_INFECTED,
                        bar_color='red',
                        ratio=False,
                        stable=stable,
                        plot_name='Infected BarH Plot',
                        save=save)
        return

    def ratio_infected_barh_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting horizontal bar chart for infected cases by cities/municipalities in ratio to population
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.barh_plot(top=top, 
                        target_col=DataMgr.RATIO_INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_RATIO_INFECTED,
                        xlabel=DataMgr.XLABEL_RATIO_INFECTED,
                        bar_color='orangered',
                        ratio=True,
                        stable=stable,
                        plot_name='Infected-ratio BarH Plot',
                        save=save)
        return
        
    def isolated_barh_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting horizontal bar chart for self-isolated cases by cities/municipalities
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.barh_plot(top=top, 
                        target_col=DataMgr.ISOLATED,
                        anim=anim,
                        day=day, 
                        title=DataMgr.TITLE_ISOLATED,
                        xlabel=DataMgr.XLABEL_ISOLATED,
                        bar_color='slateblue',
                        ratio=False,
                        stable=stable,
                        plot_name='Isolated BarH Plot',
                        save=save)
        return

    def ratio_isolated_barh_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting horizontal bar chart for self-isolated cases by cities/municipalities in ratio to population
                Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.barh_plot(top=top, 
                        target_col=DataMgr.RATIO_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_RATIO_ISOLATED,
                        xlabel=DataMgr.XLABEL_RATIO_ISOLATED,
                        bar_color='dodgerblue',
                        ratio=True,
                        stable=stable,
                        plot_name='Isolated-ratio BarH Plot',
                        save=save)
        return           

    def infected_isolated_barh_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting horizontal bar chart on the relation between infected and self-isolated cases by cities/municipalities
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.barh_plot(top=top, 
                        target_col=DataMgr.RATIO_INFECTED_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_INFECTED_ISOLATED,
                        xlabel=DataMgr.XLABEL_INFECTED_ISOLATED,
                        bar_color='mediumpurple',
                        ratio=True,
                        stable=stable,
                        plot_name='Infected-Isolated BarH Plot',
                        save=save)
        return 


    def map_bar_plot(self, top, target_col, anim, day, title, xlabel, ratio, stable, plot_name, save):
        """
        General function for plotting map of Serbia with a bar chart for each city/municipality
        """
        # Set target data
        target_data = self.data[self.data[target_col].notna()]
        target_data = target_data.sort_values(target_col, ascending=True).groupby(DataMgr.DATE).tail(top)

        # Create chart
        self.chart = MapChart(title, xlabel, ratio, stable)
        self.chart.setup_axes()
        if stable:
            minval = target_data[target_col].min()
            maxval = target_data[target_col].max()
            self.chart.set_extremes(minval, maxval)
            self.chart.create_cmap(maxval)

        # Draw plot
        if anim:
            target_data = target_data.groupby(DataMgr.DATE)
            print(target_data)
            the_anim = animation.FuncAnimation(self.chart.fig, 
                                                self.chart.draw_anim,
                                                fargs=(target_data, target_col, stable),
                                                #init_func=self.chart.draw_map,  
                                                frames=len(target_data), 
                                                interval=1000, 
                                                blit=False, 
                                                repeat=False)
            self.chart.anim = the_anim
        else:
            # Setting data for choosen day
            days = target_data.sort_index().loc[:pd.Timestamp(day)]
            the_day = days.tail(1).index if len(days) > 0 else target_data.sort_index().head(1).index
            target_data = target_data.loc[the_day]
            if not stable:
                maxval = target_data[target_col].max()
                self.chart.create_cmap(maxval)
            # Drawing
            self.chart.draw_map()
            self.chart.draw_img(target_data, target_col)
            self.chart.create_cbar()

        self.chart.display(save, plot_name)
        return

    def infected_map_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting map of Serbia with a bar chart for each city/municipality of infected cases
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.map_bar_plot(top=top,
                        target_col=DataMgr.INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_INFECTED,
                        xlabel=DataMgr.XLABEL_INFECTED,
                        ratio=False,
                        stable=stable,
                        plot_name='Infected Map Plot',
                        save=save)
        return

    def ratio_infected_map_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting map of Serbia with a bar chart for each city/municipality of infected cases to population ratio
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.map_bar_plot(top=top,
                        target_col=DataMgr.RATIO_INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_RATIO_INFECTED,
                        xlabel=DataMgr.XLABEL_RATIO_INFECTED,
                        ratio=True,
                        stable=stable,
                        plot_name='Infected-ratio Map Plot',
                        save=save)
        return

    def isolated_map_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting map of Serbia with a bar chart for each city/municipality of isolated cases
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.map_bar_plot(top=top,
                        target_col=DataMgr.ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_ISOLATED,
                        xlabel=DataMgr.XLABEL_ISOLATED,
                        ratio=False,
                        stable=stable,
                        plot_name='Isolated Map Plot',
                        save=save)
        return

    def ratio_isolated_map_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting map of Serbia with a bar chart for each city/municipality of isolated cases to population ratio
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.map_bar_plot(top=top,
                        target_col=DataMgr.RATIO_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMgr.TITLE_RATIO_ISOLATED,
                        xlabel=DataMgr.XLABEL_RATIO_ISOLATED,
                        ratio=True,
                        stable=stable,
                        plot_name='Isolated-ratio Map Plot',
                        save=save)
        return


def main():

    pltmgr = PlotMgr()

    # Parameters
    top = 20
    anim = True
    day = '2021-03-28'
    stable = True
    save = False

    # Bars
    pltmgr.infected_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.ratio_infected_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.ratio_isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.infected_isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)

    # Maps
    pltmgr.infected_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.ratio_infected_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.isolated_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    pltmgr.ratio_isolated_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)


if __name__ == "__main__": 
    main()


# Testing
''' 
# Choosing color map
cs = [(i, c) for i, c in enumerate(mpl.pyplot.colormaps())]
for i, c in cs:
    infected_map_plot(data, c, i)

# Choosing color
cs = [(i, c) for i, c in enumerate(mcolors.CSS4_COLORS) if i in [106]]
for i, c in cs:
    infected_map_plot(data, c, i)

# Choosing style
styles = [style for i, style in enumerate(plt.style.available)]
for style in styles:
    infected_map_plot(data, style)
'''