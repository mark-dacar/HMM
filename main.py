import random


# Used to manually create the HMM and save it to the file
def createModel():
    print("\n\n\t--Model Creation--\n")

    # Inputs: Takes in the identities of the matrices and the float values of the matrices.
    # Then gets the initial vector.
    inStates = input("Please enter the names of the states, separated by spaces: ")
    states, transitions = inStates.split(" "), []

    inEmits = input("\nPlease enter the names of the emissions, separated by spaces: ")
    print()
    emits, emissions = inEmits.split(" "), []

    numNodes, numEmits = len(states), len(emits)

    # Gets user input to determine whether matrices are ment to be filled manually or
    # randomly generated
    generationSelect = ''
    while generationSelect not in ["MANUAL", "AUTO"]:
        generationSelect = input("\nPlease select how the matrices will be filled." +
                                 "\n\tEnter [MANUAL] to manually input the matrix values." +
                                 "\n\tEnter [AUTO] to generate the matrices randomly." +
                                 "\n\nPlease select a menu option: ")

    # Manual matrix generation
    if generationSelect == "MANUAL":
        for i in range(0, numNodes):
            moves = input("Please enter the transitions for node " + states[i] + ", separated by spaces: ")
            moves, moveVals = moves.split(' '), []
            for j in moves:
                moveVals.append(float(j))

            transitions.append(moveVals)

        for i in range(0, numNodes):
            print()
            eProbs = []
            for j in range(0, numEmits):
                prob = float(input("Please enter the emission chance for " + emits[j] + " on state " + states[i] + ": "))
                eProbs.append(prob)
            emissions.append(eProbs)

    else:
        # Generates each matrix randomly
        transitions = generateRandomMatrix(numNodes, numNodes)
        emissions = generateRandomMatrix(numNodes, numEmits)

    # Setting the initial vector
    initVector, numStart = {}, int(input("\nPlease enter the number of starting states: "))
    print()
    for i in range(0, numStart):
        state, val = input("Please enter the name of the state and its probability, separated by a space: ").split(" ")
        val = float(val)
        initVector[state] = val

    # Saves data to the file
    saveToFile(states, transitions, emits, emissions, initVector)
    return states, transitions, emits, emissions, initVector


# Used to create a matrix with randomized values.
def generateRandomMatrix(length, width):
    matrix = []

    for i in range(0, length):

        # total keeps track of the running total of the values added to a row in the matrix.
        # It is used to make sure that the total probablity will be 1 for every row in the matrix.
        total, row = 0, []

        for j in range(0, width):
            if total != 100:
                if j == width - 1:
                    row.append(float(100 - total) / 100)
                else:
                    val = random.randrange(0, (100 - total))
                    total += val
                    row.append(float(val) / 100)
            else:
                row.append(0.0)

        matrix.append(row)
    return matrix


# Edits either of the matrices by providing tuples
def editModel(states, transitions, emits, emissions, initVector):
    selection = ''
    while selection != "EXIT":
        print("\n\n\t__Model Editting Menu__\n" +
              "To edit the transition matrix, enter [t].\n" +
              "To edit the emissions matrix, enter [e].\n" +
              "To leave the editor, enter [EXIT].")
        selection = input("Please select a menu operation: ")

        if selection == 't':
            print("\n\t--Editing Transition Matrix--\n" +
                  "CAUTION: Changes overwrite save file.\n\n")
            print("Please enter the tuples separated by spaces. Changes will be queued when\n" +
                  "the enter key is pressed.\n" +
                  "Enter tuples in the format: (row,column,value) (...) (...)...\n" +
                  "To finalize the changes, enter [EXIT].\n" +
                  "To cancel the changes, enter [CANCEL].")
            t, changeSet = '', []
            while t not in ["EXIT", "CANCEL"]:
                t = input("C: ")
                if t not in ["EXIT", "CANCEL"]:
                    changeSet = t.split(" ")
                    print("Changes queued.\n")
                elif t == "CANCEL":
                    changeSet = []

            if len(changeSet) > 0:
                for i in range(0, len(changeSet)):
                    changeSet[i] = changeSet[i].replace('(', '')
                    changeSet[i] = changeSet[i].replace(')', '')
                    row, col, val = changeSet[i].split(',')
                    row, col, val = int(row) - 1, int(col) - 1, float(val)

                    transitions[row][col] = val
                saveToFile(states, transitions, emits, emissions, initVector)
            else:
                print("Changes cancelled.")

        elif selection == 'e':
            print("\n\t--Editing Emission Matrix--\n" +
                  "CAUTION: Changes overwrite save file.\n\n")
            print("Please enter the tuples separated by spaces. Changes will be queued when\n" +
                  "the enter key is pressed.\n" +
                  "Enter tuples in the format: (row,column,value) (...) (...)...\n" +
                  "To finalize the changes, enter [EXIT].\n" +
                  "To cancel the changes, enter [CANCEL].")
            e, changeSet = '', []
            while e not in ["EXIT", "CANCEL"]:
                e = input("C: ")
                if e not in ["EXIT", "CANCEL"]:
                    changeSet = e.split(" ")
                    print("Changes queued.\n")
                elif e == "CANCEL":
                    changeSet = []

            if len(changeSet) > 0:
                for i in range(0, len(changeSet)):
                    changeSet[i] = changeSet[i].replace('(', '')
                    changeSet[i] = changeSet[i].replace(')', '')
                    row, col, val = changeSet[i].split(',')
                    row, col, val = int(row) - 1, int(col) - 1, float(val)

                    emissions[row][col] = val
                saveToFile(states, transitions, emits, emissions, initVector)
            else:
                print("Changes cancelled.")


