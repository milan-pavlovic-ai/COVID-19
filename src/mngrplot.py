
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import seaborn as sns

from mngrdata import DataMngr
from chartbarh import BarhChart
from chartmap import MapChart


class PlotMngr:
    """
    Plotting data
    """
    def __init__(self):
        self.data = DataMngr.load_build_data(info=False)
        self.chart = None


    def barh_plot(self, top, target_col, anim, day, title, xlabel, ratio, stable, plot_name, save):
        """
        General function for plotting horizontal bar chart for target column by cities/municipalities
        """
        # Set target data
        target_data = self.data[self.data[target_col].notna()]
        target_data = target_data.sort_values(target_col, ascending=True, kind='mergesort').groupby(DataMngr.DATE).tail(top)
        
        # Create chart
        self.chart = BarhChart(title, xlabel, ratio, stable, top)
        if stable:
            max_val = target_data[target_col].max()
            self.chart.set_xlim(0, max_val)

        # Draw plot
        if anim:
            target_data = target_data.groupby(DataMngr.DATE)
            self.chart.set_frames(num_groups=len(target_data), date_frames=DataMngr.DAY_FRAMES_BARH)
            the_anim = animation.FuncAnimation(self.chart.fig, 
                                                self.chart.draw_anim,
                                                fargs=(target_data, target_col), 
                                                init_func=self.chart.init_anim,
                                                frames=self.chart.total_frames, 
                                                interval=DataMngr.INTERVAL_BARH, 
                                                blit=True, 
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
                        target_col=DataMngr.INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_INFECTED,
                        xlabel=DataMngr.XLABEL_INFECTED,
                        ratio=False,
                        stable=stable,
                        plot_name='Confirmed BarH Plot',
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
                        target_col=DataMngr.RATIO_INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_RATIO_INFECTED,
                        xlabel=DataMngr.XLABEL_RATIO_INFECTED,
                        ratio=True,
                        stable=stable,
                        plot_name='Confirmed-ratio BarH Plot',
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
                        target_col=DataMngr.ISOLATED,
                        anim=anim,
                        day=day, 
                        title=DataMngr.TITLE_ISOLATED,
                        xlabel=DataMngr.XLABEL_ISOLATED,
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
                        target_col=DataMngr.RATIO_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_RATIO_ISOLATED,
                        xlabel=DataMngr.XLABEL_RATIO_ISOLATED,
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
        self.data[DataMngr.RATIO_INFECTED_ISOLATED] = self.data[DataMngr.RATIO_INFECTED_ISOLATED].replace([np.inf, -np.inf], np.nan)
        self.barh_plot(top=top, 
                        target_col=DataMngr.RATIO_INFECTED_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_INFECTED_ISOLATED,
                        xlabel=DataMngr.XLABEL_INFECTED_ISOLATED,
                        ratio=True,
                        stable=stable,
                        plot_name='Confirmed-Isolated BarH Plot',
                        save=save)
        return 


    def map_bar_plot(self, top, target_col, anim, day, title, xlabel, ratio, stable, plot_name, save):
        """
        General function for plotting map of Serbia with a bar chart for each city/municipality
        """
        # Set target data
        target_data = self.data[self.data[target_col].notna()]
        target_data = target_data.sort_values(target_col, ascending=True, kind='mergesort').groupby(DataMngr.DATE).tail(top)

        # Create chart
        self.chart = MapChart(title, xlabel, ratio, stable, top)
        self.chart.setup_axes()
        if stable:
            minval = target_data[target_col].min()
            maxval = target_data[target_col].max()
            self.chart.set_extremes(minval, maxval)
            self.chart.create_cmap(maxval)

        # Draw plot
        if anim:
            target_data = target_data.groupby(DataMngr.DATE)
            self.chart.set_frames(num_groups=len(target_data), date_frames=DataMngr.DAY_FRAMES_MAP)
            the_anim = animation.FuncAnimation(self.chart.fig, 
                                                self.chart.draw_anim,
                                                fargs=(target_data, target_col),
                                                init_func=self.chart.init_anim,  
                                                frames=self.chart.total_frames, 
                                                interval=DataMngr.INTERVAL_MAP, 
                                                blit=True, 
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
                        target_col=DataMngr.INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_INFECTED,
                        xlabel=DataMngr.XLABEL_INFECTED,
                        ratio=False,
                        stable=stable,
                        plot_name='Confirmed Map Plot',
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
                        target_col=DataMngr.RATIO_INFECTED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_RATIO_INFECTED,
                        xlabel=DataMngr.XLABEL_RATIO_INFECTED,
                        ratio=True,
                        stable=stable,
                        plot_name='Confirmed-ratio Map Plot',
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
                        target_col=DataMngr.ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_ISOLATED,
                        xlabel=DataMngr.XLABEL_ISOLATED,
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
                        target_col=DataMngr.RATIO_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_RATIO_ISOLATED,
                        xlabel=DataMngr.XLABEL_RATIO_ISOLATED,
                        ratio=True,
                        stable=stable,
                        plot_name='Isolated-ratio Map Plot',
                        save=save)
        return

    def infected_isolated_map_plot(self, top, anim=True, day=None, stable=False, save=False):
        """
        Plotting map of Serbia with a bar chart on the relation between infected and self-isolated cases by cities/municipalities
        Parameters:
            top      - number of top cities/municipalities shown in results
            anim     - enable animation
            day      - show results for specific day (only for images)
            stable   - enable fixed axis, for all frames axis maximum limit is the same
            save     - enable saving plot, otherwise just show results on screen
        """
        self.data[DataMngr.RATIO_INFECTED_ISOLATED] = self.data[DataMngr.RATIO_INFECTED_ISOLATED].replace([np.inf, -np.inf], np.nan)
        self.map_bar_plot(top=top, 
                        target_col=DataMngr.RATIO_INFECTED_ISOLATED, 
                        anim=anim,
                        day=day,
                        title=DataMngr.TITLE_INFECTED_ISOLATED,
                        xlabel=DataMngr.XLABEL_INFECTED_ISOLATED,
                        ratio=True,
                        stable=stable,
                        plot_name='Confirmed-Isolated Map Plot',
                        save=save)
        return


if __name__ == "__main__": 
    pltmgr = PlotMngr()
    pltmgr.infected_barh_plot(top=20, anim=True, day='2020-03-08', stable=True, save=False)
    pltmgr.infected_map_plot(top=20, anim=True, day='2020-03-08', stable=False, save=False)
