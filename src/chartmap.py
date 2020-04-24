
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

from mngrdata import DataMngr
from chartbase import Chart

class MapChart(Chart):
    """
    Represents figure and style of map chart
    """

    THRESHOLD = 1E-5
    ALPHA = 0.9
    LINE_ALIGN = 0.07
    TEXT_ALIGN = 0.07
    BAR_WIDTH = 0.1

    def __init__(self, title, xlabel, ratio, stable, top):
        super().__init__(title, xlabel, ratio, 'darkgrey', 'seaborn-deep', stable, top, 0.7, \
            DataMngr.WIDTH_MAP, DataMngr.HEIGHT_MAP, DataMngr.DPI_MAP)
        self.axes1 = self.fig.add_axes([0.85, 0.16, 0.02, 0.65])  # left, bottom, right, top

        self.curr_pos = None
        self.curr_xs = None
        self.curr_ys = None

        self.map_plot = None
        self.bounds = None
        self.globalmin = None
        self.globalmax = None
        self.localmin = None
        self.localmax = None

        self.cbar = None


    def setup_axes(self):
        """
        Setup axes
        """
        self.axes.set_aspect('equal')
        self.axes.set_axis_off()
        self.set_xlim(18.5, 23.5, self.axes)       # based on geographical coordinates
        self.set_ylim(41.5, 47, self.axes)

        self.axes1.set_axis_off()
        return

    def set_extremes(self, minval, maxval):
        """
        Set global minimum and maximum
        """
        self.globalmin = minval
        self.globalmax = maxval
        return

    def set_local_extremes(self, minval, maxval):
        """
        Set local minimum and maximum
        """
        self.localmin = minval
        self.localmax = maxval
        return

    def normalize(self, val):
        """
        Normalize given value
        """
        if self.stable:
            val_norm = DataMngr.normalize(val, 0, self.globalmax)
        else:
            val_norm = DataMngr.normalize(val, 0, self.localmax)
        return val_norm

    @classmethod
    def norm_alpha(cls, alpha):
        """
        Check is alpha value in range [0..1]
        """
        val = alpha if alpha <= cls.ALPHA else cls.ALPHA
        norm_val = val if val >= 0.0 else 0.0
        return norm_val

    @classmethod
    def set_alpha(cls, obj, alpha, hide=False, disappear=False, val=1):
        """
        Set alpha factor
        """
        if hide:
            if abs(val) < cls.THRESHOLD:
                obj.set_alpha(0)
                return obj
            else:
                alpha = cls.norm_alpha(alpha)
                obj.set_alpha(alpha)
                return obj

        if disappear:
            if abs(val) < cls.THRESHOLD:
                my_alpha = cls.norm_alpha(obj.get_alpha() - alpha)
                obj.set_alpha(my_alpha)
                return obj
            else:
                my_alpha = cls.norm_alpha(obj.get_alpha() + alpha)
                obj.set_alpha(my_alpha)
                return obj

        alpha = cls.norm_alpha(alpha)
        obj.set_alpha(alpha)
        return obj

    def create_cmap(self, maxval):
        """
        Create color map
        """
        self.cmap = mpl.colors.ListedColormap(['lightblue', 'dodgerblue', 'lightgreen', 'green', 'yellow', 'orange', 'red', 'darkred', 'indigo'])
        bounds = np.linspace(0, maxval, self.cmap.N+1)
        self.bounds = bounds if self.ratio else [int(x) for x in bounds]
        self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        return

    def create_cbar(self):
        """
        Create color bar
        """
        self.axes1.cla()
        num_format = '%.2f' if self.ratio else '%d'
        self.cbar = mpl.colorbar.ColorbarBase(self.axes1, cmap=self.cmap, norm=self.norm, ticks=self.bounds, boundaries=self.bounds, 
            spacing='proportional', orientation='vertical', format=num_format, drawedges=False)
        self.cbar.outline.set_visible(False)
        self.cbar.ax.set_title(self.xlabel, fontsize=10, y=-MapChart.TEXT_ALIGN, alpha=MapChart.ALPHA)
        return

    def draw_map(self):
        """
        Plotting map of Serbia
        """
        map_data = DataMngr.load_map()
        map_plot = map_data.plot(color='w', edgecolor='w', ax=self.axes)
        return map_plot

    def city_bar_plot(self, x, y, val, name, min_city, max_city):
        """
        Plotting bar chart at geographic coordinates of cities/municipalities
        """
        # Calculate parameters
        color = self.get_color(val)
        val_norm = DataMngr.normalize(val, min_city, max_city)
        if self.stable:
            val_norm = DataMngr.normalize(val, self.globalmin, self.globalmax)

        # Drawing    
        self.axes.bar(x=x, bottom=y, height=val_norm, width=MapChart.BAR_WIDTH, lw=0.3, color=color, edgecolor='black', align='center', alpha=MapChart.ALPHA)
        self.axes.plot([x - MapChart.LINE_ALIGN, x + MapChart.LINE_ALIGN], [y, y], ls='-', lw=0.5, color='black', alpha=MapChart.ALPHA)
        self.axes.text(x, y - MapChart.TEXT_ALIGN, name, ha='center', color='black', fontsize=8, alpha=MapChart.ALPHA)
        return

    def draw_img(self, data, target_col):
        """
        Plotting all cities/municipalities from data on given axes
        """
        # Add date
        day_str = DataMngr.date_to_str(data.index[0])
        self.axes.text(0.8, 0.85, day_str, horizontalalignment='right', transform=self.axes.transAxes, fontsize=14)

        # Make vertical bar plot for each city
        max_city = data[target_col].max()
        min_city = data[target_col].min()
        for day, city in data.iterrows():
            if city[target_col] > MapChart.THRESHOLD:
                self.city_bar_plot(x=city[DataMngr.LONGITUDE], 
                                    y=city[DataMngr.LATITUDE], 
                                    val=city[target_col], 
                                    name=city[DataMngr.CITY],
                                    min_city=min_city,
                                    max_city=max_city)
        return
    

    def init_anim(self):
        """
        Initialization of animation
        """
        # Set axis
        self.setup_axes()
        self.draw_map()

        # Data objects
        self.curr_cities = np.array([''] * self.top)
        self.curr_sizes = np.array(([0] * self.top), dtype=np.float64)
        self.curr_pos = np.arange(0, self.top, 1, dtype=np.int64)

        self.curr_xs = np.array(([0] * self.top), dtype=np.float64)
        self.curr_ys = np.array(([0] * self.top), dtype=np.float64)

        # Artist objects
        self.bars = np.array(
            self.axes.bar(x=self.curr_xs, bottom=self.curr_ys, height=self.curr_sizes, \
                width=MapChart.BAR_WIDTH, lw=0.3, edgecolor='black', align='center', alpha=MapChart.ALPHA))

        self.lines = np.array(
            [self.axes.plot([x - MapChart.LINE_ALIGN, x + MapChart.LINE_ALIGN], [y, y], ls='-', lw=0.5, color='black', alpha=MapChart.ALPHA) \
                for x, y in zip(self.curr_xs, self.curr_ys)]).flatten()

        self.cities = np.array(
            [self.axes.text(x, y - MapChart.TEXT_ALIGN, '', ha='center', color='black', fontsize=8, alpha=MapChart.ALPHA) \
                for x, y in zip(self.curr_xs, self.curr_ys)])
        
        self.date = self.axes.text(0.8, 0.9, '', horizontalalignment='right', transform=self.axes.transAxes, fontsize=20, alpha=0.6)
        self.create_cbar()

        changed = [bar for bar in self.bars] + [line for line in self.lines] + [city for city in self.cities] + [self.date]
        return changed

    def update_existing_cities(self, i_frame):
        """
        Update visibility and value of existing cities
        """
        # Artist
        exist_pos_art = np.argwhere(self.curr_pos != -1).flatten()
        if len(exist_pos_art) <= 0:
            return

        exist_bars = self.bars[exist_pos_art]
        exist_lines = self.lines[exist_pos_art]
        exist_cities_txt = self.cities[exist_pos_art]

        # Data
        exist_pos = exist_pos_art
        exist_cities_names = self.prev_cities[exist_pos]
        
        h_step = (self.curr_sizes[self.curr_pos[exist_pos]] - self.prev_sizes[exist_pos]) / (self.date_frames - 1)
        heights = self.prev_sizes[exist_pos] + (h_step * i_frame)

        alpha_step = MapChart.ALPHA / (self.date_frames / 3 - 1)

        for i, (bar, line, city_txt) in enumerate(zip(exist_bars, exist_lines, exist_cities_txt)):
            height = heights[i]

            color = self.get_color(height)
            bar.set_color(color)

            val_norm = self.normalize(height)
            bar.set_height(val_norm)

            alpha = alpha_step * i_frame
            curr_height_norm = self.normalize(self.curr_sizes[self.curr_pos[exist_pos]][i])
            MapChart.set_alpha(bar, alpha, disappear=True, val=curr_height_norm)
            MapChart.set_alpha(line, alpha, disappear=True, val=curr_height_norm)
            MapChart.set_alpha(city_txt, alpha, disappear=True, val=curr_height_norm)

        # Clean possible decimal errors
        if i_frame == self.date_frames - 1:
            for i, (bar, line, city_txt) in enumerate(zip(exist_bars, exist_lines, exist_cities_txt)):
                height = self.curr_sizes[self.curr_pos[exist_pos]][i]
                val_norm = self.normalize(height)
                bar.set_height(val_norm)
        return

    def update_new_cities(self, i_frame):
        """
        Update visibility and value of new cities
        """
        # Artist
        new_pos_art = np.argwhere(self.curr_pos == -1).flatten()
        if len(new_pos_art) <= 0:
            return

        new_bars = self.bars[new_pos_art]
        new_lines = self.lines[new_pos_art]
        new_cities_txt = self.cities[new_pos_art]
        
        # Data
        new_pos = np.setdiff1d(np.arange(0, self.top, 1), self.curr_pos)
        new_cities_names = self.curr_cities[new_pos]
        new_xs = self.curr_xs[new_pos]
        new_ys = self.curr_ys[new_pos]

        h_step = (self.curr_sizes[new_pos] - (0)) / (2 * self.date_frames / 3 - 1)
        i_frame_p2 = (i_frame - self.date_frames // 3) % (2 * self.date_frames // 3)
        heights = 0 + (h_step * i_frame_p2)

        alpha_step = MapChart.ALPHA / (self.date_frames / 3 - 1)

        for i, (bar, line, city_txt) in enumerate(zip(new_bars, new_lines, new_cities_txt)):
            # Bar
            x = new_xs[i] - MapChart.BAR_WIDTH / 2
            bar.set_x(x) 
            y = new_ys[i]
            bar.set_y(y)

            height = heights[i]
            color = self.get_color(height)
            bar.set_color(color)
            val_norm = self.normalize(height)
            bar.set_height(val_norm)

            # Line
            x1 = new_xs[i] - MapChart.LINE_ALIGN
            x2 = new_xs[i] + MapChart.LINE_ALIGN
            line.set_xdata([x1, x2])
            y1 = new_ys[i]
            y2 = new_ys[i]
            line.set_ydata([y1, y2])

            # Captions
            city_name = new_cities_names[i]
            city_txt.set_text(city_name)

            xt = new_xs[i]
            city_txt.set_x(xt)
            yt = new_ys[i] - MapChart.TEXT_ALIGN
            city_txt.set_y(yt)

            # Alpha
            alpha = alpha_step * i_frame_p2
            curr_height_norm = self.normalize(self.curr_sizes[new_pos][i])
            MapChart.set_alpha(bar, alpha, hide=True, val=curr_height_norm)
            MapChart.set_alpha(line, alpha, hide=True, val=curr_height_norm)
            MapChart.set_alpha(city_txt, alpha, hide=True, val=curr_height_norm)

        # Clean possible decimal errors
        if i_frame == self.date_frames - 1:
            for i, (bar, line, city_txt) in enumerate(zip(new_bars, new_lines, new_cities_txt)):
                # Size
                height = self.curr_sizes[new_pos][i]
                val_norm = self.normalize(height)  
                bar.set_height(val_norm)
                # Alpha
                MapChart.set_alpha(bar, MapChart.ALPHA, hide=True, val=val_norm)
                MapChart.set_alpha(line, MapChart.ALPHA, hide=True, val=val_norm)
                MapChart.set_alpha(city_txt, MapChart.ALPHA, hide=True, val=val_norm)
        return

    def update_old_cities(self, i_frame):
        """
        Update visibility of old cities
        """
        # Artist
        old_pos_art = np.argwhere(self.curr_pos == -1).flatten()
        if len(old_pos_art) <= 0:
            return

        old_bars = self.bars[old_pos_art]
        old_lines = self.lines[old_pos_art]
        old_cities_txt = self.cities[old_pos_art]

        # Data
        alpha_step = -MapChart.ALPHA / (self.date_frames / 3 - 1)

        for bar, line, text in zip(old_bars, old_lines, old_cities_txt):
            alpha = bar.get_alpha() + alpha_step * i_frame
            MapChart.set_alpha(bar, alpha)
            MapChart.set_alpha(line, alpha)
            MapChart.set_alpha(text, alpha)

        # Clean possible decimal errors
        if i_frame == self.date_frames // 3:
            for bar, line, text in zip(old_bars, old_lines, old_cities_txt):
                MapChart.set_alpha(bar, 0)
                MapChart.set_alpha(line, 0)
                MapChart.set_alpha(text, 0)
        return

    def update_values(self, i_frame):
        """
        Update values of bars
        """
        i_frame = i_frame % self.date_frames
        self.update_existing_cities(i_frame)

        if i_frame < self.date_frames // 3:
            self.update_old_cities(i_frame)
        else:
            self.update_new_cities(i_frame)

        changed = [bar for bar in self.bars] + [line for line in self.lines] + [city for city in self.cities]
        return changed

    def calc_positions_change(self, prev_cities, curr_cities):
        """
        Calculating positions change between previous and current cities list
        Returns new positions for common cities
        """
        for i, city in enumerate(prev_cities):
            ind = np.argwhere(city == curr_cities).flatten()
            self.curr_pos[i] = ind[0] if len(ind) > 0 else -1
        return

    def draw_anim(self, i_frame, data, target_col):
        """
        Drawing animation of map chart for the target column by cities/municipalities
        """
        # New day
        if i_frame % self.date_frames == 0:

            # Update artists
            new_pos_art = np.argwhere(self.curr_pos == -1).flatten()
            new_pos = np.setdiff1d(np.arange(0, self.top, 1), self.curr_pos)
            exist_pos_art = np.argwhere(self.curr_pos != -1).flatten()
            exist_pos = self.curr_pos[exist_pos_art]
            old_pos = np.concatenate((exist_pos_art, new_pos_art), axis=None)
            now_pos = np.concatenate((exist_pos, new_pos), axis=None)

            bars = [''] * self.top
            cities = [''] * self.top
            lines = [''] * self.top
            for i, npos in enumerate(now_pos):
                bars[npos] = self.bars[old_pos][i]
                cities[npos] = self.cities[old_pos][i]
                lines[npos] = self.lines[old_pos][i]

            self.bars = np.array(bars)
            self.cities = np.array(cities)
            self.lines = np.array(lines)

            # Update previous data
            self.prev_cities = self.curr_cities.copy()
            self.prev_sizes = self.curr_sizes.copy()

            # Calculate for new day
            ind_day = i_frame // self.date_frames
            day = list(data.groups.keys())[ind_day]
            data = data.get_group(day)
            self.curr_cities = np.array(data[DataMngr.CITY].reset_index(drop=True).values)
            self.curr_sizes = np.array(data[target_col].reset_index(drop=True).values)
            self.curr_xs = np.array(data[DataMngr.LONGITUDE].reset_index(drop=True).values)
            self.curr_ys = np.array(data[DataMngr.LATITUDE].reset_index(drop=True).values)
            self.calc_positions_change(self.prev_cities, self.curr_cities)

            # Artist
            day_str = DataMngr.date_to_str(day)
            self.date.set_text(day_str)

            # Info
            print(day_str)
            for i, city in enumerate(zip(self.curr_cities, self.curr_sizes)):
                print(i, city)
            print()

            # Update axes for new day
            if not self.stable:
                minval = data[target_col].min()
                maxval = data[target_col].max()
                self.set_local_extremes(minval, maxval)
                self.create_cmap(maxval)
                self.create_cbar()
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

        # Update 
        val_changed = self.update_values(i_frame)

        changed = val_changed + [self.date]
        return changed


if __name__ == "__main__":

    mapchart = MapChart(title='Title', 
                        xlabel='Xlabel', 
                        ratio=False, 
                        stable=True, 
                        top=20)

    mapchart.display(False, 'mapchart')