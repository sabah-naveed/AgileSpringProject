#############################################################################
#  Agile GEDCOM Project                                                     #
#  Sabah Naveed, Parul Mahajan, Manoj Sai Naramreddy, & Dhruvan Dronavalli  #                                                          
#  I pledge my honor that I have abided by the Stevens Honor System.        #
#############################################################################         

#imports
import datetime
from prettytable import PrettyTable
from datetime import datetime, timedelta

#global variables commonly used among stories

validMonths = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

current_year = datetime.now().year
current_month_num = datetime.now().month
current_month = validMonths[current_month_num - 1]
current_day = datetime.now().day

individualTable = PrettyTable()
individualTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

familyTable = PrettyTable()
familyTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

validMonths = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

individuals = []
families = []

indInfo = []
spouseArray = []
famInfo = []
linesIF = []

dead = []

#parse file
def parse_file(filename, individuals, families, indInfo, spouseArray, lessThan150):
    #parse the file and do initial population
    #Input: filename

    validTags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
    f = open(filename, "r")
    contents = f.read()
    lines = contents.splitlines()

    list_deceased(filename)

    rest = ""
    for l in lines:
        if l != "":
          elem = l.rsplit()
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
          if ("DATE" in elem):
            invalid_date(elem[2:])


    indInfo = []
    dateOfBirth = []
    for i in range(len(individuals)):

        rejoinedLine = " ".join(individuals[i])

        indexIndAt = lines.index(rejoinedLine)
        indexIndAtTag = lines[indexIndAt][0]

        tempInd = []

        tempInd.append(lines[indexIndAt])
        indexIndAt += 1

        
        while(lines[indexIndAt][0] != "0"):
            tempInd.append(lines[indexIndAt])
            indexIndAt += 1
    
        indInfo.append(tempInd)

    #getting info needed for fam
    for i in range(len(families)):
    #print(individuals[i][1])
        if 'FAM' in families[i]:
            rejoinedLine = " ".join(families[i])

            indexFamAt = lines.index(rejoinedLine)
            indexFamAtTag = lines[indexFamAt][0]

            tempFam = []

            tempFam.append(lines[indexFamAt])
            indexFamAt += 1

            print(lines)
            while(indexFamAt < len(lines) and lines[indexFamAt][0] != "0"):
            #print("getting fam tab")
                tempFam.append(lines[indexFamAt])
                indexFamAt += 1

                
            
            famInfo.append(tempFam)
    
    f.close()

    
    #do individual table --> print('individual table..', indInfo)
    for i in range(len(indInfo)):
        child = False
        spouse = False
        age = 0
        alive = True
        deathDate = "N/A"
         #print('indInfo of i..', i, indInfo[i])
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
                #print("inside death...", indInfo, i)
                #print("inside indinfo\n", indInfo[i])
                #list_deceased(filename)
                print("DEAT found")
                

        if indInfo[i][4][8] == " " :
            dateOfBirth = indInfo[i][4][13:]
        else:
            dateOfBirth = indInfo[i][4][14:]

    #print('dateOfBirth ..',dateOfBirth)
        age = include_individual_ages(dateOfBirth)
        #print('alive ..',alive)
        if less_than_150_years_old(age):
            lessThan150 += [indInfo[i][0][2:6]]

        print(dead)
        individualTable.add_row([indInfo[i][0][2:6], indInfo[i][1][7:], indInfo[i][2][6:], indInfo[i][4][7:], age, "False" if (indInfo[i][0][2:6] in dead) else "True", deathDate, childFam if child else "N/A" , spouseFam if spouse else "N/A"])
        individuals.append([indInfo[i][0][2:6], indInfo[i][1][7:], indInfo[i][2][6:], indInfo[i][4][7:], age, alive, deathDate, childFam if child else "N/A" , spouseFam if spouse else "N/A"])



    for i in range(len(famInfo)):
        husbID = "N/A"
        wifeID = "N/A"
        marriage = "N/A"
        divorce = "N/A"
        husbName = ""
        wifeName = ""
        children = "{"
        for j in range(len(famInfo[i])):
            # print("fam info.....", famInfo[i])
             #print("-----------")
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
               indexOfMarrDate = famInfo[i].index(next(item for item in famInfo[i] if "MARR" in item))
               # print("index of marr date...", indexOfMarrDate)
                #print("-----------")
               marriage = famInfo[i][indexOfMarrDate+1][6:]
            if "DIV" in famInfo[i][j]:
                #print("indie div value...", famInfo[i][7][6:])
                divorce = famInfo[i][7][6:]
        #  print(" ")
        
    children += "}"

    familyTable.add_row([famInfo[i][0][2:6], marriage, divorce, husbID, husbName, wifeID, wifeName, children])
    families.append([famInfo[i][0][2:6], marriage, divorce, husbID, husbName, wifeID, wifeName, children])
    marriage_after_14(marriage,husbID, wifeID,indInfo)
    list_large_age_differences(husbID, wifeID)

    individualTable.sortby = "ID"
    print(individualTable)
    familyTable.sortby = "ID"
    print(familyTable)

    #LISTING LESS THAN 150 YEARS OLD
    print("Individuals that are less than 150 years old")
    print(lessThan150)

    #LISTING DECEASED INDIVIDUALS
    print("Individuals that have passed away")
    print(dead)

    #large age difference
    

