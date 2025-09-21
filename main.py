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
import numpy as np
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
tuplesall = []
tuplesatk = []
tuplessave = []
for i in range(len(datadict['ROLLS'])):
    tuplesall.append((i+1,datadict['ROLLS'][i]))
    tuplesatk.append((i+1,datadict['ATK_ROLLS'][i]))
    tuplessave.append((i+1,datadict['SAVES_ROLLS'][i]))
total_rolls = datadict['TOTAL_ROLLS']

# finally, recreate the dataframes with the values desired and get some useful values from it
rolldata = pd.DataFrame.from_records(tuplesall, columns=['Die Value', 'Frequency'])
atkdata = pd.DataFrame.from_records(tuplesatk, columns=['Die Value', 'Frequency'])
savesdata = pd.DataFrame.from_records(tuplessave, columns=['Die Value', 'Frequency'])
diesize = len(rolldata)
expectedvalue = float(total_rolls)/float(diesize)

# begin plotting
fig1, ax = plt.subplots()
ax.set_xlabel('Roll')
ax.set_xticks(ticks=rolldata['Die Value'])
ax.set_ylabel('Frequency')
ax.set_yticks(ticks=range(1,max(rolldata['Frequency'])+1))
ax.set_title('Frequency of Dice rolls')

# create a bar chart
ax.bar(rolldata['Die Value'], rolldata['Frequency'], color='black')

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

# plot the error bars and a bar for the expected frequencies for each result
ax.errorbar(rolldata['Die Value'], rolldata['Frequency'], yerr = yerror, fmt='none', color='r')
ax.axhline(y=expectedvalue, color='g')

# create a second figure with two subplot that share an x axis
fig2, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Attack Rolls')
ax2.set_title('Saves')

ax1.bar(atkdata['Die Value'], atkdata['Frequency'], color='black')
ax2.bar(savesdata['Die Value'], savesdata['Frequency'], color='black')
ax2.set_xticks(ticks=rolldata['Die Value'])
fig2.supylabel('Frequency')

# having some fun with trend lines here
# probably has little in the way of true statistical rigor, but it's fun to see how the rolls trend
atktrend = np.polynomial.polynomial.Polynomial.fit(atkdata['Die Value'], atkdata['Frequency'], 5)
ax1.plot(atkdata['Die Value'], atktrend(atkdata['Die Value']), color='r')

savestrend = np.polynomial.polynomial.Polynomial.fit(savesdata['Die Value'], savesdata['Frequency'], 1)
ax2.plot(savesdata['Die Value'], savestrend(savesdata['Die Value']), color='r')

#check if a folder titled 'charts' exists in the file location. if not, make one
if not os.path.exists('charts'):
    os.mkdir('charts')

fig1.savefig('charts/alld20.png', dpi=800)
fig2.savefig('charts/atksaves.png', dpi=800)

fig1.show()
fig2.show()