
import os
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

from datamgr import DataMgr


class Chart:
    """
    Represents figure and style of chart
    """
    def __init__(self, title, xlabel, bgcolor, style, stable):
        # Labels and style
        self.title = title
        self.xlabel = xlabel
        self.bgcolor = bgcolor
        self.style = style

        # Axes margins
        self.stable = stable
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        
        # Figure
        self.fig = self.create()
        self.axes = self.fig.gca()
        self.anim = None
        
    def create(self):
        """
        Returns new initialized new figure
        """
        plt.style.use(self.style) 
        fig = plt.figure(figsize=(DataMgr.WIDTH, DataMgr.HEIGHT), dpi=DataMgr.DPI, facecolor=self.bgcolor)
        axes = fig.gca()
        axes.set_title(self.title)
        axes.set_xlabel(self.xlabel)
        return fig

    def set_xlim(self, xmin, xmax):
        """
        Set limits for X-axis
        """
        self.xmin = xmin
        self.xmax = xmax
        self.axes.set_xlim(xmin=xmin, xmax=xmax)
        return

    def clear(self):
        """
        Clear the current axes 
        """
        self.axes.cla()
        self.axes.set_title(self.title)
        self.axes.set_xlabel(self.xlabel)
        if (not self.xmin is None) and (not self.xmax is None):
            self.set_xlim(self.xmin, self.xmax)

    def display(self, to_save, filename):
        """
        Show plot or save figure
        Parameters:
            to_save  - enable saving plot, otherwise just show results on screen 
            filename - name of the file
        """
        if to_save:
            if self.anim is None:
                url_img = os.path.join(DataMgr.OUTPUT_DIR, '{}-{}.png'.format(filename, DataMgr.LANG))
                self.fig.savefig(url_img, facecolor=self.bgcolor)
            else:
                url_anim = os.path.join(DataMgr.OUTPUT_DIR, '{}-{}.mp4'.format(filename, DataMgr.LANG))
                self.anim.save(url_anim, writer='ffmpeg', dpi=DataMgr.DPI)
        else:
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            plt.show()

        plt.close()
        return


class BarhChart(Chart):
    """
    Represents figure and style of horizontal bar chart
    """
    def __init__(self, title, xlabel, ratio, bar_color, stable):
        super().__init__(title, xlabel, 'white', 'seaborn-darkgrid', stable)
        self.ratio = ratio
        self.bar_color = bar_color



    def draw_img(self, data, target_col):
        """
        Drawing image of horizontal bar chart for the target column by cities/municipalities
        """
        # Make horizontal bar plot
        y = data[DataMgr.CITY]
        width = data[target_col]
        bars = self.axes.barh(y, width, color=self.bar_color, alpha=0.8)

        # Add date
        day = DataMgr.date_to_str(data.index[0])
        self.axes.text(0.95, 1.01, day, horizontalalignment='right', transform=self.axes.transAxes, fontsize=12)

        # Add value for each bar
        for bar in bars:
            y_pos = bar.get_y() + bar.get_height() / 2
            x_pos = bar.get_width() * 1.01
            text = '{:.2f}'.format(bar.get_width()) if self.ratio else int(bar.get_width())
            self.axes.text(x_pos, y_pos, text, color='black', ha='left', va='center', fontsize=8)
        return

    def draw_anim(self, i_frame, data, target_col):
        """
        Drawing horizontal bar chart for the target column by cities/municipalities
        """
        if i_frame >= len(data.groups.keys()):
            self.anim.event_source.stop()
            return

        # Clean old objects
        self.clear()

        # Make horizontal bar plot
        day = list(data.groups.keys())[i_frame]
        data = data.get_group(day)
        y = data[DataMgr.CITY]
        width = data[target_col]
        bars = self.axes.barh(y, width, color=self.bar_color, alpha=0.8)

        # Add date
        day_str = DataMgr.date_to_str(day)
        self.axes.text(0.95, 1.01, day_str, horizontalalignment='right', transform=self.axes.transAxes, fontsize=12)

        # Add value for each bar
        for bar in bars:
            y_pos = bar.get_y() + bar.get_height() / 2
            x_pos = bar.get_width() * 1.01
            text = '{:.2f}'.format(bar.get_width()) if self.ratio else int(bar.get_width())
            self.axes.text(x_pos, y_pos, text, color='black', ha='left', va='center', fontsize=8)
        return #bars


