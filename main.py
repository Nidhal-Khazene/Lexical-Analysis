import tkinter as tk
from tkinter import filedialog
import re
import string

# clean_paragraph function to remove the Superfluous characters like TAB, comments...
def clean_paragraph(input_string):
    input_string = re.sub(r'\$[^$]*\$(?!\S)', ' ', input_string)
    input_string = re.sub(r'\$[^$]*\$', ' ', input_string)
    input_string = re.sub(r'[\t\n]', ' ', input_string)
    return ' '.join(input_string.split())

# separate_tokens function to seperate every single word with the ending of string character #
def separate_tokens(text):
    result = []
    words = text.split()
    for word in words:
        if re.match(r'^[a-zA-Z]+\.$', word):
            result.append(word[:-1])
            result.append('#.#')
            continue
        if re.match(r'^[-,+]?\d*\.?\d*$', word):
            result.append(word)
            continue
        if re.match(r'^[a-zA-Z]+\d+$', word):
            result.append(word)
            continue
        if re.match(r'^[a-zA-Z]\+\+$', word):
            result.append(word[0])
            result.append('++')
            continue
        current_token = ''
        i = 0
        while i < len(word):
            char = word[i]
            # Handle := case
            if char == ':' and i + 1 < len(word) and word[i + 1] == '=':
                if current_token:
                    result.append(current_token)
                    current_token = ''
                result.append(':=')
                i += 2
                continue
            # Handle numbers with + or - prefix
            if (char in '+-') and i + 1 < len(word) and word[i + 1].isdigit():
                if i == 0 or not word[i - 1].isalnum():
                    num = char
                    i += 1
                    while i < len(word) and (word[i].isdigit() or word[i] == '.'):
                        num += word[i]
                        i += 1
                    result.append(num)
                    current_token = ''
                    continue
            # Handle ++ case
            if char == '+' and i + 1 < len(word) and word[i + 1] == '+':
                if current_token:
                    result.append(current_token)
                    current_token = ''
                if i > 0 and word[i - 1].isalpha():
                    result.append('++')
                else:
                    result.append('+')
                    result.append('+')
                i += 2
                continue
            # Handle <= and >= cases
            if (char == '<' or char == '>') and i + 1 < len(word) and word[i + 1] == '=':
                if current_token:
                    result.append(current_token)
                    current_token = ''
                result.append(char + '=' + '#')
                i += 2
                continue
            # General handling of other characters
            if char in '=+-*/(){,};><&~':
                if current_token:
                    result.append(current_token)
                    current_token = ''
                result.append(char)
            else:
                current_token += char
            i += 1
        if current_token:
            result.append(current_token)
    return '#'.join(result)

# all this functions is related with the lexical analysis algorithm and they are very important for its functionality.
# typeFunction
def typeFunction(index):
    typeArray = ["", "identifier", "", "condition", "condition", "separator", "operator", "unsigned Integer Constant", "", "unsigned Float Constant",
                 "operator", "step", "operator", "step", "signed Integer Constant", "", "signed Float Constant", "separator", "", "ANDLogic", "", "ORLogic", ""]
    return typeArray[index]

# keyword function
def keyword(str):
    keywordList = ["PROGRAM#", "BEGIN#", "END#", "INT#", "REAL#", "BOOLEAN#", "CHAR#", "STRING#", "CONST#", "WHEN#", "DO#", "OTHERWISE#", "EXECUTE#", "FOR#"]
    return str in keywordList

# getEcMatrix
def getEcMatrix(i, j):
    cols = 12
    rows = 23
    EcMatrix = [[None for _ in range(cols)] for _ in range(rows)]
    EcMatrix[0][0] = 12
    EcMatrix[0][1] = 10
    EcMatrix[0][2] = 7
    EcMatrix[0][3] = 6
    EcMatrix[0][4] = 5
    EcMatrix[0][5] = 3
    EcMatrix[0][6] = 17
    EcMatrix[0][7] = 1
    EcMatrix[0][9] = 20
    EcMatrix[0][10] = 18
    EcMatrix[1][2] = 1
    EcMatrix[1][7] = 1
    EcMatrix[1][8] = 2
    EcMatrix[2][2] = 1
    EcMatrix[2][7] = 1
    EcMatrix[2][8] = 22
    EcMatrix[3][5] = 4
    EcMatrix[5][5] = 6 
    EcMatrix[7][2] = 7
    EcMatrix[7][11] = 8
    EcMatrix[8][2] = 9
    EcMatrix[9][2] = 9
    EcMatrix[10][1] = 11
    EcMatrix[10][2] = 14
    EcMatrix[12][0] = 13
    EcMatrix[12][2] = 14
    EcMatrix[14][2] = 14
    EcMatrix[14][11] = 15
    EcMatrix[15][6] = 16
    EcMatrix[16][6] = 16
    EcMatrix[18][10] = 19
    EcMatrix[20][9] = 21
    EcMatrix[21][8] = 2
    if i < rows and j < cols:
        return EcMatrix[i][j]
    else:
        return 0

