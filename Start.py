import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#I am first going to get the inputs from the user
#First, I ask for the starting date for the averages
initial_date = int(input("Starting date for the average (yyyymmdd): "))
initial_date_str = str(initial_date)
initial_year = int(initial_date_str[0:3])

#I now gask for the end date
end_date = int(input("End date for the average (yyyymmdd): "))
end_date_str = str(initial_date)
end_year = int(end_date_str[0:3])

#I now ask for the month of the year the user wants to get the info for:
month_of_interest = input("Month of interest: ")


#Read the file with climate information from the project folder
#The file was downloaded, but all the columns were "compressed" in the first
#To solve it, I imported the .csv in Excel, which converts it to real csv
#I saved as .csv and then I started to work with it
df = pd.read_csv("real_csv_BAS.csv")

#Generate a second df with only the columns I need
df2 = df[["station/location","date","tre200d0", "tre200dn", "tre200dx"]]

#Now I want to get the values only for the dates stated by the user

#Now, I slice the data frame to remove all rows before the initial date
df3 = df2.loc[df2["date"] >= initial_date]

#Now, I slice the data frame to remove all rows after the end date
df4 =df3.loc[df3["date"] <= end_date]

#Now I replace the name of the columns to something easier to read
df4=df4.rename(columns={'station/location' : 'Station', 'date' : 'Date', 'tre200d0' : 'Average temp', 'tre200dn' : 'Min temp', 'tre200dx' : 'Max temp'})

#Now I need to start working on generating the averages of the temperatures of each day across all years
#To do so I need to take the temperatures of each day. It's easier if I can split the dates in year on one side and month + day
#Instead of the current "Date" which is yyyymmdd all together.

#I generate a new dataframe from the cleaned df4, taking only the column date
df5 = df4[["Date"]]

#Then I convert the values in this column (it is now a series, not a dataframe) to str to be able to slice each value
df5=df5["Date"].apply(str)

#I create a new dataset slicing each value to extract the month and day. I take [4:] to get the positions containing the month/day
df6=df5.str[4:]

#I rename the series as Month
df6=df6.rename("Month/Day")

#And here the same for years
df9 = df4[["Date"]]
df9=df9["Date"].apply(str)
df10=df9.str[0:4]
df10=df10.rename("Year")

#I add the new columns to the dataframe
df4["Year"] = df10
df4["Month/Day"] = df6


#Now, Max temp and min temp are objects, not floats. I convert them to floats
df4["Max temp"] = pd.to_numeric(df4["Max temp"])
df4["Min temp"] = pd.to_numeric(df4["Min temp"])


#And I now generate a new dataframe with the average temperatures (Average of average, average of Max and
# average of Min for each day of the year
df11 = df4.groupby('Month/Day').mean()

#And another dataframe with the standard deviation
#df11["StDev Average temp"] = df4.groupby('Month/Day').std()

#I remove the column "Date" from the new dataframe, so I have it completely clean
df11 = df11.drop(columns=["Date"])


#I add a column "Month/Day" to use it to plot data. To do so, I take it from the index column of the df
df11["Month/Day"] = df11.index

df11["Month/Day_2"] = df11.index


#I convert the column "Month/Day" to integer
df11["Month/Day"] = pd.to_numeric(df11["Month/Day"])



#Now I want to start working on a month by month basis
#I want to get the average temperatures of august
#To do so, the best is to get the "Month/Day" column and split it in a Month and a day column

#I take an ad-hoc "Month/Day" column generated for the df11 dataframe and create a new series with it
df12 = df11["Month/Day_2"]

#And then I slice the string to get the first 2 values only (note that I need to rename the variable to itself)
df12 = df12.str.slice(stop=2)

#I do the same for the day
df13 = df11["Month/Day_2"]
df13 = df13.str.slice(start=2)

#Now I remove the extra "Month/Day_2" column that I created to get the slices for the month and day from the df11
df11 = df11.drop(columns=["Month/Day_2"])
df11 = df11.drop(columns=["Month/Day"])

#And I add the two columns, one with the Month, another with the Day
df11["Month"] = df12
df11["Day"] = df13



#Good, now I have a good dataframe to work with
#As an example, I will now plot the Average temps vs Max temps to see if there is some correlation

#I do a scatter plot using Seaborn and define the Average temp as the x values and the Max temp as the y values
#sns.scatterplot(x=df11["Average temp"], y=df11["Max temp"])
#plt.show()

#Now I rename the elements in the "Month" column as the names of the months
df11["Month"]=df11["Month"].replace({"01":"January", "02":"February","03":"March", "04":"April", "05":"May",
                       "06":"June","07":"July","08":"August", "09":"September", "10":"October","11":"November","12":"December"})

#Now I convert the values in "Day" column to integers, to make it simpler to work with them
df11["Day"] = pd.to_numeric(df11["Day"])


#Now I save the file
df11.to_csv("Clean averages from "+str(initial_year)+"to "+str(end_year)+".csv")

#OK, so I think we got it
#Now I want to start plotting real stuff
#First I want to do is to plot data from August


df_month = df11.loc[df11["Month"] == month_of_interest]
sns.lineplot(x=df_month["Day"], y=df_month["Average temp"])
sns.lineplot(x=df_month['Day'], y=df_month['Max temp'])
sns.lineplot(x=df_month['Day'], y=df_month['Min temp'])
plt.ylim(-10,30)
plt.show()
