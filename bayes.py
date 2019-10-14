# Bayes Network
# Author: Marco Mancha

from tkinter import Tk, Frame, Entry, Label, BOTH, Button

# Event names
event1 = "Burglary"
event2 = "Earthquake"
event3 = "Alarm"
event4 = "JohnCalls"
event5 = "MaryCalls"

# Event index of tables
events_n ={
    event1:1,
    event2:2,
    event3:3,
    event4:4,
    event5:5
}

# Tables of probability for each event given other events     
tables = []
table_1 = {event1 + "_True":0.001,event1 + "_False":0.999}
table_2 = {event2 + "_True":0.002,event2 + "_False":0.998}
table_3 = { event3 + "_True": 
                {event1 + "_True": 
                    {event2 + "_True": 0.95,event2 + "_False": 0.94},
                event1 + "_False": 
                    {event2 + "_True":0.29,event2 + "_False":0.001}},
            event3 + "_False" : 
                {event1 + "_True":
                    {event2 + "_True":0.05,event2 + "_False":0.06},
                event1 + "_False":
                    {event2 + "_True":0.71,event2 + "_False":0.999}}}

table_4 = { event4 + "_True": 
                {event3 + "_True":0.9,event3 + "_False":0.05},
            event4 + "_False" : 
                {event3 + "_True":0.1,event3 + "_False":0.95}}

table_5 = { event5 + "_True": 
                {event3 + "_True":0.7,event3 + "_False":0.01},
            event5 + "_False" : 
                {event3 + "_True":0.3,event3 + "_False":0.99}}

tables.append(table_1)
tables.append(table_2)
tables.append(table_3)
tables.append(table_4)
tables.append(table_5)

# Possible operations on the network
operaciones = ["p(B)","p(E)","p(A|B,E)","p(J|A)","p(M|A)"]

# Function to output data on the frame
def get_Data():

    # Obtain data from user input
    alarm_d = str(alarm.get())
    burglary_d = str(burglary.get())
    earth_d = str(earth.get())
    john_d = str(john.get())
    mary_d = str(mary.get())
    
    # Create dictionary with user values
    user = {event1 : burglary_d, event2 : earth_d, event3 : alarm_d, event4 : john_d, event5 : mary_d}
    evidence = {}
    hidden = {}
    unknown_events = []
    # Separate events that are evidence, hidden or an event we are trying to find
    for response in user:
        if user[response] == '':
            hidden[response] = 'Positive'
        elif user[response] == 'Positive' or user[response] == 'Negative':
            hidden[response] = user[response]
        else:
            evidence[response] = "_" + user[response]

    # Create helper variables
    index = len(hidden)
    length = pow(2,index)
    i = 0
    div = {}
    bandera = {}
    j = length

    # Loop to obtain the factor to divide positive probs and negative probs
    for h in hidden:
        j = j / 2
        div[h] = int(j)
        bandera[h] = 0

    # Loop to create the matrix of probabilities
    while i < length:
        row = {}

        # First half of matrix will be for the positive prob
        if i < (length / 2):
            positive = True
        else:
            positive = False
        
        # Create the matrix based on user input
        for h in hidden:
            if bandera[h] == 0:
                if hidden[h] == "Positive":
                    row[h] = "_True"
                else:
                    row[h] = "_False"
            else:
                if hidden[h] == "Positive":
                    row[h] = "_False"
                else:
                    row[h] = "_True"

            # Change the auxiliar variable to alternate between values
            # on the different events
            if (i+1) % div[h] == 0 and bandera[h] == 0:
                bandera[h] = 1
            elif (i+1) % div[h] == 0 and bandera[h] == 1:
                bandera[h] = 0

            row["positive"] = positive 
        unknown_events.append(row)
        i = i + 1

    positive = 0
    negative = 0
    result = 1.0

    # For each possible scenario in unknown variables
    for unknown in unknown_events:
        positive_prob = 1.0
        negative_prob = 1.0
        # For each possible operation in the network
        for op in operaciones:
            event = ""
            f_event = ""
            s_event = ""
            t_event = ""

            if op == "p(B)":
                event = event1 + "_True"

                # Check if the event is an evidence
                try:
                    event = event1 + evidence[event1]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    event = event1 + unknown[event1]
                except:
                    pass
                
                # Check if this scenario corresponds to negative or positive prob
                if not unknown['positive']:
                    negative_prob = negative_prob * tables[0][event]
                else:
                    positive_prob = positive_prob * tables[0][event]

            elif op == "p(E)":
                event = event2 + "_True"

                # Check if the event is an evidence
                try:
                    event = event2 + evidence[event2]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    event = event2 + unknown[event2]
                except:
                    pass
                # Check if this scenario corresponds to negative or positive prob
                if not unknown['positive']:
                    negative_prob = negative_prob * tables[1][event]
                else:
                    positive_prob = positive_prob * tables[1][event]
                
            elif op == "p(A|B,E)":
                f_event = event3 + "_True"
                s_event = event1 + "_True"
                t_event = event2 + "_True"
                # Check if the event is an evidence
                try:
                    f_event = event3 + evidence[event3]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    f_event = event3 + unknown[event3]
                except:
                    pass
                # Check if the event is an evidence
                try:
                    s_event = event1 + evidence[event1]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    s_event = event1 + unknown[event1]
                except:
                    pass
                # Check if the event is an evidence
                try:
                    t_event = event2 + evidence[event2]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    t_event = event2 + unknown[event2]
                except:
                    pass
                # Check if this scenario corresponds to negative or positive prob
                if not unknown['positive']:
                    negative_prob = negative_prob * tables[2][f_event][s_event][t_event]
                else:
                    positive_prob = positive_prob * tables[2][f_event][s_event][t_event]

            elif op == "p(J|A)":
                f_event = event4 + "_True"
                s_event = event3 + "_True"
                # Check if the event is an evidence
                try:
                    f_event = event4 + evidence[event4]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    f_event = event4 + unknown[event4]
                except:
                    pass
                # Check if the event is an evidence
                try:
                    s_event = event3 + evidence[event3]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    s_event = event3 + unknown[event3]
                except:
                    pass
                # Check if this scenario corresponds to negative or positive prob
                if not unknown['positive']:
                    negative_prob = negative_prob * tables[3][f_event][s_event]
                else:
                    positive_prob = positive_prob * tables[3][f_event][s_event]

            elif op == "p(M|A)":
                f_event = event5 + "_True"
                s_event = event3 + "_True"
                # Check if the event is an evidence
                try:
                    f_event = event5 + evidence[event5]
                except:
                    pass
                # Check if the event is a hidden variable
                try:
                    f_event = event5 + unknown[event5]
                except:
                    pass
                # Check if the event is an evidence
                try:
                    s_event = event3 + evidence[event3]
                except:
                   pass
                # Check if the event is a hidden variable
                try:
                    s_event = event3 + unknown[event3]
                except:
                    pass
                # Check if this scenario corresponds to negative or positive prob
                if not unknown['positive']:
                    negative_prob = negative_prob * tables[4][f_event][s_event]
                else:
                    positive_prob = positive_prob * tables[4][f_event][s_event]

        if positive_prob != 1.0:
            # Accumulate the positive probabilities
            positive = positive + positive_prob

        if negative_prob != 1.0:
            # Accumulate the negative probabilities
            negative = negative + negative_prob

    # Sum the positive probabilities to the negative probabilities 
    negative = negative + positive
    final_result = positive / negative
    # Obtain final result
    final_result = final_result * 100
    # Update window
    result_label.configure(text="Result: " + str(round(final_result,4)) + "%")
    result_label.update()

