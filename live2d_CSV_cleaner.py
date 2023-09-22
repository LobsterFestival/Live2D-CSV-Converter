import sys
import pandas as pd
import re

# @author: LobsterMatsuri
# @date: May 7th, 2022
# thanks: @cillia for regression testing 

# CONSTRAINTS
# ID can't be longer than 64 characters, currently just catches and prompts user to shorten Name
# FIXME: Might be able to handle this with shortening ID, but everyone wants different things with that
# ALL IDs need to be unique, import failures will happen if any IDs conflict, the problem is sneaky
# because if you export ArtMesh data only, when you import, a Part (folder) could share the same ID

# If multiple layers or folders share the same NAME before exporting to CSV
# they will automatically be renamed to NAME, NAME2, NAME{n} ...
# But there are cases where we have duplicate malformed names that get their ID's set to ArtMesh{n}
# So when we clean the NAMEs to be compliant, we need to check if we have a duplicate of that name
# We have already updated the ID to be the new name,
# and if we do we need to adjust the ID to be {CLEANED_NAME + occurance_count}
# Two parts named Left Eyelash would become -> Left_Eyelash & Left_Eyelash2
# The handleDuplicates() fuction will take the n-th occurance of a cleaned NAME and fix its id
# it needs the NAME string, the row that it is from, and the occurance number

# Parameters:
# DataFrame : dataframe row, we can edit inplace.
# Index : location of row to modify in place
def cleanText(df, index):
    # Pull 'Name' string out of df structure put into `str`
    str = df.at[index, 'Name']
    # strip leading and trailing whitespace, FIXME: probably a more pythonic way to do this
    str = str.lstrip()
    str = str.rstrip()

    id = df.at[index, 'ID']

    # Don't mess with folder names at all
    if df.at[index, 'Types'] == "PART":
        return

    # Don't edit an ID of a file if its valid, could conflict with Part names
    # e.g ArtMesh called "Belly" might have an ID of "Belly2"
    # because its under the folder "Belly" with an id of "Belly"
    artMeshSubString = "ArtMesh"
    status = id.find(artMeshSubString)
    if status == -1:
        return

    ogStr = str
    # if 'Name' has non ascii characters, ignore them.
    for c in str:
        if 0 <= ord(c) <= 127:
            continue
        else:
            # Non-ASCII characters, dont do anything
            return

    # if NAME has < or > characters rename that substring section to R (<) or L (>)
    # These seem flipped but Live2D uses character based directions {reword this}
    str = str.replace("<", "R")
    str = str.replace(">", "L")

    # WANT: Some people might want the option of having a different prepend than "AM"
    if str[0].isdigit():
        str = "AM" + str

    # if NAME contains spaces, the ID column of that row needs to be changed to name_like_this, name column doesnt need to change.
    str = str.replace(" ", "_")
    # if NAME has any dashes (-) they should be converted to underscore (_)
    str = str.replace("-", "_")
    # strip anything thats not space, _ , or alphanumeric
    str = re.sub(r'\W+', "", str)
    # set the ID to our sanitized string
    # Modify in place
    if len(str) > 64:
        print(
            f"New ID length is greater than 64 Characters! This is not allowed! Shorten the name of {ogStr}, keeping ID as {df.at[index, 'ID']}")
        return
    # if for some reason our new ID is blank (invalid), error and show conflicting 
    if str == "":
        print(f"Invalid Name! Please change the name of \"{ogStr}\", make sure to use alpha numeric characters somewhere in the name <3")
        print(f"Keeping the ID for {ogStr} as {id}")
        return

    df.at[index, 'ID'] = str
    return

# Parameters:
# DataFrame : DataFrame object
# Index: index of current row we are looking at
# dupList : our list of duplicates, yes I know passing it everytime isnt the best way.
# This function will be our set (not really a set) that we use to prevent duplicate IDs
# If duplicates are found, will modify the ID in place
# NOTE: This should be refactored, because doing this for Every ID in the dataframe is not great
# FIXME: / WANT: Look into using an apply() function over the data frame for this maybe at the end?
def handleDuplicates(df, index, dupList):
    # Pull string from dataframe
    strToCheck = df.at[index, 'ID']
    # Temp list used because we dont want to append to dupList unless it is unique
    tempList = list(dupList)
    tempList.append(strToCheck)
    # Check if we already have this item in the list
    dupDict = findDuplicatesWithCount(tempList)
    matched = False
    for key, value in dupDict.items():
        # It is a duplicate
        if strToCheck == key:
            # Append occurance count to ID string to make unique
            matched = True
            strToCheck = strToCheck + str(value)
            # Modify dataframe row in place
            df.at[index, 'ID'] = strToCheck
    # if no matches, add to our list because this is the first occurance.
    if not matched:
        dupList.append(strToCheck)

    return

# Credit: https://thispointer.com/python-find-duplicates-in-a-list-with-frequency-count-index-positions/
# Parameters
# dupList : List we want to check for duplicates
def findDuplicatesWithCount(dupList):
    dictOfElems = dict()
    # Iterate over each element in list
    for elem in dupList:
        # If element exists in dict then increment its value else add it in dict
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1

    # Filter key-value pairs in dictionary. Keep pairs whose value is greater than 1 i.e. only duplicate elements from list.
    dictOfElems = {key: value for key,
                   value in dictOfElems.items() if value > 1}
    # Returns a dict of duplicate elements and thier frequency count
    return dictOfElems


def main():
    # List with one entry to prevent empty list errors, won't match with any ID
    dupList = ["???"]
    df = pd.read_csv(sys.argv[1], index_col=0)
    # loop over all rows, doing our ill work
    df = df.reset_index()  # safety check
    for index, row in df.iterrows():
        cleanText(df, index)
        handleDuplicates(df, index, dupList)

    # now we can write the dataframe to a new CSV file

    # FIXME: another arg for new filename
    filename = "corrected.csv"
    # Need UTF-8 because original file could have non-ascii characters, original file has UNIX line endings
    df.to_csv(filename, encoding='utf-8', index=False, line_terminator='\n')


# eskeetit
main()