import re
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np

def getHTNumbers(fileName : str) -> list[tuple[str, float, float]]:
    with open(fileName, "r") as f:
        dates : list[str] = []
        weightNumbers : list[float] = []
        repNumbers : list[float] = []

        prevLine : str = ""
        for line in f:
            if (line.find("HT x") != -1):
                date = re.sub(r"[a-zA-Z\(\)\,\? +]", '', prevLine[:prevLine.find(' ')])
                date = re.sub(r"\.", '/', date)
                dates.append(date)
                
                if (line.find("BW") != -1):
                    weightNumbers.append(0.0)
                    repNumbers.append(float(line[line.find("HT x") + 4:line.find('F')].replace('½', '.5')))
                else:
                    firstWeightNum = line[: line.find(' ')]
                    firstWeightNum = re.sub(r"[a-zA-Z\(\)\,\?\n +]", '', firstWeightNum)
                    weightNumbers.append(float(firstWeightNum))

                    firstRepNum = line[line.find("HT x") + 4:line.find('/')].replace('½', '.5')
                    firstRepNum = re.sub(r"[a-zA-Z\(\)\,\? +]", '',firstRepNum) 
                    repNumbers.append(float(firstRepNum))
            prevLine = line

        return [(date, weight, reps) for date, weight, reps in zip(dates, weightNumbers, repNumbers)]

hipThrustProgress = getHTNumbers("logbook.txt")
dates = []
weights = []
reps = []
for (date, weightNum, repNum) in hipThrustProgress:
    dates.append(dt.datetime.strptime(date, "%m/%d/%y").date())
    weights.append(weightNum)
    reps.append(repNum)

data = { "Date" : dates, "Weight" : weights, "Reps" : reps }
dataFrame = pd.DataFrame(data)

fig, firstAxis = plt.subplots()

firstAxis.set_xlabel("Date")
firstAxis.set_ylabel("Weight (in lbs)", color = "red")
firstAxis.scatter(dataFrame['Date'], dataFrame['Weight'], color = "red")
firstAxis.tick_params(axis='y', labelcolor = "red")
daysSinceJan_1_1970toFeb9_2025 = 20128.5
firstAxis.vlines(x=daysSinceJan_1_1970toFeb9_2025, ymin=0.0, ymax=600.0, color='orange', \
                label="Switch from B-Stance to Single Leg", linestyle="--")

secondAxis = firstAxis.twinx()
secondAxis.set_ylabel("Reps", color = "blue")
secondAxis.scatter(dataFrame['Date'], dataFrame['Reps'])
secondAxis.tick_params(axis='y', labelcolor = "blue")

dateToTime = []
i = 1
for date in dataFrame["Date"]:
    dateToTime.append(i)
    i += 1

# weightRateOfChange = np.gradient(dataFrame["Weight"], dateToTime)
# thirdAxis = firstAxis.twinx()
# thirdAxis.plot(dataFrame['Date'], weightRateOfChange, color = "green")

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels)

plt.title("Hip Thrust Progress")
plt.show()
