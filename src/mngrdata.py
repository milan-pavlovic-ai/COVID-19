
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import cyrtranslit
import missingno as msno 
import matplotlib.pyplot as plt

from configparser import ConfigParser


class DataMngr:
    """
    Loading and building data
    """

    # Directory structure 
    ROOT_DIR = os.getcwd()
    CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
    DATAIN_DIR = os.path.join(ROOT_DIR, 'data/input')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'data/output')
    MAP_DIR = os.path.join(ROOT_DIR, 'data/map')
    LOGO_DIR = os.path.join(ROOT_DIR, 'data/logo')

    # Parameters
    url_config = os.path.join(CONFIG_DIR, 'config.ini')
    config = ConfigParser()
    config.read(url_config)

    PARAM = 'param'
    LANG = config.get(PARAM, 'LANG')
    LOGO_SIZE = int(config.get(PARAM, 'LOGO_SIZE'))

    WIDTH_BARH = int(config.get(PARAM, 'WIDTH_BARH'))
    HEIGHT_BARH = int(config.get(PARAM, 'HEIGHT_BARH'))
    DPI_BARH = int(config.get(PARAM, 'DPI_BARH'))
    DAY_FRAMES_BARH = int(config.get(PARAM, 'DAY_FRAMES_BARH'))
    INTERVAL_BARH = int(config.get(PARAM, 'INTERVAL_BARH'))

    WIDTH_MAP = int(config.get(PARAM, 'WIDTH_MAP'))
    HEIGHT_MAP = int(config.get(PARAM, 'HEIGHT_MAP'))
    DPI_MAP = int(config.get(PARAM, 'DPI_MAP'))
    DAY_FRAMES_MAP = int(config.get(PARAM, 'DAY_FRAMES_MAP'))
    INTERVAL_MAP = int(config.get(PARAM, 'INTERVAL_MAP'))

    FILE = 'file'
    GEO_FILENAME = config.get(FILE, 'GEO_FILENAME')
    POPUL_FILENAME = config.get(FILE, 'POPUL_FILENAME')
    MAP_FILENAME = config.get(FILE, 'MAP_FILENAME')
    LOGO_FILENAME = config.get(FILE, 'LOGO_FILENAME')

    # Labels
    lang_url = os.path.join(CONFIG_DIR, 'lang.ini')
    labels = ConfigParser()
    labels.read(lang_url)

    DATE = labels.get(LANG, 'DATE')
    CITY = labels.get(LANG, 'CITY')
    POPULATION = labels.get(LANG, 'POPULATION')
    INFECTED = labels.get(LANG, 'INFECTED')
    RATIO_INFECTED = labels.get(LANG, 'RATIO_INFECTED')
    ISOLATED = labels.get(LANG, 'ISOLATED')
    RATIO_ISOLATED = labels.get(LANG, 'RATIO_ISOLATED')
    RATIO_INFECTED_ISOLATED = labels.get(LANG, 'RATIO_INFECTED_ISOLATED')
    LATITUDE = labels.get(LANG, 'LATITUDE')
    LONGITUDE = labels.get(LANG, 'LONGITUDE')

    TITLE_INFECTED = labels.get(LANG, 'TITLE_INFECTED')
    XLABEL_INFECTED = labels.get(LANG, 'XLABEL_INFECTED')
    TITLE_RATIO_INFECTED = labels.get(LANG, 'TITLE_RATIO_INFECTED')
    XLABEL_RATIO_INFECTED = labels.get(LANG, 'XLABEL_RATIO_INFECTED')

    TITLE_ISOLATED = labels.get(LANG, 'TITLE_ISOLATED')
    XLABEL_ISOLATED = labels.get(LANG, 'XLABEL_ISOLATED')
    TITLE_RATIO_ISOLATED = labels.get(LANG, 'TITLE_RATIO_ISOLATED')
    XLABEL_RATIO_ISOLATED = labels.get(LANG, 'XLABEL_RATIO_ISOLATED')

    TITLE_INFECTED_ISOLATED = labels.get(LANG, 'TITLE_INFECTED_ISOLATED')
    XLABEL_INFECTED_ISOLATED = labels.get(LANG, 'XLABEL_INFECTED_ISOLATED')

    # Cleaning keywords
    PREFIX = 'Град '
    INVALID_WORDS = ['област', 'регион', 'србиј']

    # Coefficients
    RATIO_INFECTED_COEFF = 1E3
    RATIO_ISOLATED_COEFF = 1E3
    RATIO_INFECTED_ISOLATED_COEFF = 1E2


    @staticmethod
    def describe_data(df, info_flag):
        """
        Describe given dataframe
        """
        if info_flag:
            print(df)
            print('NaN:\n', df.isna().sum())
            print('NaN rows:\n', df[df.isna().any(axis=1)])
            print(df.describe(include='all'))
            msno.matrix(df)
            plt.show()
            plt.close()
        return


    @staticmethod
    def normalize(val, min, max):
        """
        Normalize value into range [0..1]
        """
        return (val - min) / (max - min)

    @staticmethod
    def latin_to_cyrillic(text):
        """
        Convert Latin letters to Serbian-Cyrillic letters
        """
        return cyrtranslit.to_cyrillic(text)

    @staticmethod
    def date_to_str(date):
        """
        Date conversion into appropriate string format
        """
        return date.strftime('%d.%m.%Y')

    @classmethod
    def clean_prefix(cls, text):
        """
        Remove prefix for given string
        """
        text = text.strip()
        pos = text.find(cls.PREFIX)
        if pos >= 0:
            return text[pos + len(cls.PREFIX):]  
        return text

    @classmethod
    def is_not_city(cls, text):
        """
        Text is not a city/municipality if it has numbers or invalid words in the name.
        Returns True if given text is not a city/municipality
        """
        contains_number = lambda text: any(ch.isdigit() for ch in text)
        contains_invalid_word = lambda text: any((word in text.lower()) for word in cls.INVALID_WORDS)

        return contains_number(text) or contains_invalid_word(text)


    @classmethod
    def load_single_infect_data(cls, url, info):
        """
        Load and clean data for COVID-19 infected cases by cities/municipalities
        """
        data = pd.read_csv(url, usecols=[1,2], names=[cls.CITY, cls.INFECTED], header=None)
        day = pd.Timestamp(data.iloc[0, 0])
        data = data.iloc[3:].dropna()
        data[cls.DATE] = day
        data[cls.INFECTED] = data[cls.INFECTED].astype(float)
        data[cls.CITY] = data[cls.CITY].apply(cls.clean_prefix)
        cls.describe_data(data, info)
        return data

    @classmethod
    def load_infect_data(cls, url, info):
        """
        Load and clean data for COVID-19 infected cases by cities/municipalities for the entire period
        """
        data = pd.DataFrame()
        for filename in os.listdir(url):
            url_file = os.path.join(url, filename)
            data_file = cls.load_single_infect_data(url_file, False)
            data = pd.concat([data, data_file])

        cls.describe_data(data, info)
        return data

    @classmethod
    def load_single_isolat_data(cls, url, info):
        """
        Load and clean data for COVID-19 self-isolated cases by cities/municipalities
        """
        data = pd.read_csv(url, usecols=[1,2], names=[cls.CITY, cls.ISOLATED], header=None)
        day = pd.Timestamp(data.iloc[0, 0])
        data = data.iloc[3:].dropna()
        data[cls.DATE] = day
        data[cls.ISOLATED] = data[cls.ISOLATED].astype(float)
        data[cls.CITY] = data[cls.CITY].apply(cls.clean_prefix)
        cls.describe_data(data, info)
        return data

    @classmethod
    def load_isolat_data(cls, url, info):
        """
        Load and clean data for COVID-19 self-isolated cases by cities/municipalities for the entire period
        """
        data = pd.DataFrame()
        for filename in os.listdir(url):
            url_file = os.path.join(url, filename)
            data_file = cls.load_single_isolat_data(url_file, False)
            data = pd.concat([data, data_file])

        cls.describe_data(data, info)
        return data

    @classmethod
    def load_populat_data(cls, url, info):
        """
        Load and clean data for cities/municipalities population in Serbia 
        """
        populat_data = pd.read_excel(url, usecols='A,D', skiprows=7, skipfooter=44, header=None)
        populat_data.columns = [cls.CITY, cls.POPULATION]
        populat_data = populat_data.dropna()
        populat_data[cls.POPULATION] = populat_data[cls.POPULATION].astype(int)
        populat_data[cls.CITY] = populat_data[cls.CITY].apply(cls.clean_prefix)

        not_city_rows = populat_data[populat_data[cls.CITY].apply(cls.is_not_city)]
        populat_data = populat_data.drop(not_city_rows.index)
        #print('Not city rows:\n', not_city_rows, len(not_city_rows))

        #print('Cities with same subregion name:\n', populat_data.groupby(cls.CITY).filter(lambda group: len(group) >= 2))
        populat_data = populat_data.groupby(cls.CITY).max()       # select main city from municipalities with same name
        cls.describe_data(populat_data, info)
        return populat_data

    @classmethod
    def load_geo_data(cls, url, info):
        """
        Load geographic coordinates for cities/municipalities in Serbia
        """
        geo_data = pd.read_csv(url, usecols=[0,1,2], names=[cls.CITY, cls.LATITUDE, cls.LONGITUDE], header=0)
        geo_data = geo_data.dropna()            
        geo_data[cls.CITY] = geo_data[cls.CITY].replace('Belgrade', 'Београд').apply(cls.latin_to_cyrillic)
        geo_data = geo_data.set_index(cls.CITY)
        cls.describe_data(geo_data, info)
        return geo_data

    @classmethod
    def load_build_data(cls, info=False):
        """
        Returns loaded and built data
        """
        # Load
        url_infect = os.path.join(cls.DATAIN_DIR, 'infected')
        infect_data = cls.load_infect_data(url_infect, info)

        url_isolat = os.path.join(cls.DATAIN_DIR, 'isolated')
        isolat_data = cls.load_isolat_data(url_isolat, info)

        url_populat = os.path.join(cls.DATAIN_DIR, cls.POPUL_FILENAME)
        populat_data = cls.load_populat_data(url_populat, info)

        url_geo = os.path.join(cls.DATAIN_DIR, cls.GEO_FILENAME)
        geo_data = cls.load_geo_data(url_geo, info)

        # Merge
        infect_isolat_data = pd.merge(infect_data, isolat_data, on=[cls.CITY, cls.DATE], how='outer')
        cls.describe_data(infect_isolat_data, info)

        cases_populat_data = pd.merge(infect_isolat_data, populat_data, on=cls.CITY, how='inner')
        cls.describe_data(cases_populat_data, info)

        data = pd.merge(cases_populat_data, geo_data, on=cls.CITY, how='inner')
        cls.describe_data(data, info)

        # Transform
        infected_cases = data[data[cls.INFECTED].notna()]
        data[cls.RATIO_INFECTED] = (infected_cases[cls.INFECTED] / infected_cases[cls.POPULATION]) * cls.RATIO_INFECTED_COEFF

        isolated_cases = data[data[cls.ISOLATED].notna()]
        data[cls.RATIO_ISOLATED] = (isolated_cases[cls.ISOLATED] / isolated_cases[cls.POPULATION]) * cls.RATIO_ISOLATED_COEFF

        both_cases = data[data[cls.INFECTED].notna() & data[cls.ISOLATED].notna()]
        data[cls.RATIO_INFECTED_ISOLATED] = (both_cases[cls.INFECTED] / both_cases[cls.ISOLATED]) * cls.RATIO_INFECTED_ISOLATED_COEFF

        data = data.set_index(cls.DATE).sort_index()
        cls.describe_data(data, info)
        return data


    @classmethod
    def load_map(cls):
        """
        Loading map into geo-pandas dataframe
        """
        url_map = os.path.join(cls.MAP_DIR, cls.MAP_FILENAME)
        serbia = gpd.read_file(url_map)
        return serbia


if __name__ == "__main__": 
    data = DataMngr.load_build_data(info=True)
    print(data)

