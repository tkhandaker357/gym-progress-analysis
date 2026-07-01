import re
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np

# functions like a macro
ADMIN_PRIVILEGES = 1
chosenExercise : str = "None"

def getExerciseName() -> str:
    selection : str = "Invalid"
    while True:
        selection = input("Choose an exercise:\n\t(1) Hip Thrust\n\t(2) Bulgarian Split Squat\n\t(3) Romanian Deadlift\n")
        match selection:
            case "1" | "Hip Thrust"            | "HT":
                globals()["chosenExercise"] = "Hip Thrust"
                return "HT"
            case "2" | "Bulgarian Split Squat" | "BSS":
                globals()["chosenExercise"] = "Bulgarian Split Squat"
                return "BSS"
            case "3" | "Romanian Deadlift"     | "RDL":
                globals()["chosenExercise"] ="Romanian Deadlift"
                return "RDL"
            case _:
                # for me to see the graph of any exercise i choose
                if ADMIN_PRIVILEGES == 1:
                    globals()["chosenExercise"] = selection 
                    return selection
                else:
                    continue


def getExerciseNumbers(fileName : str, whichExercise : str) -> list[tuple[str, float, float]]:
    with open(fileName, "r") as f:
        dates : list[str] = []
        weightNumbers : list[float] = []
        repNumbers : list[float] = []
        
        prevLine : str = ""
        date : str = ""
        for line in f:
            if (line.find("HT") != -1):
                date = re.sub(r"[a-zA-Z\(\)\,\? +]", '', prevLine[:prevLine.find(' ')])
                date = re.sub(r"\.", '/', date)
            prevLine = line

            if (line.find(whichExercise) != -1):
                dates.append(date)

                if (line.find("BW") != -1):
                    weightNumbers.append(0.0)
                    repNumbers.append(float(line[line.find(" x") + 4:line.find('F')].replace('½', '.5')))
                else:
                    firstWeightNum = line[: line.find(' ')]
                    if (firstWeightNum.find('/') != -1):
                        firstWeightNum = firstWeightNum[: firstWeightNum.find('/')]
                    firstWeightNum = re.sub(r"[a-zA-Z\(\)\,\?\n +]", '', firstWeightNum)
                    weightNumbers.append(float(firstWeightNum))
                    firstRepNum = line[line.find(" x") + 3:line.find('/')].replace('½', '.5')
                    firstRepNum = re.sub(r"[a-zA-Z\(\)\,\? +]", '',firstRepNum) 
                    repNumbers.append(float(firstRepNum))

        return [(date, weight, reps) for date, weight, reps in zip(dates, weightNumbers, repNumbers)]

exerciseProgress = getExerciseNumbers("logbook.txt", getExerciseName())

dates = []
weights = []
reps = []

for (date, weightNum, repNum) in exerciseProgress:
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

# TODO: 
#   add match statement to change this line from simply being the switch from b-stance to single leg hip thrusts
#   to the corresponding changes in bulgarian split squats and romanian deadlifts during switch from smith machine
#   to machine hip thrusts

daysSinceJan_1_1970toFeb9_2025 : float = 20128.5
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
    
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels)

plt.title(chosenExercise + " Progress")
plt.show()
