
from mngrdata import DataMngr
from mngrplot import PlotMngr


def main():

    # Initialize plot manager
    pltmgr = PlotMngr()

    # Parameters
    top = 20
    anim = True
    day = '2021-03-28'
    stable = False
    save = True

    # Bars
    #pltmgr.infected_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.ratio_infected_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.ratio_isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.infected_isolated_barh_plot(top=top, anim=anim, day=day, stable=stable, save=save)

    # Maps
    pltmgr.infected_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.ratio_infected_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.isolated_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.ratio_isolated_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)
    #pltmgr.infected_isolated_map_plot(top=top, anim=anim, day=day, stable=stable, save=save)


if __name__ == "__main__": 
    main()