#US01
def dates_before_current_date(filename):
    #Dates (birth, marriage, divorce, death) should not be after the current date
    
    f = open(filename, "r")
    contents = f.read()
    linesUS = contents.splitlines()
    #print(linesUS)
    dateBool = False
    for i in linesUS:
        if dateBool == True:
            if "DATE" in i:
                date = i[7:]
                #put date in correct format 
                date_format = "%d %b %Y"
                date = datetime.strptime(date, date_format)
                today = datetime.today()
                #print(date)
                #print(today)
                if date > today:
                    print("ERROR: US01: The following date is before current date:", date)
                    dateBool = False
        if "BIRT" in i or "MARR" in i or "DIV" in i or "DEAT" in i:
            dateBool = True



#US02
def birth_before_marriage():
    #Birth should occur before marriage of an individual
    #print("individual: \n", individuals)
    bbmList = ["h", "w", "m"]
    #print("family: \n", famInfo)
    marrBool = False
    for i in range(len(famInfo)):
        for j in famInfo[i]:
            if marrBool:
                bbmList[2] = j[7:]
                marrBool = False
            if "HUSB" in j:
                husbID = j[7:]
                bbmList[0] = husbID
                #print("husbID: ", husbID)
            if "WIFE" in j:
                wifeID = j[7:]
                bbmList[1] = wifeID
                #print("wifeID: ", wifeID)
            if "MARR" in j:
                marrBool = True
    #print("bbmList: ", bbmList)
    #find dates of these individuals and compare them
    coupleBirths = ["h", "w"]
    for i in range(len(individuals)):
        if individuals[i][0] == bbmList[0]:
            husbBirth = individuals[i][3]
            coupleBirths[0] = husbBirth
        if individuals[i][0] == bbmList[1]:
            wifeBirth = individuals[i][3]
            coupleBirths[1] = wifeBirth
    #print("coupleBirths: ", coupleBirths)

    #compare dates to see if birth before marriage
    date_format = "%d %b %Y"
    husbBirth = datetime.strptime(husbBirth, date_format)
    wifeBirth = datetime.strptime(wifeBirth, date_format)
    marr = datetime.strptime(bbmList[2], date_format)
    if husbBirth > marr:
        print("ERROR: US02: Birth before marriage for husband")
    if wifeBirth > marr:
        print("ERROR: US02: Birth before marriage for wife")


#US03
def birth_before_death(filename):
    #Birth should occur before death of an individual
    
    print("individual: \n", individuals)
    f = open(filename, "r")
    contents = f.read()
    lines = contents.splitlines()



#US04
def marriage_before_divorce():
    #Marriage should occur before divorce of spouses, and divorce can only occur after marriage
    print("[NOT IMPLEMENTED] US04: Marriage before divorce")

#US05
def marriage_before_death():
    #Marriage should occur before death of either spouse
    print("[NOT IMPLEMENTED] US05: Marriage before death")

#US06
def divorce_before_death():
    #Divorce can only occur before death of both spouses
    print("[NOT IMPLEMENTED] US06: Divorce before death")

#US07
def less_than_150_years_old(a):
    #Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
    #Input: age
    #Output: True or False
    
    if a < 150:
        return True
    else:
        return False


#US08
def birth_before_marriage_of_parents():
    #Children should be born after marriage of parents (and not more than 9 months after their divorce)
    print("[NOT IMPLEMENTED] US08: Birth before marriage of parents")

#US09
def birth_before_death_of_parents():
    #Child should be born before death of mother and before 9 months after death of father
    print("[NOT IMPLEMENTED] US09: Birth before death of parents")

