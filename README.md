# COVID-19
Visualization of COVID-19 confirmed and self-isolated cases by municipalities/cities in Serbia

## Date, Region and Domain
* April 24, 2020
* Serbia
* Health
      
## Research Questions
1. Which are the top municipalities/cities in Serbia with the highest COVID-19 confirmed cases overall and to population ratio?
1. Which are the top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases overall and to population ratio?

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

## Visualization
### Map chart
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases
    * https://streamable.com/e2xh1f
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio
    * https://streamable.com/nnftnr
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases
    * https://streamable.com/dag565
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases to population ratio
    * https://streamable.com/dnekz3

### Bar chart race
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases
    * https://streamable.com/n8jbsi
1. Top municipalities/cities in Serbia with the highest COVID-19 confirmed cases to population ratio
    * https://streamable.com/bjd3qk
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases
    * https://streamable.com/i55qo6
1. Top municipalities/cities in Serbia with the highest COVID-19 self-isolated cases to population ratio
    * https://streamable.com/wjid0w

## Technology
* Libraries
    * numpy
    * pandas
    * matplotlib  
* Installation
    * Get necessary libraries with command: pip install -r requirements.txt
    * You can adjust the quality and size of the visualizations in the config.ini file

## About
The goal of visualization is to answer the research questions. Data visualization presents the difference between municipalities/cities in Serbia by different criteria. 

The municipality/city population data represent the population estimate for 2018 according to the Statistical Office of the Republic of Serbia. Due to the unavailability of accurate and complete data, the province of Kosovo and Metohija was omitted. Data on infected cases of coronavirus were downloaded from the website of the Government of the Republic of Serbia with the original source of the Institute of Public Health of Serbia "Milan Jovanovic Batut", while the number of self-isolated cases was taken from the website of the Government of the Republic of Serbia with the original source of the Ministry of Interior of the Republic of Serbia.
