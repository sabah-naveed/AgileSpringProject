from prettytable import PrettyTable
import datetime

current_year = datetime.datetime.now().year

x = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
#x.add_row([0, 0, 0, 0, 0, 0, 0, 0, 0])

y = PrettyTable()
y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

spouseArray = []

f = open('gedexample.txt', 'r')

validTags = [
  "INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB",
  "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"
]

individuals = []
families = []

lessThan150 = []
dead = []

#file contents
contents = f.read()

#each line is an element in list
lines = contents.splitlines()

#loop that formats and splits every line according to specs
rest = ""
for l in lines:
  if l != "":
    #print("--> " + l)
    elem = l.rsplit()
    #print('element..',elem)
    #print("-----")
    regular = True
    if ("INDI" in elem):
      individuals += [elem]
    if ("FAM" in elem) or ("FAMC" in elem) or ("FAMS" in elem):
      families += [elem]
      #print("families...", families)
      #print("-----")
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

#print("Indi....", individuals)
#print("Fams.... ", families)

#getting info needed for individuals

#print(lines)


indInfo = []
dateOfBirth = []
for i in range(len(individuals)):
  #print(individuals[i][1])

  rejoinedLine = " ".join(individuals[i])

  indexIndAt = lines.index(rejoinedLine)
  #print(indexIndAt)
  indexIndAtTag = lines[indexIndAt][0]
  #print(indexIndAtTag)

  tempInd = []

  tempInd.append(lines[indexIndAt])
  indexIndAt += 1

  
  while(lines[indexIndAt][0] != "0"):
    tempInd.append(lines[indexIndAt])
    indexIndAt += 1
  
  indInfo.append(tempInd)
 # print("---------")
 # print('Indi info full...',indInfo[0])

  #print('Indi info onlly age...',indInfo[0][4])

#getting info needed for fam
famInfo = []
for i in range(len(families)):
  #print(individuals[i][1])
  if 'FAM' in families[i]:
    #print("fam found")
    rejoinedLine = " ".join(families[i])

    indexFamAt = lines.index(rejoinedLine)
    #print(indexFamAt)
    indexFamAtTag = lines[indexFamAt][0]
    #print(indexIndAtTag)

    tempFam = []

    tempFam.append(lines[indexFamAt])
    indexFamAt += 1

    while(lines[indexFamAt][0] != "0"):
      #print("getting fam tab")
      tempFam.append(lines[indexFamAt])
      indexFamAt += 1
    
    famInfo.append(tempFam)
    #print("---------")
   
f.close()

#do individual table --> print('individual table..', indInfo)
for i in range(len(indInfo)):
  child = False
  spouse = False
  age = 0
  alive = True
  deathDate = "N/A"
   #print('indInfo of i..', indInfo[i])
  for item in indInfo[i]:
    if "FAMS" in item:
      indexOfFamS = indInfo[i].index(next(item for item in indInfo[i] if "FAMS" in item))
      #  print('index is...',indexOfFamS)
      spouse = True
      spouseArray.append(indInfo[i][indexOfFamS][7:])
      spouseArray.append(indInfo[i][0][2:6])
       #print('spouse of i..', spouseArray)
      spouseArray.append(indInfo[i][1][7:])
      spouseFam = "{'" + indInfo[i][indexOfFamS][7:] + "'}"
      #print("spouse array after append.. famS...", spouseArray)
      #print("---------------")
    elif "FAMC" in item:
       #print('inside FAMC..')
      indexOfFamC = indInfo[i].index(next(item for item in indInfo[i] if "FAMC" in item))
      child = True
      childFam = "{'" + indInfo[i][indexOfFamC][7:] + "'}"
    elif "DEAT" in item:
      #print("inside death...")
      alive = False
      deathDate = indInfo[i][6][6:]
      #add to dead array
      dead += [indInfo[i][0][2:6]]

  if indInfo[i][4][8] == " " :
    dateOfBirth = indInfo[i][4][13:]
  else:
    dateOfBirth = indInfo[i][4][14:]

  #print('dateOfBirth ..',dateOfBirth)
  age = current_year - int(dateOfBirth)
  #print('alive ..',alive)
  if age < 150:
    lessThan150 += [indInfo[i][0][2:6]]

  x.add_row([indInfo[i][0][2:6], indInfo[i][1][7:], indInfo[i][2][6:], indInfo[i][4][7:], age, alive, deathDate, childFam if child else "N/A" , spouseFam if spouse else "N/A"])



for i in range(len(famInfo)):
  husbID = "N/A"
  wifeID = "N/A"
  marriage = "N/A"
  divorce = "N/A"
  husbName = ""
  wifeName = ""
  children = "{"
  for j in range(len(famInfo[i])):
    if "CHIL" in famInfo[i][j]:
      children += "'"
      children += famInfo[i][j][7:]
      children += "'"

    if "HUSB" in famInfo[i][j]:
      husbID = famInfo[i][j][7:]
     # print('huband id...',husbID)
      husbName = spouseArray[spouseArray.index(husbID) + 1]

    if "WIFE" in famInfo[i][j]:
      wifeID = famInfo[i][j][7:]
      #print('wifeID id...',wifeID)
      wifeName = spouseArray[spouseArray.index(wifeID) + 1]

    if "MARR" in famInfo[i][j]:
     # print("indie marr value...", famInfo[i][5][6:])
      marriage = famInfo[i][5][6:]
    if "DIV" in famInfo[i][j]:
      # print("indie div value...", famInfo[i][7][6:])
      divorce = famInfo[i][7][6:]
      #  print(" ")
    
  children += "}"

  y.add_row([famInfo[i][0][2:6], marriage, divorce, husbID, husbName, wifeID, wifeName, children])

x.sortby = "ID"
print(x)
y.sortby = "ID"
print(y)

#LISTING LESS THAN 150 YEARS OLD
print("Individuals that are less than 150 years old")
print(lessThan150)

#LISTING DECEASED INDIVIDUALS
print("Individuals that have passed away")
print(dead)

  
#LISTING DECEASED INDIVIDUALS
#print(spouseArray)