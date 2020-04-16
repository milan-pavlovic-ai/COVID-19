
from datamgr import DataMgr
from plotmgr import PlotMgr


def main():
    data = DataMgr.load_build_data(infect_filename='COVID19 Infected 07-04-2020.xlsx',
                isolat_filename='COVID19 Self-isolated 07-04-2020.xlsx',
                info=True)

    # Maps
    PlotMgr.infected_map_plot(data, top=20, save=False)

    # Bars
    PlotMgr.infected_barh_plot(data, top=20, save=False)
    PlotMgr.isolated_barh_plot(data, top=20, save=False)
    PlotMgr.infected_isolated_line_plot(data, top=20, save=False)


if __name__ == "__main__": 
  main()