
import os, sys, cv2
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import matplotlib.image as image

from mngrdata import DataMngr


class Chart:
    """
    Represents figure and style of chart
    """

    LOGO_X = 100
    LOGO_Y = 100

    def __init__(self, title, xlabel, ratio, bgcolor, style, stable, top, logo_alpha, width, height, dpi):
        # Labels and style
        self.title = title
        self.xlabel = xlabel
        self.ratio = ratio
        self.bgcolor = bgcolor
        self.style = style
        self.top = top
        self.logo_alpha = logo_alpha
        self.width = width
        self.height = height
        self.dpi = dpi
        self.cmap = None
        self.norm = None
        self.date_frames = None
        self.total_frames = None

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
        fig = plt.figure(figsize=(self.width, self.height), dpi=self.dpi, facecolor=self.bgcolor)
        axes = fig.gca()
        axes.set_title(self.title)
        axes.set_xlabel(self.xlabel)
        return fig

    def set_xlim(self, xmin, xmax, axes=None):
        """
        Set limits for X-axis
        """
        self.xmin = xmin
        self.xmax = xmax
        if axes is None:
            self.axes.set_xlim(xmin=xmin, xmax=xmax)
        else:
            axes.set_xlim(xmin=xmin, xmax=xmax)
        return

    def set_ylim(self, ymin, ymax, axes=None):
        """
        Set limits for Y-axis
        """
        self.ymin = ymin
        self.ymax = ymax
        if axes is None:
            self.axes.set_ylim(ymin=ymin, ymax=ymax)
        else:
            axes.set_ylim(ymin=ymin, ymax=ymax)
        return

    def get_color(self, val):
        """
        Returns color from defined color map for normalized value
        """
        return self.cmap(self.norm(val))

    def clear(self):
        """
        Clear the current axes 
        """
        self.axes.cla()
        self.axes.set_title(self.title)
        self.axes.set_xlabel(self.xlabel)
        if (not self.xmin is None) and (not self.xmax is None):
            self.set_xlim(self.xmin, self.xmax)
        if (not self.ymin is None) and (not self.ymax is None):
            self.set_ylim(self.ymin, self.ymax)

    def display(self, to_save, filename):
        """
        Show plot or save figure
        Parameters:
            to_save  - enable saving plot, otherwise just show results on screen 
            filename - name of the file
        """
        url_img = os.path.join(DataMngr.LOGO_DIR, DataMngr.LOGO_FILENAME)
        img = image.imread(url_img)
        img = cv2.resize(img, (DataMngr.LOGO_SIZE, DataMngr.LOGO_SIZE))
        self.fig.figimage(img, Chart.LOGO_X, Chart.LOGO_Y, zorder=3, alpha=self.logo_alpha)

        if to_save:
            if self.anim is None:
                url_img = os.path.join(DataMngr.OUTPUT_DIR, '{}-{}.png'.format(filename, DataMngr.LANG))
                self.fig.savefig(url_img, dpi=self.dpi, facecolor=self.bgcolor)
            else:
                url_anim = os.path.join(DataMngr.OUTPUT_DIR, '{}-{}.mp4'.format(filename, DataMngr.LANG))
                self.anim.save(url_anim, writer='ffmpeg', dpi=self.dpi, bitrate=-1, \
                    codec='libx264', extra_args=['-pix_fmt', 'yuv420p'], savefig_kwargs=dict(facecolor=self.bgcolor))
        else:
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            plt.show()

        plt.close()
        return

    def set_frames(self, num_groups, date_frames):
        """
        Set number total number of frames and number of frames per date
        """
        self.date_frames = date_frames
        self.total_frames = num_groups * date_frames
        return


if __name__ == "__main__":

    chart = Chart(title='Title', 
                    xlabel='Xlabel', 
                    ratio=False, 
                    bgcolor='yellow', 
                    style='seaborn', 
                    stable=True, 
                    top=20, 
                    logo_alpha=0.7, 
                    width=10, 
                    height=10,
                    dpi=100)

    chart.display(False, 'BaseChart')