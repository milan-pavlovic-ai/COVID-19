# COVID-19
Visualization of COVID-19 confirmed and self-isolated cases by municipalities/cities in Serbia.

Implementation of algorithm bar-chart-race with local and global viewpoints. 

## Date, Region and Domain
* May 4, 2020
* Serbia
* Health
      
## Research Questions
1. Which are the top municipalities/cities in Serbia with the highest total COVID-19 confirmed cases?
1. Which are the top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio?
1. Which are the top municipalities/cities in Serbia with the highest total COVID-19 self-isolated cases?
1. Which are the top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases to population ratio?

## Data Sources
* Population estimates by municipalities/cities 2018
    * https://publikacije.stat.gov.rs/G2019/Xls/G201913046.xlsx
* Number of COVID-19 confirmed cases by municipalities/cities
    * https://covid19.data.gov.rs/
* Number of COVID-19 self-isolated cases by municipalities/cities
    * https://covid19.data.gov.rs/self_isolation
* Geographic coordinates by municipalities/cities
    * https://simplemaps.com/data/rs-cities
* Map of Serbia
    * http://alas.matf.bg.ac.rs/~mi09109/sr_kos_regional.html
* News in Serbia
    * https://sr.wikipedia.org/wiki/Пандемија_вируса_корона_у_Србији_2020.

## Visualization
### Map chart
1. Top municipalities/cities in Serbia with the highest total COVID-19 confirmed cases
    * https://youtu.be/VFxMH-yaiVA
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio
    * https://youtu.be/5cGeN5OKGFY
1. Top municipalities/cities in Serbia with the highest total COVID-19 self-isolated cases
    * https://youtu.be/4nJBIBfBIWc
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases to population ratio
    * https://youtu.be/d8tXrhAeKf8

### Bar chart race
1. Top municipalities/cities in Serbia with the highest total COVID-19 confirmed cases
    * https://youtu.be/XTsFuy-O0Kk
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio
    * https://youtu.be/LRioosJCZtg
1. Top municipalities/cities in Serbia with the highest total COVID-19 self-isolated cases
    * https://youtu.be/tSb4OF9WZt8
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases to population ratio
    * https://youtu.be/B8vzNp_KmfU

## Technology
The implementation of the bar-chart-race algorithm is based on monitoring the position of each bar and its value in every frame.
The smooth transition between two adjacent days is made possible by assigning the appropriate number of frames to the transition calculation. Where each frame corresponds to one step by how much the bar value and its position are increased/decreased.

The map of Serbia was imported from a JSON file using the geopandas library, the map is actually a large polygon. Geographical coordinates were used (latitude and longitude) to be able to present the real position of municipalities/cities on the map.

* Libraries
    * numpy
    * pandas
    * matplotlib  
* Installation
    * Get necessary libraries with command: pip install -r requirements.txt
    * You can adjust the quality and size of the visualizations in the config.ini file

## Discussion
### About
The goal of visualization is to answer the research questions. Data visualization presents the difference between municipalities/cities in Serbia by different criteria. 

The municipality/city population data represent the population estimate for 2018 according to the Statistical Office of the Republic of Serbia. Due to the unavailability of accurate and complete data, the province of Kosovo and Metohija was omitted. Data on infected cases of coronavirus were downloaded from the website of the Government of the Republic of Serbia with the original source of the Institute of Public Health of Serbia "Milan Jovanovic Batut", while the number of self-isolated cases was taken from the website of the Government of the Republic of Serbia with the original source of the Ministry of Interior of the Republic of Serbia.

The observation period on confirmed cases is from the first recorded positive case at 06.03 until 04.05. There are missing data on confirmed cases in the period 30.03-07.04 and 08.04-15.04 from used source. Notice that the visualization used the total number of recorded confirmed cases, regardless of whether the counted cases were cured at some point or unfortunately not alive anymore. The observation period on self-isolated cases is from 24.03. to 04.05.

### At day 23.04.2020
On 23.04.2020 we have 2 cities that have more than 1000 COVID-19 confirmed cases. Belgrade has 1910 cases, making it the city with the highest number of confirmed cases, followed by Niš with 1038,
Ćuprija 227, Kruševac 170, Valjevo 165 and Leskovac with 162 cases, other municipalities/cities have fewer than 150 cases.

In the case of top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio. The first place is Ćuprija, which has 8 confirmed cases in every 1000 citizens, the third place is Niš with 4 confirmed cases in every 1000 citizens.
Although Belgrade has the highest number of confirmed cases, 
it is not in the top 20 municipalities/cities in terms of population.

Leading city in the number of self-isolated cases of the virus corona is Belgrade with 3273 cases, which is about 2x more than Novi Sad with 1540 cases which is in second place. Belgrade, Niš, Leskovac and Kruševac are cities that are in the top 6 in both criteria, by absolute number of self-isolated cases and by absolute number of confirmed cases.

In the case of top municipalities/cities with the highest COVID-19 self-isolated cases to population ratio, mostly at the top are municipalities/cities with a small population such as Blace, Babušnica, Ćuprija, with between 12-16 self-isolated cases in 1000 citizens.

### Over period
Looking at the data over the observed period, we can see that from the first days Belgrade and Niš were dominant in the number of confirmed cases, from 15.03. Valjevo occurs and from 19.03. Ćuprija.
The mentioned 4 municipalities/cities are absolutely leading until 29.03., as well as in the period from 15.04. to 04.05., where they are joined by Kruševac and Leskovac.

As of 15.04. most of the leading municipalities/cities of confirmed cases in terms of population are in southeastern Serbia.

Belgrade, Lozinica, Novi Sad and Niš are leading in the number of self-isolated cases which are generally increasing from the first days to 11.04 when the number of cases starts dramatically falling to 18.04 when numbers become mostly static. The number of cases continues to falling from 26.04.

Mostly from day one, we can see that the leading municipalities/cities in terms of self-isolated cases in terms of population are close the western and southern borders of Serbia until 11.04. when we have a dramatic decline in the number of self-isolated cases. As of 16.04., most of the leading municipalities/cities are located in Southeastern Serbia.