#US10
def marriage_after_14(marriage,husbID, wifeID,indInfo):
    #Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    #print("[IN PROGRESS] US10: Marriage after 14")
   # print("marriage date..", marriage)
   # print("Husb ID..", husbID)
   # print("wide Id..", wifeID)
    for i in range(len(indInfo)):
         #print("indi info inside marriage after 14..", indInfo[i])
        for item in indInfo[i]:
            if husbID in item:
                #print("inside item....,", item)
                indexOfHusbBirth = indInfo[i].index(next(item for item in indInfo[i] if "BIRT" in item))
                #print("index of husb birth...,", indInfo[i][indexOfHusbBirth+1][13:])
                husbDOB = indInfo[i][indexOfHusbBirth+1][13:]
            if wifeID in item:
               # print("inside item wife......,", item)
                indexOfWifeBirth = indInfo[i].index(next(item for item in indInfo[i] if "BIRT" in item))
                #print("index of wife birth...,", indInfo[i][indexOfWifeBirth+1][13:])
                wifeDOB = indInfo[i][indexOfWifeBirth+1][13:]

    marriageDate  = []
    marriageDate = marriage.rsplit()
   # print("marriage date...",marriageDate[2])
    if (len(marriageDate) > 2):
        husbDOBatMarr = int(marriageDate[2]) - int(husbDOB)
        wifeDOBatMarr = int(marriageDate[2]) - int(wifeDOB)
        if(husbDOBatMarr < 14 ):
            print("ERROR: US10 - Husband DOB < 14 at the time of marriage")
        if(wifeDOBatMarr < 14 ):
            print("ERROR: US10 - Wife DOB < 14 at the time of marriage")


#US11
def no_bigamy():
    #Marriage should not occur during marriage to another spouse; No more than one marriage at a time
    print("[NOT IMPLEMENTED] US11: No bigamy")

#US12
def parents_not_too_old():
    #Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
    print("[NOT IMPLEMENTED] US12: Parents not too old")

#US13
def siblings_spacing():
    #Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
    print("[NOT IMPLEMENTED] US13: Siblings spacing")

#US17
def no_marriages_to_descendants():
    #Parents should not marry any of their descendants
    print("[NOT IMPLEMENTED] US17: No marriages to descendants")

#US18
def siblings_should_not_marry():
    #Siblings should not marry one another
    print("[NOT IMPLEMENTED] US18: Siblings should not marry")

#US19
def first_cousins_should_not_marry():
    #First cousins should not marry one another
    print("[NOT IMPLEMENTED] US19: First cousins should not marry")

#US20
def aunts_and_uncles():
    #Aunts and uncles should not marry their nieces or nephews, their siblings’ children
    print("[NOT IMPLEMENTED] US20: Aunts and uncles")

#US22
def unique_ids():
    #All individual IDs should be unique and all family IDs should be unique
    print("[NOT IMPLEMENTED] US22: Unique IDs")

#US23
def unique_name_and_birth_date():
    #No more than one individual with the same name and birth date should appear in a GEDCOM file
    print("[NOT IMPLEMENTED] US23: Unique name and birth date")

#US24
def unique_families_by_spouses():
    #No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
    print("[NOT IMPLEMENTED] US24: Unique families by spouses")

#US27
def include_individual_ages(dob):
    #Include the current ages of all living individuals in the output
    #Input: index of individual
    #Output: age of individual
    return current_year - int(dob)
    

#US29
def list_deceased(filename):
    #List all deceased individuals in a GEDCOM file
    #Input: index of individual
    #Output: dead array
    #print("death date is..",index)
    #print("indiInfo is..",indiInfo)
    
    #go through lines and find individual ids for those who are dead
    
    f = open(filename, "r")
    contents = f.read()
    lines = contents.splitlines()
    currentIndividual = ""
    print("lines are:: ",lines)
    for line in lines:
        #if '0 @Ix@ INDI' type of line reached
        if "INDI" in line:
            currentIndividual = line[2:6]
            print("current individual is:: ",currentIndividual)
        #if '1 DEAT' type of line reached
        if "DEAT" in line:
            #print("DEAT line reached..",line)
            dead.append(currentIndividual)
    print("dead array is:: ",dead)

    

#US30
def list_living_married():
    #List all living married people in a GEDCOM file
    print("[NOT IMPLEMENTED] US30: List living married")

#US31
def list_living_single():
    #List all living people over 30 who have never been married in a GEDCOM file
    print("[NOT IMPLEMENTED] US31: List living single")

#US32
def list_multiple_births():
    #List all multiple births in a GEDCOM file
    print("[NOT IMPLEMENTED] US32: List multiple births")

#US33
def list_orphans():
    #List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
    print("[NOT IMPLEMENTED] US33: List orphans")

