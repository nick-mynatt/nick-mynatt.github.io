# Name: OWmenu.py
# Author: Nick Mynatt
# Purpose: Interactive menu to input Overwatch battle-tags, find SR, and calculate average of multiple players at a time
# Last Modified: 3/17/20


# HOW TO USE:
# Run OWmenu.py


import tkinter as tk
from OWfinder import findSR

# Frame: root
root = tk.Tk()

numberOfPeople = 0

# Dictionary to hold variables of player names (given in Entries)
names = {}

# Initializing dictionary with empty StringVar() variables
for x in range(1, 13):
    names["{}".format(x)] = tk.StringVar()
    names["{}".format(x)].set("")

# Number of people, determines # of entry widgets (given by entry widget)
ppl_var = tk.IntVar()

# Display names in a dictionary up to number in names[num]
def displayNames():
    for x in names:
        if int(x) <= ppl_var.get():
            print ("Player {}: {}".format(x, names[x].get()))

# Update root frame with number of people, called when number of people (ppl_var) changes
def updateEntries(a, b, c):
    num = ppl_var.get()
    if ppl_var.get() >= 12:
        num = 12
    if ppl_var.get() <= 0:
        num = 1

    # forgetting all grids > num
    for x in root.grid_slaves():
        if int(x.grid_info()["row"]) > num:
            x.grid_forget()

    # creating grids equal to num
    for x in range(1, num+1):
        tk.Label(root, text="Player {}:".format(x)).grid(row=x+2,column=0)
        tk.Entry(root, textvariable = names["{}".format(x)]).grid(row=x+2,column=1)

# Close root and open new menu
def calculateData():
    root.quit()
    master = tk.Tk()

    tk.Label(master, text="Player:").grid(row=0, column=0)
    tk.Label(master, text="SR:").grid(row=0, column=1)
    
    print (names)
    name_and_sr = {}
    for x in range(1, ppl_var.get()+1):
        name_and_sr[names["{}".format(x)].get()] = findSR(names["{}".format(x)].get())

    counter = 1
    for key, val in name_and_sr.items():
        tk.Label(master, text="{}".format(key)).grid(row=counter, column=0)
        tk.Label(master, text="{}".format(val)).grid(row=counter, column=1)
        counter += 1

    sum = 0
    for SR in name_and_sr:
        sum += int(name_and_sr[SR])
    
    average = sum / ppl_var.get()

    tk.Label(master, text="Average:").grid(row=0, column=2)
    tk.Label(master, text="{}".format(average)).grid(row=1, column=2)

    master.rowconfigure((0,1), weight=1)  
    master.columnconfigure((0,2), weight=1) 

    master.mainloop()

# Static elements in root frame
tk.Label(root, text="# of people:").grid(row=0, column=0)
tk.Entry(root, textvariable=ppl_var, width=3).grid(row=0, column=1)

tk.Button(root, text="Display Names", command = displayNames).grid(row=0,column=2)
tk.Button(root, text="Calculate SR", command = calculateData).grid(row=0,column=3)

root.rowconfigure((0,1), weight=1)  
root.columnconfigure((0,2), weight=1) 

# Updates frame when number of players changes
ppl_var.trace('w', updateEntries)

root.mainloop()