# tcDecide function
def tcDecide(tc):
    numeric = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    operator = ['*', '/']
    condition = ['<', '>', '!', '=']
    separator = ['{', '}', '(', ')', '[', ']', ';',',']
    Alphabet = list(string.ascii_uppercase)
    decide = ""
    for i in range(len(numeric)):
        if numeric[i] == tc:
            decide = "numeric"
            return decide
    for i in range(len(operator)):
        if operator[i] == tc:
            decide = "operator"
            return decide
    for i in range(len(condition)):
        if condition[i] == tc:
            decide ="condition"
            return decide
    for i in range(len(separator)):
        if separator[i] == tc:
            decide = "separator"
            return decide
    for i in range(len(Alphabet)):
        if Alphabet[i] == tc:
            decide = "alphabet"
            return decide
    return decide

# getTcIndex
def getTcIndex(tc):
    tcMatrix = ["-","+","numeric","operator",":","condition","separator","alphabet","_","|","&","."] 
    for i in range(len(tcMatrix)):
        if tc == tcMatrix[i]:
            return i
        elif tcDecide(tc) == tcMatrix[i]:
            return i
    return 1000        

# LexicalAlgorithm
def lexicalAlgorithm(str):
    Ec = 0
    tc = str[0]
    cpt = 1
    word = tc
    output = ""  # To accumulate the result
    while Ec is not None and tc != '#':
        Ec = getEcMatrix(Ec, getTcIndex(tc))
        tc = str[cpt]
        cpt += 1
        word = word + tc

    if Ec == 0:
        output += f"{word} incorrect\n"
    elif Ec == 1:
        if keyword(word):
            output += f"{word} is a keyword\n"
        elif cpt > 40:
            output += f"the size of identifier {word} is > 40\n"
        else:
            output += f"{word} is a {typeFunction(1)}\n"
    elif Ec == 3 or Ec == 4:
        output += f"{word} is {typeFunction(3)}\n"
    elif Ec == 5 or Ec == 17:
        output += f"{word} is {typeFunction(5)}\n"
    elif Ec == 6 or Ec == 10 or Ec == 12:
        output += f"{word} is {typeFunction(6)}\n"
    elif Ec == 7:
        if cpt > 7:
            output += f"the size of number {word}  is > 7.\n"
        else:
            output += f"{word} is {typeFunction(7)}\n"
    elif Ec == 9:
        if cpt > 7:
            output += f"the size of number {word} is > 7.\n"
        else:
            output += f"{word} is {typeFunction(9)}\n"
    elif Ec == 11 or Ec == 13:
        output += f"{word} is {typeFunction(11)}\n"
    elif Ec == 14:
        if cpt > 7:
            output += f"the size of number {word} is > 7.\n"
        else:
            output += f"{word} is {typeFunction(14)}\n"
    elif Ec == 16:
        if cpt > 7:
            output += f"the size of number {word} is > 7.\n"
        else:
            output += f"{word} is {typeFunction(16)}\n"
    elif Ec == 19:
        output += f"{word} is {typeFunction(19)}\n"
    elif Ec == 21:
        output += f"{word} is {typeFunction(21)}\n"
    else:
        output += f"{word} is incorrect\n"

    return output  # Return the accumulated output

# end of all pseudo program that related with lexical analysis program

# Desktop Application with Tkinter

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("All files", ".*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_box1.delete(1.0, tk.END)
            text_box1.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", ".txt"), ("All files", ".*")])
    if file_path:
        with open(file_path, "w") as file:
            content = text_box1.get(1.0, tk.END)
            file.write(content)

def lexical_analysis():
    input_string = text_box1.get(1.0, tk.END)
    cleaned_result = clean_paragraph(input_string)
    final_result = separate_tokens(cleaned_result)
    
    
    words = [word for word in final_result.upper().split('#') if word]
    words_with_hash = [w + '#' for w in words]
    
    analysis_output = ""

    for i in range(len(words)):
        analysis_output += lexicalAlgorithm(words_with_hash[i])

    text_box2.delete(1.0, tk.END)
    text_box2.insert(tk.END, analysis_output)
    

root = tk.Tk()
root.title("Lexical Analysis")
menuBar = tk.Menu(root)
root.config(menu=menuBar)
file_menu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Exit", command=root.quit)
analysis_menu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Analysis", menu=analysis_menu)
analysis_menu.add_command(label="Lexical Analysis", command=lexical_analysis)
analysis_menu.add_command(label="Syntax Analysis", command=lambda: print("Syntax Analysis"))
analysis_menu.add_command(label="Semantic Analysis", command=lambda: print("Semantic Analysis"))
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y)
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
text_box1 = tk.Text(right_frame, width=50, height=25)
text_box1.pack(side=tk.LEFT, padx=40)
text_box2 = tk.Text(right_frame, width=50, height=25)
text_box2.pack(side=tk.RIGHT, padx=40)
root.mainloop()
