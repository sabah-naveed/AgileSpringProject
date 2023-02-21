# Sabah Naveed
# I pledge my honor that I have abided by the Stevens Honor System.
# Project 2
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
#x.add_row([0, 0, 0, 0, 0, 0, 0, 0, 0])

print(x) 

f = open('gedexample.txt', 'r')

validTags = [
  "INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB",
  "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"
]

individuals = []
families = []

#file contents
contents = f.read()

#each line is an element in list
lines = contents.splitlines()

#loop that formats and splits every line according to specs
rest = ""
for l in lines:
  if l != "":
    print("--> " + l)
    elem = l.rsplit()
    #print(elem)
    regular = True
    if ("INDI" in elem):
      individuals += [elem]
    if ("FAM" in elem) or ("FAMC" in elem) or ("FAMS" in elem):
      families += [elem]
    if elem:
      if elem[1] in validTags:
        valid = "T"
      else:
        if len(elem) > 2 and elem[2] in validTags:
          valid = "T"
          regular = False
        else:
          valid = "F"
      for i in elem[2:]:
        rest += i
        rest += " "

      #if regular:
      #print("<-- " + elem[0] + "|" + elem[1] + "|" + valid + "|" + rest)
      #else:
      #print("<-- " + elem[0] + "|" + elem[2] + "|" + valid + "|" + elem[1])
      #rest = ""

print("Indi....", individuals)
print("Fams.... ", families)

#printing the individual table
indInfo = []
print(lines)
for i in range(len(individuals)):
  #print(individuals[i][1])

  rejoinedLine = " ".join(individuals[i])

  indexIndAt = lines.index(rejoinedLine)
  print(indexIndAt)
  indexIndAtTag = lines[indexIndAt][0]
  #print(indexIndAtTag)

  tempInd = []

  tempInd.append(lines[indexIndAt])
  indexIndAt += 1

  
  while(lines[indexIndAt][0] != "0"):
    tempInd.append(lines[indexIndAt])
    indexIndAt += 1
  
  indInfo.append(tempInd)
  print("---------")
  print(indInfo)

f.close()

#do individual table

for i in range(len(indInfo)):
  child = False
  spouse = False

  if "FAMS" in indInfo[i][5]:
    spouse = True
    spouseFam = "{'" + indInfo[i][5][7:] + "'}"
  elif "FAMC" in indInfo[i][5]:
    child = True
    childFam = "{'" + indInfo[i][5][7:] + "'}"

  x.add_row([indInfo[i][0][2:6], indInfo[i][1][7:], indInfo[i][2][6:], indInfo[i][4][7:], 0, 0, 0, childFam if child else "N/A" , spouseFam if spouse else "N/A"])

x.sortby = "ID"
print(x)
