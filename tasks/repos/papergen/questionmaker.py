import re
import os
import random

# ---------------------------
# File paths
# ---------------------------
counter_file = "counter.txt"   # Keeps track of how many functions have been added
# Automatically point to papergen.py in the same directory as this script
base_dir = os.path.dirname(__file__)   # folder where your script is located
target_file = os.path.join(base_dir, "papergen.py")  # Python file we will insert new functions into


# ---------------------------
# Counter handling
# ---------------------------
# If counter.txt exists, read the current counter value
# Else, start from 0
if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        count = int(f.read().strip() or 0)
else:
    count = 0


# ---------------------------
# Helper function: next_label
# ---------------------------
def next_label(label: str) -> str:
    """
    Generate the next alphabetical label.
    Works like Excel columns:
    A, B, ..., Z, AA, AB, ..., AZ, BA, ...
    """
    if not label:
        return "A"
    label = list(label.upper())
    i = len(label) - 1
    while i >= 0:
        if label[i] == "Z":   # if current letter is Z, reset to A and carry left
            label[i] = "A"
            i -= 1
        else:
            label[i] = chr(ord(label[i]) + 1)  # move to next character
            return "".join(label)
    return "A" * (len(label) + 1)   # if all were Z → add a new digit (e.g., Z → AA)


# ---------------------------
# Variables (editable by user)
# ---------------------------
question = "find c in 10^2 + 15^2 = z^2"   # Input question template
exception = (2,)                           # Numbers we do NOT want to replace
lr, ur = 10, 20                            # Random number range
label = ""                                 # Starting label (A, B, C, ...)


# ---------------------------
# Build function definition (string)
# ---------------------------
# Function header (e.g., def qestion0():)
new_line = f"def qestion{count}():\n\n"

# Step 1: assign random values for numbers in the question (skip exceptions)
number_re = re.compile(r"\b\d+\b")
for match in number_re.findall(question):
    if match.isnumeric() and int(match) not in exception:
        label = next_label(label)
        new_line += f"\t{label} = random.randint({lr}, {ur})\n\n"

# Step 2: build the actual question string
new_line += "\tq = f\""   # Start f-string
label = ""                # reset labels for string building

# Break down the question into tokens (numbers, words, symbols)
for token in re.findall(r"\d+|[a-zA-Z]+|\S", question):
    if token.isnumeric() and int(token) not in exception:
        label = next_label(label)
        new_line += f"{{{label}}} "   # Insert placeholder for variable
    else:
        new_line += token + " "

# Finalize function body
new_line = new_line.strip() + "\".format(" + ", ".join(
    [chr(c) for c in range(ord("A"), ord("A") + len(set(re.findall(r'\d+', question)))) if chr(c) <= label]
) + ")\n\treturn q\n\n"


# ---------------------------
# Insert the new function into target file
# ---------------------------
with open(target_file, "r+") as f:
    lines = f.readlines()
    # Insert new function at line 15
    lines.insert(21, new_line)
    f.seek(0)
    f.writelines(lines)
    f.truncate()


# ---------------------------
# Update counter file
# ---------------------------
count += 1
with open(counter_file, "w") as f:
    f.write(str(count))


# ---------------------------
# Patch last line of the target file
# ---------------------------
# Add a call to the new question function
with open(target_file, "r+") as f:
    lines = f.readlines()
    if not lines:
        raise ValueError("File is empty!")

    last_line = lines[-2]   # get the second-last line
    if len(last_line) < 16:
        raise ValueError("Last line has fewer than 16 characters.")

    # Insert function call after 15th character
    lines[-3] = last_line[:15] + f"qestion{count-1}(), " + last_line[15:]
    f.seek(0)
    f.writelines(lines)
    f.truncate()
