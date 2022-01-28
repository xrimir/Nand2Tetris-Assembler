import sys

filename = sys.argv[-1]
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
}


def strip(l):
    char = l[0]
    if char == "\n" or char == "/":
        return ""
    elif char == " ":
        return strip(l[1:])
    else:
        return char + strip(l[1:])


def translate_a(l):
    if "@" in l:
        x = l.split("@")[1]
        x = table[x]
        address = bin(int(x))[2:]
        trans_a = address.zfill(16)
    elif "(" in l:
        x = l[1:-1]
        x = table[x]
        address = bin(int(x))[2:]
        trans_a = address.zfill(16)
    return trans_a


def translate_c(l):
    trans_c = ""
    if ";" in l:
        line_splat = l.split(";")
        jump_c = jump[line_splat[1]]
        if line_splat[0] in comp.keys():
            trans_c = "111" + comp[line_splat[0]] + "000" + jump_c
    elif "=" in l:
        line_splat = l.split("=")
        trans_c = "111" + comp[line_splat[1]] + dest[line_splat[0]] + "000"
    return trans_c


# Label
def zero_pass():
    with open(filename, 'r') as f:
        counter = 0
        for line in f:
            strippedLine = strip(line)
            if strippedLine:
                if strippedLine[0] == "(":
                    if strippedLine[1:-1] not in table.keys():
                        name = strippedLine[1:-1]
                        table[name] = counter
                else:
                    counter += 1


def first_pass():
    with open(filename, 'r') as f:
        memoryLocation = 16
        for line in f:
            strippedLine = strip(line)
            if strippedLine and strippedLine[0] == "@":
                if strippedLine[1:] not in table.keys():
                    name = strippedLine[1:]
                    table[name] = memoryLocation
                    memoryLocation += 1


def main():
    with open(filename, 'r') as f:
        o = open(f"{filename.split('.asm')[0]}.hack", "w")
        for line in f:
            translated = ""
            strippedLine = strip(line)
            if strippedLine:
                if strippedLine[0] == "@":
                    translated = translate_a(strippedLine)
                    o.write(translated + "\n")
                elif ";" in strippedLine or "=" in strippedLine:
                    translated = translate_c(strippedLine)
                    o.write(translated + "\n")
        o.close()


zero_pass()
first_pass()
main()