# Rewrites the save file with new data in correct format
def saveToFile(states, transitions, emits, emissions, initVector):
    print("\n\n---File Saving---")
    file = open("Data.txt", "w")

    print("__Saving states.")
    file.write(' '.join(states) + "\nBREAK\n")

    print("__Saving transitions.")
    sTransitions = []
    for i in transitions:
        sStates = []
        for j in i:
            sStates.append(str(j))
        sTransitions.append(' '.join(sStates))
    file.write("\n".join(sTransitions) + "\nBREAK\n")

    print("__Saving emission names.")
    file.write(' '.join(emits) + "\nBREAK\n")

    print("__Saving emissions.")
    sEmissions = []
    for i in emissions:
        sEmits = []
        for j in i:
            sEmits.append(str(j))
        sEmissions.append(' '.join(sEmits))
    file.write("\n".join(sEmissions) + "\nBREAK\n")

    print("__Saving initial vector.")
    length = 0
    for i in initVector:
        file.write(i + " " + str(initVector[i]))
        length += 1
        if length != len(initVector):
            file.write("\n")

    file.close()
    print("\n\t\tSaving procedure complete.")


# Reads data from the file and returns the values stored on the file
def readFile():
    file = open("Data.txt", 'r')
    data = file.read()
    data = data.split("BREAK\n")

    cnt = 0
    for i in data:
        if i[-1:] == '\n':
            data[cnt] = i[0:-1]
        cnt += 1

    # Formatting data into usable format
    states = data[0].split(' ')

    moves, transitions = data[1].split("\n"), []
    for i in moves:
        line, vals = i.split(" "), []
        for d in line:
            vals.append(float(d))
        transitions.append(vals)

    emits = data[2].split(' ')

    signals, emissions = data[3].split('\n'), []
    for i in signals:
        line, vals = i.split(' '), []
        for d in line:
            vals.append(float(d))
        emissions.append(vals)

    nodes, initVector = data[4].split('\n'), {}
    for n in nodes:
        key, val = n.split(" ")
        initVector[key] = float(val)

    return states, transitions, emits, emissions, initVector


# Performs a search loop, finding the most probable path repeatedly for different sequences.
def findPaths(states, transitions, emits, emissions, initVector):
    search = True
    while search:
        print("\n\n\t__Sequence Search__\n")
        sequence = input("Please enter the emission sequence, separated by spaces." +
                         "\nEnter \"EXIT\" to stop exploring sequences: ")

        if sequence == "EXIT":
            search = False
        else:
            print("\nEmission Sequence:\n" + ' '.join(sequence) + "\n")
            sequence = sequence.split(" ")
            if checkEmissions(sequence, emits):
                # Getting the cartesian product of the states
                pathSet = []
                for i in initVector:
                    path, length = [i], 1
                    pathSet.append(path)
                    cartesianProduct(states, sequence, path, pathSet, length)

                # Pruning
                poppedLast, i, limit = False, 0, len(pathSet)
                while i < limit:
                    if poppedLast:
                        i -= 1
                        limit -= 1
                        poppedLast = False

                    # First prunes by length
                    if len(pathSet[i]) != len(sequence):
                        pathSet.pop(i)
                        poppedLast = True

                    # Then prunes by valid transitions
                    elif badTransition(states, transitions, pathSet[i]):
                        pathSet.pop(i)
                        poppedLast = True

                    # Then prunes by valid emissions
                    elif badEmission(states, emits, emissions, pathSet[i], sequence):
                        pathSet.pop(i)
                        poppedLast = True

                    i += 1

                pathProbs = []
                calculateProbabilities(states, transitions, emits, emissions, initVector, sequence, pathSet, pathProbs)

                print("Possible paths and respective probabilities: ")
                for i in range(0, len(pathSet)):
                    print(' '.join(pathSet[i]) + " | " + str(pathProbs[i]))

                print("\n\nThe most probable path for the sequence \"" + ' '.join(sequence) + "\": ")
                max, path = 0, []
                for i in range(0, len(pathProbs)):
                    if pathProbs[i] > max:
                        max = pathProbs[i]
                        path = pathSet[i]
                print(' '.join(path) + " | " + str(max))


