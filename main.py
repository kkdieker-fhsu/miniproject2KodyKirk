# INF601 - Advanced Programming in Python

# Kody Kirk

# Mini Project 2


#     (5/5 points) Initial comments with your name, class and project at the top of your .py file.
#     (5/5 points) Proper import of packages used.
#     (20/20 points) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
#     Think of some question you would like to solve such as:
#     "How many homes in the US have access to 100Mbps Internet or more?"
#     "How many movies that Ridley Scott directed is on Netflix?" - https://www.kaggle.com/datasets/shivamb/netflix-shows
#     Here are some other great datasets: https://www.kaggle.com/datasets
#     (10/10 points) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data is labeled tabular data.
#     (10/10 points) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build some fancy charts here as it will greatly help you in future homework assignments and in the final project.
#     (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the project should save these when it executes. You may want to add this folder to your .gitignore file.
#     (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
#     (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
#     (20/20 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the explanations.

# This project is to visualize and quantify how lucky or unlucky I am when playing TTRPGs. The data is from the virtual
#   tabletop I host and includes my roll data from the last several sessions.

import matplotlib.pyplot as plt
import pandas as pd
import os

# this is probably an awful way of parsing this, but the json data used contains quite a few different records, with the
#   one I wanted buried inside other parts of it

# first, read the data in the json file that is formatted as 'records'
data = pd.read_json('me-dice-stats-json-data.json', orient='records')

# then extract the Series under 'PLAYER_DICE', which itself contains a list of dictionaries that holds the data
#   I want
datadict = data['PLAYER_DICE'][0][7]

# the data consists of d20 die results. this part is to add a column that associates the frequency of the roll with the
#   corresponding die value
tuples = []
for i in range(len(datadict['ROLLS'])):
    tuples.append((i+1,datadict['ROLLS'][i]))
total_rolls = datadict['TOTAL_ROLLS']

# finally, recreate the dataframe with the values desired and get some useful values from it
rolldata = pd.DataFrame.from_records(tuples, columns=['Die Value', 'Frequency'])
diesize = len(rolldata)
expectedvalue = float(total_rolls)/float(diesize)

# begin plotting
fig, ax = plt.subplots()
ax.set_xlabel('Roll')
ax.set_xticks(ticks=rolldata['Die Value'])
ax.set_ylabel('Frequency')
ax.set_yticks(ticks=range(1,max(rolldata['Frequency'])+1))
ax.set_title('Frequency of Dice rolls')

# create a bar chart with a horizontal line across it denoting the expected value of the die
ax.bar(rolldata['Die Value'], rolldata['Frequency'], color='black')
ax.axhline(y=expectedvalue, color='g')

# this part is to create the bars showing the distance of each result from the expected value using error bars
# first, get the difference for each data point
ydiffs = [expectedvalue] * diesize - rolldata['Frequency']

# create lists for the upper and lower error to get asymmetric error bars
ylowererror = []
yuppererror = []

# loop over each difference
# if the difference is negative, the frequency is higher than expected, so that difference
#   is made positive and appended to the lower error list and a 0 to the upper, and vice versa for positive differences
for e in ydiffs:
    if e < 0:
        ylowererror.append(abs(e))
        yuppererror.append(0)
    else:
        yuppererror.append(e)
        ylowererror.append(0)

# create the error array for plotting
yerror = [ylowererror, yuppererror]

# plot the error bars
ax.errorbar(rolldata['Die Value'], rolldata['Frequency'], yerr = yerror, fmt='none', color='r')
fig.show()