# Create window
window = Tk()
window.title("Bayes Network")
all = Frame(window, background="white")
all.pack(expand=1, fill=BOTH)

# Create labels
text = Label(all, text="Write True or False for evidence", font=("Verdana", 25), foreground="black")
text.grid(column=0, row=0)
text2 = Label(all, text="Write Positive or Negative for Guess", font=("Verdana", 25), foreground="black")
text2.grid(column=0, row=1)
burglary_label = Label(all, text="Burglary: ", font=("Verdana", 25), foreground="black")
burglary_label.grid(column=0, row=2)
earth_label = Label(all, text="Earthquake: ", font=("Verdana", 25), foreground="black")
earth_label.grid(column=0, row=3)
alarm_label = Label(all, text="Alarm: ", font=("Verdana", 25), foreground="black")
alarm_label .grid(column=0, row=4)
john_label = Label(all, text="John Calls: ", font=("Verdana", 25), foreground="black")
john_label.grid(column=0, row=5)
mary_label = Label(all, text="Mary Calls: ", font=("Verdana", 25), foreground="black")
mary_label.grid(column=0, row=6)
result_label = Label(all, text="Result: ", font=("Verdana", 25), foreground="black")
result_label.grid(column=0, row=7)

# Create input fields
burglary = Entry(all, font=("Verdana", 25), foreground="black")
burglary.grid(column=1, row=2)
earth = Entry(all, font=("Verdana", 25), foreground="black")
earth.grid(column=1, row=3)
alarm = Entry(all, font=("Verdana", 25), foreground="black")
alarm.grid(column=1, row=4)
john = Entry(all, font=("Verdana", 25), foreground="black")
john.grid(column=1, row=5)
mary = Entry(all, font=("Verdana", 25), foreground="black")
mary.grid(column=1, row=6)

# Create button 
resultados_button = Button(all, text="Calculate", font=("Verdana", 25), foreground="black", command=get_Data)
resultados_button.grid(column=0, row=8, columnspan=2)
window.mainloop()