# Recursively finds the cartesian product of the states
def cartesianProduct(states, sequence, path, pathSet, length):
    # Creates a cartesian product of the states up to length of the sequence.
    if length == len(sequence):
        return
    else:
        for i in states:
            path.append(i)
            pathSet.append(path[:])
            cartesianProduct(states, sequence, path, pathSet, length + 1)
            path.pop(-1)
        return


# Returns True if the path cannot exist based on the transition matrix
def badTransition(states, transitions, path):
    for i in range(0, len(path) - 1):
        startState, destState = path[i], path[i + 1]
        startState, destState = states.index(startState), states.index(destState)

        if transitions[startState][destState] == 0:
            return True
    return False


# Returns True if the path cannot exist based on emission
def badEmission(states, emits, emissions, path, sequence):
    for i in range(0, len(path)):
        state = states.index(path[i])
        emit = emits.index(sequence[i])

        if emissions[state][emit] == 0:
            return True
    return False


# Checks if the sequence is a valid combination of emissions
def checkEmissions(sequence, emits):
    for i in sequence:
        if i not in emits:
            return False
    return True


# Calculates the probabilities for every path that is passed, storing them into a given list
def calculateProbabilities(states, transitions, emits, emissions, initVector, sequence, pathSet, pathProbs):
    for i in pathSet:
        probability = 0
        for j in range(0, len(sequence)):
            if j == 0:
                state, emit = states.index(i[j]), emits.index(sequence[j])
                probability += (initVector[i[j]] * emissions[state][emit])
            else:
                currentState, lastState, emit = i[j], i[j - 1], sequence[j]
                currentState, lastState = states.index(currentState), states.index(lastState)
                emit = emits.index(emit)
                probability += (transitions[lastState][currentState] * emissions[currentState][emit])
        pathProbs.append(probability)


def main():
    # OUTER LOOP, determines if the program terminates!
    menuSelection = ''
    while menuSelection != "EXIT":
        print("\n\n\t__Main Menu__\n" +
              "To perform operations on the saved model, type [r].\n" +
              "To perform operations on a new model (Overwrites save!), type [n].\n" +
              "To exit the program, type [EXIT].")
        menuSelection = input("Please select a menu operation: ")

        if menuSelection != "EXIT":
            states, transitions, emits, emissions, initVector = "", [], "", [], {}
            if menuSelection == 'r':
                states, transitions, emits, emissions, initVector = readFile()
            elif menuSelection == 'n':
                states, transitions, emits, emissions, initVector = createModel()

            # INNER LOOP, Determines what the program does with the chosen model
            modelSelection = ''
            while modelSelection not in ["EXIT", "BACK"]:
                # Displays the HMM
                print("\nStates:\n" + str(states))

                print("\nTransition Matrix: ")
                for i in transitions:
                    print(i)

                print("\nEmissions:\n" + str(emits))

                print("\nEmission Matrix: ")
                for i in emissions:
                    print(i)

                print("\nInitial Vector:\n" + str(initVector))

                # Begins the operations prompt
                print("\n\n\t__HMM Operations Menu__\n" +
                      "To search for the most probable paths to a sequence, type [s].\n" +
                      "To edit the transmission or emission matrices, type [e].\n" +
                      "To return to model selection, type [BACK].\n" +
                      "To exit the program, type [EXIT].")
                modelSelection = input("Please select a menu operation: ")

                if modelSelection == "EXIT":
                    menuSelection = "EXIT"
                elif modelSelection == 's':
                    findPaths(states, transitions, emits, emissions, initVector)
                elif modelSelection == 'e':
                    editModel(states, transitions, emits, emissions, initVector)


if __name__ == "__main__":
    main()
