import random

# ---------------------------
# Editable variables (easy for your friend to change)
# ---------------------------
tname = "Mid-Term"        # Test name
lname = "maths"           # Subject / Lesson name
cname = "3rd"             # Class or grade
marks = "16"              # Total marks
time = "1 hour"           # Duration of the test
date = "11/9/2025"        # Test date (not inserted yet, but available if needed)

nsections = int(3)        # Number of sections in the paper
nquestionsps = 5          # Number of questions per section


# ---------------------------
# Example question generators
# Each returns a math question string (with random numbers)
# ---------------------------



def question1():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}+{b}=c"   # Example: "12+7=c"

def question2():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}-{b}=c"   # Example: "19-3=c"

def question3():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}*{b}=c"   # Example: "8*4=c"


# ---------------------------
# Helper: generate next label
# Produces "A", "B", ..., "Z", then "AA", "AB", ...
# Used for section labels in the paper
# ---------------------------
def next_label(label: str) -> str:
    if not label:
        return "A"
    label = list(label.upper())
    i = len(label) - 1
    while i >= 0 and label[i] == "Z":
        label[i] = "A"
        i -= 1
    if i >= 0:
        label[i] = chr(ord(label[i]) + 1)
        return "".join(label)
    return "A" * (len(label) + 1)


# ---------------------------
# Main paper generator
# Creates LaTeX code for the test paper
# ---------------------------
def genpap():
    # Base LaTeX template
    template = r"""\documentclass[12pt,a4paper]{article}
% Packages
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{multicol}
\usepackage{amsmath, amssymb}
\usepackage{titlesec}

% Header & Footer
\pagestyle{fancy}
\fancyhf{}

\chead{Test Paper}
\rhead{Date: \_\_\_\_\_\_\_}
\rfoot{Page \thepage}

% Section formatting
\titleformat{\section}{\large\bfseries}{}{0em}{}
\titleformat{\subsection}{\normalsize\bfseries}{}{0em}{}

% Document starts
\begin{document}

% Title Area
\begin{center}
    \Large \textbf{__TNAME__}\\[1ex]
    __LNAME__ \\
    Class: __CNAME__ \\
\end{center}

\vspace{0.2cm}

\noindent Time: __TIME__ \hfill Marks: __MARKS__

\vspace{0.5cm}

% Instructions
\noindent\textbf{Instructions:}
\begin{enumerate}[leftmargin=*]
    \item Attempt all questions.
    \item Show all steps for full credit.
    \item Use of calculator: Allowed/Not Allowed.
\end{enumerate}

\vspace{0.5cm}

% Sections and Questions
"""

    # Replace placeholders with variables
    template = (
        template
        .replace("__TNAME__", tname)
        .replace("__LNAME__", lname)
        .replace("__CNAME__", cname)
        .replace("__TIME__", time)
        .replace("__MARKS__", marks)
    )

    # Section generation
    label = ""
    for _ in range(nsections):
        # Section heading (A, B, C, ...)
        label = next_label(label)
        template += r"\section*{Section " + label + "}\n" + r"\begin{enumerate}" + "\n"

        # Add questions to this section
        for _ in range(nquestionsps):
            template += "\t" + r"\item $" + random.choice(questions) + "$\n"

        template += r"\end{enumerate}" + "\n\n"

    # End of document
    template += "% End\n" + r"\end{document}"

    # Print to console (for quick preview)
    print(template)

    # Save LaTeX file
    with open("test_paper.tex", "w", encoding="utf-8") as f:
        f.write(template)


# ---------------------------
# Program entry point
# ---------------------------
if __name__ == "__main__":
    # Pre-generate a small pool of questions (1 of each type)
    questions = [question1(), question2(), question3()]
    # Build the paper
    genpap()
