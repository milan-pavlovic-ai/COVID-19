
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


class BarhChart(Chart):
    """
    Represents figure and style of horizontal bar chart
    """

    HEIGHT = 0.8
    ALPHA = 0.8

    def __init__(self, title, xlabel, ratio, stable, top):
        super().__init__(title, xlabel, ratio, 'white', 'seaborn-darkgrid', stable, top, 0.7, \
            DataMngr.WIDTH_BARH, DataMngr.HEIGHT_BARH, DataMngr.DPI_BARH)
        self.create_cmap()
        self.colors = None
        # Artist
        self.bars = None
        self.date = None
        self.cities = None
        # Data
        self.prev_cities = None
        self.curr_cities = None
        self.prev_sizes = None
        self.curr_sizes = None
        self.prev_pos = None
        self.curr_pos = None


    def set_xlim(self, xmin, xmax):
        """
        Set limits for X-axis
        """
        xmax = xmax * 1.1 if self.ratio else max(int(xmax + 1), int(xmax * 1.1))
        return super().set_xlim(xmin, xmax)

    def create_cmap(self):
        """
        Create color map
        """
        self.cmap = cm.get_cmap('tab20')
        return

    def draw_img(self, data, target_col):
        """
        Drawing image of horizontal bar chart for the target column by cities/municipalities
        """
        # Make horizontal bar plot
        y = data[DataMngr.CITY]
        width = data[target_col]
        bars = self.axes.barh(y, width, color=self.cmap(np.arange(len(y)-1, -1, -1)), alpha=BarhChart.ALPHA)

        # Add date
        day = DataMngr.date_to_str(data.index[0])
        self.axes.text(0.95, 1.01, day, horizontalalignment='right', transform=self.axes.transAxes, fontsize=14)

        # Add value for each bar
        for bar in bars:
            y_pos = bar.get_y() + bar.get_height() / 2
            x_pos = bar.get_width() * 1.01
            text = '{:.2f}'.format(bar.get_width()) if self.ratio else int(bar.get_width())
            self.axes.text(x_pos, y_pos, text, color='black', ha='left', va='center', fontsize=8)
        return


    def init_anim(self):
        """
        Initialization of animation
        """
        # Set axes
        self.axes.set_ylim(0, self.top)
        self.axes.set_yticks(np.arange(BarhChart.HEIGHT/2, self.top, 1))
        self.axes.set_yticklabels([str(i) for i in np.arange(self.top, 0, -1)])
        #self.axes.get_yaxis().set_visible(False)

        # Data objects
        self.curr_pos = np.arange(0, self.top, 1, dtype=np.int64)
        self.curr_cities = np.array([''] * self.top)
        self.curr_sizes = np.array(([0] * self.top), dtype=np.float64)
        self.colors = np.array(self.cmap.colors)

        # Artist objects
        self.bars = np.array(self.axes.barh(self.curr_pos, self.curr_sizes, align='edge', height=BarhChart.HEIGHT, alpha=BarhChart.ALPHA))
        self.cities = np.array([self.axes.text(0, 0, '', horizontalalignment='left', verticalalignment='center') for bar in self.bars])
        self.date = self.axes.text(0.95, 0.075, '', horizontalalignment='right', transform=self.axes.transAxes, fontsize=22, alpha=0.7)

        changed = [bar for bar in self.bars] + [city for city in self.cities] + [self.date]
        return changed

    def calc_positions_change(self, prev_cities, curr_cities):
        """
        Calculating positions change between previous and current cities list
        Returns new positions for common cities
        """
        # Update previous
        self.prev_pos = np.arange(0, self.top, 1)
        self.curr_pos = np.zeros(self.top, dtype=np.int64)

        # Calculate new
        for i, city in enumerate(prev_cities):
            ind = np.argwhere(city == curr_cities).flatten()
            self.curr_pos[i] = ind[0] if len(ind) > 0 else -1

        # missing values indicates new cities
        return
        
    def update_existing_cities(self, i_frame):
        """
        Update positions and values of existing cities
        """
        # Artist
        exist_pos_art = np.argwhere(self.curr_pos != -1).flatten()
        if len(exist_pos_art) <= 0:
            return

        exist_cities_txt = self.cities[exist_pos_art]
        exist_bars = self.bars[exist_pos_art]
        exist_colors = self.colors[exist_pos_art]

        # Data
        exist_pos = exist_pos_art
        exist_cities_names = self.prev_cities[exist_pos]
        
        y_step = (self.curr_pos[exist_pos] - self.prev_pos[exist_pos]) / (self.date_frames - 1)
        w_step = (self.curr_sizes[self.curr_pos[exist_pos]] - self.prev_sizes[exist_pos]) / (self.date_frames - 1)

        ys = self.prev_pos[exist_pos] + (y_step * i_frame)
        ws = self.prev_sizes[exist_pos] + (w_step * i_frame)

        for i, bar in enumerate(exist_bars):
            y = ys[i]
            bar.set_y(y)
            w = ws[i]
            bar.set_width(w)
            bar.set_color(exist_colors[i])

            y_txt = y + bar.get_height() / 2.0
            x_txt = w * 1.01
            city_name = exist_cities_names[i]
            val = '{:.2f}'.format(w) if self.ratio else str(int(round(w, 0)))
            city = exist_cities_txt[i]
            city.set_text(city_name + '\n' + val)
            city.set_x(x_txt)
            city.set_y(y_txt)
            if abs(w) < 1E-5: 
                city.set_text('')
                bar.set_color(None)

        # Clean possible decimal errors
        if i_frame == self.date_frames - 1:
            for i, bar in enumerate(exist_bars):
                y = round(bar.get_y(), 0)
                bar.set_y(y)
                curr_val = self.curr_sizes[self.curr_pos[exist_pos]][i]
                bar.set_width(curr_val)
        return

    def update_old_cities(self, i_frame):
        """
        Update positions of old cities
        """
        # Artist
        old_pos_art = np.argwhere(self.curr_pos == -1).flatten()
        if len(old_pos_art) <= 0:
            return

        old_cities_txt = self.cities[old_pos_art]
        old_bars = self.bars[old_pos_art]
        old_colors = self.colors[old_pos_art]

        # Data
        old_pos = old_pos_art
        old_cities_names = self.prev_cities[old_pos]

        y_step = (self.curr_pos[old_pos] - self.prev_pos[old_pos]) / (self.date_frames / 2 - 1)
        #w_step = ((0) - self.prev_sizes[old_pos]) / (self.date_frames / 2 - 1)

        ys = self.prev_pos[old_pos] + (y_step * i_frame)
        #ws = self.prev_sizes[old_pos] + (w_step * i_frame)

        for i, bar in enumerate(old_bars):
            y = ys[i]
            bar.set_y(y)
            #w = ws[i]
            #bar.set_width(w)
            bar.set_color(old_colors[i])

            y_txt = y + bar.get_height() / 2.0
            x_txt = bar.get_width() * 1.01
            city_name = old_cities_names[i] 
            prev_val = self.prev_sizes[old_pos][i]
            val = '{:.2f}'.format(prev_val) if self.ratio else str(int(prev_val))
            city = old_cities_txt[i]
            city.set_text(city_name + '\n' + val)
            city.set_x(x_txt)
            city.set_y(y_txt)
            if abs(prev_val) < 1E-5: 
                city.set_text('')
                bar.set_color(None)

        # Clean possible decimal errors
        if i_frame == self.date_frames // 2:
            for bar in old_bars:
                bar.set_y(-1)
                bar.set_width(0)
        return

    def update_new_cities(self, i_frame):
        """
        Update positions and values for new cities
        """
        # Artist
        new_pos_art = np.argwhere(self.curr_pos == -1).flatten()
        if len(new_pos_art) <= 0:
            return

        new_cities_txt = self.cities[new_pos_art]
        new_bars = self.bars[new_pos_art]
        new_colors = self.colors[new_pos_art] 

        # Data
        new_pos = np.setdiff1d(np.arange(0, self.top, 1), self.curr_pos)
        new_cities_names = self.curr_cities[new_pos]

        y_step = (new_pos - (-1)) / (self.date_frames / 2 - 1)
        w_step = (self.curr_sizes[new_pos] - (0)) / (self.date_frames / 2 - 1)

        i_frame_p2 = i_frame % (self.date_frames // 2)
        ys = -1 + (y_step * i_frame_p2)
        ws = 0 + (w_step * i_frame_p2)

        for i, bar in enumerate(new_bars):
            y = ys[i]
            bar.set_y(y)
            w = ws[i]
            bar.set_width(w)
            bar.set_color(new_colors[i])

            y_txt = y + bar.get_height() / 2.0
            x_txt = bar.get_width() * 1.01
            city_name = new_cities_names[i]
            val = '{:.2f}'.format(w) if self.ratio else str(int(round(w, 0)))
            city = new_cities_txt[i]
            city.set_text(city_name + '\n' + val)
            city.set_x(x_txt)
            city.set_y(y_txt)
            if abs(w) < 1E-5: 
                city.set_text('')
                bar.set_color(None)

        # Clean possible decimal errors
        if i_frame == self.date_frames - 1:
            for i, bar in enumerate(new_bars):
                y = round(bar.get_y(), 0)
                bar.set_y(y)
                w = self.curr_sizes[new_pos][i]
                bar.set_width(w)
        return

    def update_positions(self, i_frame):
        """
        Update position of bars
        """
        i_frame = i_frame % self.date_frames

        self.update_existing_cities(i_frame)

        if i_frame < self.date_frames // 2:
            self.update_old_cities(i_frame)
        else:
            self.update_new_cities(i_frame)

        changed = [bar for bar in self.bars] + [city for city in self.cities]
        return changed

    def draw_anim(self, i_frame, data, target_col):
        """
        Drawing horizontal bar chart for the target column by cities/municipalities
        """
        # New day
        if i_frame % self.date_frames == 0:

            # Update artists
            bars_ranks = np.vectorize(lambda bar: bar.get_y())(self.bars)
            order = np.argsort(bars_ranks, kind='mergesort')
            self.bars = self.bars[order]
            self.cities = self.cities[order]
            self.colors = self.colors[order]

            # Update previous data
            self.prev_cities = self.curr_cities.copy()
            self.prev_sizes = self.curr_sizes.copy()

            # Calculate for new day
            ind_day = i_frame // self.date_frames
            day = list(data.groups.keys())[ind_day]
            data = data.get_group(day)
            self.curr_cities = np.array(data[DataMngr.CITY].reset_index(drop=True).values)
            self.curr_sizes = np.array(data[target_col].reset_index(drop=True).values)
            self.calc_positions_change(self.prev_cities, self.curr_cities)

            # Artist
            day_str = DataMngr.date_to_str(day)
            self.date.set_text(day_str)

            # Info
            print(day_str)
            for i, city in enumerate(zip(reversed(self.curr_cities), reversed(self.curr_sizes))):
                print(self.top - 1 - i, city)
            print()

            # Update axes for new day
            if not self.stable:
                maxval = data[target_col].max()
                self.set_xlim(0, maxval)
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

        # Update 
        pos_changed = self.update_positions(i_frame)

        changed = pos_changed + [self.date]
        return changed


if __name__ == "__main__":

    barchart = BarhChart(title='Title', 
                        xlabel='Xlabel', 
                        ratio=False, 
                        stable=True, 
                        top=20)

    barchart.display(False, 'barchart')