import mdmake

doc =""
with open("input.txt", "r") as inputFile:
    doc=inputFile.read()

with open("input.txt","w") as outputFile:
    outputFile.write(mdmake.clear_input_space(doc))