#US34
def list_large_age_differences(hID, wID):
    #List all couples who were married when the older spouse was more than twice as old as the younger spouse
    #Input: husband ID, wife ID
    for i in individuals:
        if i[0] == hID:
            husbandAge = i[4]
        if i[0] == wID:
            wifeAge = i[4]

    if husbandAge > wifeAge:
        if husbandAge > 2*wifeAge:
            print("Husband of ID", hID, "is more than twice as old as wife of ID", wID)
        if wifeAge > 2*husbandAge:
            print("Wife of", wID, "is more than twice as old as husband of ID", hID)


#US35
def list_recent_births():
    #List all people in a GEDCOM file who were born in the last 30 days
    for i in individuals:
        if len(i) > 3 and i[3] and i[3] != "N/A":
            #print(i[3])
            #print(current_day, current_month, current_year)

            date_format = "%d %b %Y"
            a = datetime.strptime(i[3], date_format)
            b = datetime.strptime(str(current_day) + " " + str(current_month) + " " + str(current_year), date_format)

            delta = b - a
            #print(delta.days)
            if delta.days < 30 and delta.days > 0:
                print("This person", i[0] , "was born in the last 30 days")


#US36
def list_recent_deaths():
    #List all people in a GEDCOM file who died in the last 30 days
    for i in individuals:
        if len(i) > 3 and i[6] and i[6] != "N/A":
            #print(i[3])
            #print(current_day, current_month, current_year)

            date_format = "%d %b %Y"
            a = datetime.strptime(i[6], date_format)
            b = datetime.strptime(str(current_day) + " " + str(current_month) + " " + str(current_year), date_format)

            delta = b - a
            #print(delta.days)
            if delta.days < 30 and delta.days > 0:
                print("This person", i[0] , "died in the last 30 days")

#US38
def list_upcoming_birthdays():
    #List all living people in a GEDCOM file whose birthdays occur in the next 30 days
    #print(individuals)
    for i in individuals:
        if len(i) > 3 and i[3] and i[3] != "N/A":
            #print(i[3])
            #print(current_day, current_month, current_year)

            date_format = "%d %b %Y"
            birthday = datetime.strptime(i[3], date_format)
            #print(birthday)
            #change year to current year
            birthday = birthday.replace(year = current_year)
            #print(birthday)
            #print("---")
            today = datetime.strptime(str(current_day) + " " + str(current_month) + " " + str(current_year), date_format)

            delta = birthday - today
            #print(delta.days)
            
            if delta.days < 30 and delta.days > 0:
                print(i[1] , "has a birthday in the next 30 days.")

#US39
def list_upcoming_anniversaries():
    #List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days
    
    #print(famInfo)
    #print(spouseArray)
    marriedBool = False
    for i in famInfo[0]:
            #print(i[3])
            #print(current_day, current_month, current_year)
        if marriedBool:
            date_format = "%d %b %Y"
            #print(i[7:])
            anniversary = datetime.strptime(i[7:], date_format)
            #print(anniversary)
            #change year to current year
            anniversary = anniversary.replace(year = current_year)
            #print(birthday)
            #print("---")
            today = datetime.strptime(str(current_day) + " " + str(current_month) + " " + str(current_year), date_format)

            delta = anniversary - today
            #print(delta.days)
            
            if delta.days < 30 and delta.days > 0:
                print("Husband and wife of family", famInfo[0][0][2:6] , "have an anniversary in the next 30 days.")

            marriedBool = False
        if i[2:6] == "MARR":
            #print("marr hit")
            marriedBool = True


#US42
def invalid_date(d):
    #Check for invalid dates
    #input: date in ["day", "month", "year"] format
    if d[1] not in validMonths:
        print("Error: Invalid date; wrong month")
    if int(d[2]) > current_year:
        print("Error: Invalid date; date in the future")
    if int(d[2]) < 1:
        print("Error: Invalid date; date in non-positive year")
    if int(d[2]) % 4 != 0 and d[1] == "FEB" and int(d[0]) > 28:
        print("Error: Invalid date; February has 28 days")
    if d[1] == "FEB" and int(d[0]) > 29:
        print("Error: Invalid date; February has 29 days at most")
    if (d[1] == "APR" and int(d[0]) > 30) or (d[1] == "JUN" and int(d[0]) > 30) or (d[1] == "SEP" and int(d[0]) > 30) or (d[1] == "NOV" and int(d[0]) > 30):
        print("Error: Invalid date; ", d[0], " has 30 days at most")
    
    


def main():
    #main

    outArray = parse_file("gedexample.txt", individuals, families, indInfo, spouseArray, [])
    list_recent_births()
    list_recent_deaths()

    list_upcoming_birthdays()
    list_upcoming_anniversaries()

    dates_before_current_date("gedexample.txt")

    birth_before_marriage()
    birth_before_death("gedexample.txt")


if __name__ == '__main__':
    main()