class MapChart(Chart):
    """
    Represents figure and style of map chart
    """
    def __init__(self, title, xlabel, stable):
        super().__init__(title, xlabel, 'darkgrey', 'seaborn-deep', stable)
        self.cmap = None
        self.norm = None
        self.bounds = None

    def setup_axes(self):
        """
        Setup axes
        """
        #self.axes.set_aspect('equal')
        self.axes.set_axis_off()

    def get_color(self, val):
        """
        Returns color from defined color map for normalized value
        """
        return self.cmap(self.norm(val))

    def create_cmap(self, maxval):
        """
        Create color map
        """
        self.cmap = mpl.colors.ListedColormap(['lightblue', 'dodgerblue', 'lightgreen', 'green', 'yellow', 'orange', 'red', 'darkred', 'indigo'])
        self.bounds = np.linspace(0, maxval, self.cmap.N+1)
        self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        return

    def create_cbar(self):
        """
        Create color bar
        """
        cb_axes = self.fig.add_axes([0.75, 0.1, 0.025, 0.75])
        cb = mpl.colorbar.ColorbarBase(cb_axes, cmap=self.cmap, norm=self.norm, ticks=self.bounds, boundaries=self.bounds, 
            spacing='proportional', orientation='vertical', format='%.2f', drawedges=False)
        cb.outline.set_visible(False)
        cb.set_label(self.xlabel)
        return


    def draw_map(self):
        """
        Plotting map of Serbia
        """
        serbia = DataMgr.load_map()
        serbia.plot(color='w', edgecolor='w', ax=self.axes)
        return

    def city_bar_plot(self, x, y, val, name, min_city, max_city):
        """
        Plotting bar chart at geographic coordinates of cities/municipalities
        """
        color = self.get_color(val)
        val_norm = DataMgr.normalize(val, min_city, max_city)
        val_norm_auto = self.norm(val)
        self.axes.bar(x=x, bottom=y, height=val_norm, width=0.1, lw=0.3, color=color, edgecolor='black', align='center', alpha=0.9)
        self.axes.plot([x-0.07, x+0.07], [y, y], ls='-', lw=0.5, color='black', alpha=0.9)
        self.axes.text(x, y-0.061, name, ha='center', color='black', fontsize=8, alpha=0.9)
        return

    def draw_img(self, data, target_col):
        """
        Plotting all cities/municipalities from data on given axes
        """
        max_city = data[target_col].max()
        min_city = data[target_col].min()
        for day, city in data.iterrows():
            if city[target_col] / max_city > 0.03:
                self.city_bar_plot(x=city[DataMgr.LONGITUDE], 
                                    y=city[DataMgr.LATITUDE], 
                                    val=city[target_col], 
                                    name=city[DataMgr.CITY],
                                    min_city=min_city,
                                    max_city=max_city)
        return
    
    def draw_anim(self, i_frame, data, target_col, stable):
        """
        Drawing animation of map chart for the target column by cities/municipalities
        """
        if i_frame >= len(data.groups.keys()):
            self.anim.event_source.stop()
            return

        # Clean old objects
        self.clear()
        self.setup_axes()
        self.draw_map()

        # Setup data 
        day = list(data.groups.keys())[i_frame]
        data = data.get_group(day)
        if not stable:
            maxval = data[target_col].max()
            self.create_cmap(maxval)

        # Add date
        day_str = DataMgr.date_to_str(day)
        self.axes.text(0.95, 1.01, day_str, horizontalalignment='right', transform=self.axes.transAxes, fontsize=12)

        # Make vertical bar plot for each city
        max_city = data[target_col].max()
        min_city = data[target_col].min()
        for day, city in data.iterrows():
            if city[target_col] / max_city > 0.03:
                self.city_bar_plot(x=city[DataMgr.LONGITUDE], 
                                    y=city[DataMgr.LATITUDE], 
                                    val=city[target_col], 
                                    name=city[DataMgr.CITY],
                                    min_city=min_city,
                                    max_city=max_city)

        self.create_cbar()
        return


if __name__ == "__main__":
    barchart = BarhChart('Title', 'Xlabel', False, 'red', True)
    barchart.display(False, 'barchart')

    mapchart = MapChart('Title', 'Xlabel', True)
    mapchart.display(False, 'mapchart')