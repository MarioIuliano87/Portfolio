# Create a quick Dataframe to practice libraries

I created this small function to respond to the personal need to have quickly-accessible dataframes
on which I could practice new libraries and so on. 

The idea is pretty simple: I need a 2 dimensional dataframe with a date and some metrics. 

The function takes 4 parameters: 
    len_days: len of the df\
    int1: minimum integer from which random int will be generated\
    int2: maximum integer until which random int will be generated\
    int1 and int2 define the range of integers from which random numbers will
    generated\
    last_date: the date from which len_days days will be created. Defaults to current date
  
The only required parameter is len_days. The remaining parameters will default to given values if not defined by the user.

Code and output --> [here](https://github.com/MarioIuliano87/Portfolio/blob/main/functions/create_calendar_and_metric.ipynb)
