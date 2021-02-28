# Surfs Up

## Overview

This repository hosts Jupyter Notebooks using Python, Pandas, and SQLAlchemy for the purposes of analyzing data from [hawaii.sqlite](/hawaii.sqlite) for W. Avy. In the base notebook [here](/SurfsUp_Challenge.ipynb), Temperature data is taken from June and December in Oahu to determine if the surf and ice cream shop business is sustainable year-round.

## Results

Temperature data from the sqlite was queried using SQLAlchemy and then imported as dataframes using Pandas to produce the following information:

* Mean/Average
* Standard Deviation
* Minimum
* Maximum
* First, Second and Third Quartiles

Below is the summary of temperature data for all June months (left) and December months (right)

![JuneTemp](/Resources/JuneTemperature.png) ![DecTemp](/Resources/DecemberTemperature.png)

Below is the summary of temperature data for all December months. 



As can be seen, the average temperature in December and June months is a difference of approximately three degrees F (approximately 1.67 deg C) but is on average above 71 deg F (21 deg C). However, December has a minimum temperature of 56 deg F (13.3 deg C) in comparison to June's minimum temperature of 64 deg F (17.78 deg C). Both of these temperatures breach on being too brisk for Ice Cream and surfing. Given that the minimum is so low though for December and still managing to keep within 3 degrees F of June's average, it is likely that the temperature highs balance it out. This is reflected with the maximum temperature recorded for December being 83 with June being 85. These temperatures are ideal for Ice Cream and surfing. With a standard deviation of between 3 to 4 degrees F which means the environment is fairly stable. There runs the risk of slower individual days given outliers past the first quartile of 73 and 68 degrees respectively for June and December. 

## Summary

Based on the results, it is likely safe to consider an Ice Cream and surfing shop business to be sustainable year-round albeit there runs risk of slow days. From the data provided, it is possible to delve deeper into detail to other factors that can affect business. In particular, precipation patterns show rain which in turn can suggest demand for Ice Cream and surfing based on the assumption that eating ice cream and surfing is best done on clear and warm to hot days. It is also possible to scout out locations for opening up shops. The Station table in the hawaii.sqlite provides details with where the weather station itself is and it's elevation. Weather stations nearer to ocean level for instance suggest a stronger reflection of temperatures and precipitations near the ocean. The Station table also provides the coordinates of the weather stations so it would be possible to scout for locations to open near those weather stations. 

One such query is to pull precipation and seperate by months. The following is a code block using list comprehension, pandas, and sqlalchemy to produce a data frame displaying describe data of percipitation based on months.
![precipitation](/Resources/precipitationQuery.png)

The specific query (run from sqlalchemy) the data is based on is `session.query(Measurement.prcp).filter(extract('month',Measurement.date) == x).all()` where x is the month which can be re-written as `months.index(month)+1`. The result of this query is a list of precipitation values filtered by the month.

Moving along, a sample query on extracting average temperature by station can be done using `session.query(func.avg(Measurement.tobs), 
Measurement.station).group_by(Measurement.station).all()`. Assigned into a dataframe, the result will look like this.

![avgTempStn](/Resources/avgTempStation.png)

For further granularity, it's possible to query using SQL and present as a dataframe, the average temperature at the stations by month. The query to do this is
```
SELECT station, AVG(tobs) as AvgTemp, strftime("%m",date) as mnth\
FROM Measurement\
GROUP BY mnth, station\
ORDER BY station'
```
but done through python's jupyternotebook by using `session.execute` then converted into a dataframe in the following manner and producing a dataframe of 108 rows x 3 columns as shown below.

![AvgTempStn](/Resources/avgTempStation.png)

Lastly, it's possible to modify the above query to include data from the Station table to filter by certain elevations.

```
station_month_temp = pd.DataFrame(session.execute('SELECT m.station, AVG(m.tobs), strftime("%m",m.date)\
                             FROM Measurement as m\
                             LEFT JOIN Station as s\
                                 ON m.station = s.station\
                             WHERE s.elevation < 15\
                             GROUP BY strftime("%m",m.date), m.station\
                             ORDER BY m.station').fetchall(), columns = ['station', 'avgtemp', 'num_month'])
```

In this case, out of the 9 stations, a total of 5 of them were below the 15 ft above ocean level criteria. Similarly, to append and display location, all that needs to be done would be to add `s.latitude, s.longitude` to the SELECT clause (with appropriate comma). The basis for these queries and dataframes can be found [here](/SurfsUp_Challenge_Summary) in the repository as well as supplemental resources.

