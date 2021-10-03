# Create a quick Dataframe to practice libraries

I created this small function to respond to the personal need to have quickly-accessible dataframes
on which I could practice new libraries and so on. 

The idea is pretty simple: I need a 2 dimensional dataframe with a date and some metrics. 

The function takes 4 parameters: 
    len_days: len of the df
    int1: minimum integer from which random int will be generated
    int2: maximum integer until which random int will be generated
    int1 and int2 define the range of integers from which random numbers will
    generated
    last_date: the date from which len_days days will be created. Defaults to current date
  
The only required parameter is len_days. The remaining parameters will default to given values if not defined by the user.
An example output: 

<img width="172" alt="Screenshot 2021-10-03 at 15 24 46" src="https://user-images.githubusercontent.com/73912794/135755578-088128ba-1a15-4ac8-8b28-5a094a3f36e9.png">
