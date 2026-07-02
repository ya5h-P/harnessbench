import random

tname = "Mid-Term"
lname = "maths"
cname = "3rd"
marks = "16"
time = "1 hour"
date = "11/9/2025"

nsections = int(3)
nquestionsps = 5


def question1():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}+{b}=c"


def question2():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}-{b}=c"


def question3():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}*{b}=c"


# module-level pool of GENERATORS (not pre-computed strings) so each slot is fresh
QUESTION_GENERATORS = [question1, question2, question3]


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


def genpap():
    template = r"""\documentclass[12pt,a4paper]{article}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{amsmath, amssymb}
\begin{document}
\begin{center}
    \Large \textbf{__TNAME__}\\[1ex]
    __LNAME__ \\
    Class: __CNAME__ \\
\end{center}
\noindent Time: __TIME__ \hfill Marks: __MARKS__
"""
    template = (template.replace("__TNAME__", tname).replace("__LNAME__", lname)
                .replace("__CNAME__", cname).replace("__TIME__", time).replace("__MARKS__", marks))

    label = ""
    for _ in range(nsections):
        label = next_label(label)
        template += r"\section*{Section " + label + "}\n" + r"\begin{enumerate}" + "\n"
        for _ in range(nquestionsps):
            # fresh question generated on demand -> numbers vary every slot
            template += "\t" + r"\item $" + random.choice(QUESTION_GENERATORS)() + "$\n"
        template += r"\end{enumerate}" + "\n\n"

    template += "% End\n" + r"\end{document}"
    print(template)
    with open("test_paper.tex", "w", encoding="utf-8") as f:
        f.write(template)


if __name__ == "__main__":
    genpap()
