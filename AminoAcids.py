from EncodingDetails import *
import numpy as np
import sys


def aminoacids(inputcode):
    assert(np.remainder(len(inputcode), 3) == 0)  # Check length is divisible by 3

    original = [0, 0, 0]  # How many [A, C, U] occurrences in original?
    indices = np.zeros(int(len(inputcode)/3))  # Which amino acids occurred in original?

    # Calculate original & indices variables
    for i in range(0, int(len(inputcode)/3)):
        total = 0
        for j in range(0, 3):
            if inputcode[3 * i + 2 - j] == 'G':
                pass
            elif inputcode[3 * i + 2 - j] == 'U':
                total += (4**j)
            elif inputcode[3 * i + 2 - j] == 'C':
                total += (4**j)*2
            elif inputcode[3 * i + 2 - j] == 'A':
                total += (4**j)*3
            else:
                sys.exit('Invalid Input')
        original = np.add(original, acids[encoding[total][0]][encoding[total][1]])
        indices[i] = encoding[total][0]

    lengths = np.zeros(len(indices))  # How many encoding options are these for each acid?

    # Calculate the intermediate number of combinations:
    products = np.zeros(len(indices))
    products[-1] = 1
    for i in range(len(indices)-1, -1, -1):
        lengths[i] = len(acids[int(indices[i])])
        if i < len(indices) - 1:
            products[i] = products[i+1]*lengths[i+1]

    n = int(np.prod(lengths))  # How many possible combinations of acids are there to check?
    print(str(n) + ' possibilities to check')

    solutions = 0  # Total found
    f = open('solutions.txt', 'w')  # Write solutions to file

    attempts = np.zeros(len(lengths))  # Each iteration represented by the attempted index for each acid, contained in list
    for i in range(n):  # Iterate through all combinations of acid encodings

        # # Optional cutoff when sufficient solutions found
        # if solutions == 10000:
        #     print(str(solutions) + ' solutions reached, terminating search...')
        #     break

        # Update progress
        if np.remainder(i+1, 100000) == 0:
            print(str(i+1) + ' possibilities checked, ' + str(solutions) + ' solutions found...')
        # Convert i to attempts list
        attempts[0] = np.floor(i/products[0])
        remaining = i
        for j in range(1, len(lengths)):
            remaining = np.mod(remaining, products[j-1])
            attempts[j] = np.floor(remaining/products[j])

        # Check if number of As match: if not, move to next case
        total = 0
        for j in range(len(lengths)):
            total += acids[int(indices[j])][int(attempts[j])][0]
        if total != original[0]:
            continue

        # Check if number of Cs match: if not, move to next case
        total = 0
        for j in range(len(lengths)):
            total += acids[int(indices[j])][int(attempts[j])][1]
        if total != original[1]:
            continue

        # Check if number of Us match: if not, move to next case
        total = 0
        for j in range(len(lengths)):
            total += acids[int(indices[j])][int(attempts[j])][2]
        if total == original[2]:
            # If we reach here, a solution has been found
            solutions += 1  # Iterate counter
            # Decode solution to base-4 string representation
            output = ''
            for j in range(len(lengths)):
                location = encoding.index((indices[j], attempts[j]))
                for k in range(2, -1, -1):
                    baseout = np.floor(location/4**k)
                    output += bases[int(baseout)]
                    location = location - baseout*4**k
            # print(output)  # Output solution to command line
            f.write(output + '\n')

    print('Process complete.')
    print(str(solutions) + ' solutions found.')
    f.close()


# # Example use:
# inputcode = 'AACGUUUGACCCGCUAUAUUCUUCACUACUACU'
# aminoacids(inputcode)
