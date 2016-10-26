import os.path
import csv


#   Where is the data held?
# folderpath = "C:\\Users\Paul Jonak\\Documents\\STAT_E150__gradProject\\"
folderpath = "C:\\Users\\Paul\\Documents\\Coursework\\2016_3_HarExt_STATS_150_IntermediateStats\\GradProject\\dataAnalysis\\"

#   When gathering the most recent data, how many years back can we search?
maxDiffYear = 5

# What is the most recent year we would be interested in?
yearThresStart = 2015



###############################################################################
###############################################################################
###############################################################################
def loadData_csv(filepath: str) -> list:
    # Verify that filepath points to a valid file
    print("Looking for: " + filepath)
    print("Found? " + str(os.path.isfile(filepath)) )

    if os.path.isfile(filepath) is True:
        # Load data
        with open(filepath, 'r') as f:
            hRead = csv.reader(f)
            return list(hRead)

    else:
        # Invalid filepath
        return [None]
# End of loadData_csv
###############################################################################
###############################################################################
###############################################################################
def adjCountryName(nameCountry: str) -> str:

    nameCountry = nameCountry.lstrip()

    if len(nameCountry) > 6 and nameCountry[0:6] == "United":
        if len(nameCountry) >= 12 and nameCountry[7:13] == "States":
            nameCountry = "USA"
        elif len(nameCountry) >= 13 and nameCountry[7:14] == "Kingdom":
            nameCountry = "UK"
    elif nameCountry == "Russian Federation":
        nameCountry = "Russia"
    elif nameCountry == "Slovakia":
        nameCountry = "Slovak Republic"
    elif nameCountry == "Syrian Arab Republic":
        nameCountry = "Syria"
    elif "(" in nameCountry:
        nameCountry = nameCountry[0:nameCountry.index("(") - 1]
    return nameCountry
# End of adjCountryName
###############################################################################
###############################################################################
###############################################################################
def getData_struct01(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int) -> list:
    # Data is organized by country and year is given in idxRaw_year

    # Go through each row and identify the country
    # Adjust country name if appropriate
    # Find matching year and country in main matrix, dat
    #   Ignore first row - headers
    curYear = idxRaw_year
    if curYear <= yearThresStart and curYear >= yearThresEnd:
        for iRow in range(1,len(dat_raw)):
            nameCountry = dat_raw[iRow][idxRaw_country]

            nameCountry = adjCountryName(nameCountry)

            # Make sure country exists within WHO country list
            for idxWHO in range(1, len(dat_WHO_country)):
                if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                    # Found match by name
                    #   Find match in dat for code
                    codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                    for iCode in range(len(listCountryCode)):
                        if codeCountry == listCountryCode[iCode]:
                            # Found match by code

                            # Define dat indicies
                            idxDat = yearThresStart - curYear
                            idxDat_country = 1 + iCode
                            idxDat_dataset = 2 + iDS

                            # Get data point / observation
                            #   Some data sets report: "mean [95% CI]"
                            #       ex: 91.1 [69.6-118.8]
                            haveData = True
                            if isinstance( dat_raw[iRow][idxRaw_data] ,str ):
                                try:
                                    curData = dat_raw[iRow][idxRaw_data].split(' ', 1)[0]
                                except:
                                    curData = dat_raw[iRow][idxRaw_data]

                                try:
                                    byteTest = curData[0].encode('utf-8')
                                    if byteTest < b"0" or byteTest > b"9":
                                        haveData = False
                                except:
                                    haveData = False

                            else:
                                curData = dat_raw[iRow][idxRaw_data]

                            if haveData:
                                # Set data
                                dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                            break

                    break

    return dat
# End of getData_struct01
###############################################################################
###############################################################################
###############################################################################
def getData_struct10(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int) -> list:
    # Data is organized by country first, and by year secondly
    #   There is no gender information

    # Determine which countries are present, and their index range
    #   Initialize
    iCountry = 0
    I_countryHasCode = [0]
    dataCountry = [None]
    idxCountry_name = 0
    idxCountry_code = 1
    idxCountry_startIdx = 2
    idxCountry_endIdx = 3

    #   Loop through raw data to get indices
    for idxRaw in range(1, len(dat_raw)):
        # Do we have a new country or more data for the previous country?
        #   Get country name and compare to previous entry
        nameCountry = dat_raw[idxRaw][idxRaw_country]

        #   Country name may need to be adjusted
        #       e.g. Russian Federation -> Russia
        nameCountry = adjCountryName(nameCountry)

        #   New country?
        I_new = False
        if idxRaw == 1:
            I_new = True
        elif dat_raw[idxRaw][idxRaw_country] !=                 dat_raw[idxRaw - 1][idxRaw_country]:
            I_new = True

        if I_new:
            # Have a new country
            #   Update storage matrix
            iCountry = iCountry + 1
            I_countryHasCode.append(0)
            dataCountry.append([None for x in range(4)])

            #   Find WHO country code
            for idxWHO in range(1, len(dat_WHO_country)):
                nameCountry_WHO = dat_WHO_country[idxWHO][idxWHO_country]

                if nameCountry == nameCountry_WHO:
                    # Found match
                    #   Record and break the FOR loop (WHO country code)
                    I_countryHasCode[iCountry] = 1
                    dataCountry[iCountry][idxCountry_name] = nameCountry_WHO
                    dataCountry[iCountry][idxCountry_code] = dat_WHO_country[idxWHO][idxWHO_code]
                    dataCountry[iCountry][idxCountry_startIdx] = idxRaw  # Record starting index
                    dataCountry[iCountry][idxCountry_endIdx] = idxRaw  # Record last index

                    break

            if I_countryHasCode[iCountry] == 0:
                # Warn user that this country name is not found in WHO dataset
                print(str(idxRaw) + " - " + nameCountry + " - No match")

                dataCountry[iCountry][idxCountry_name] = nameCountry
                # No country code available
                dataCountry[iCountry][idxCountry_startIdx] = idxRaw  # Record starting index
                dataCountry[iCountry][idxCountry_endIdx] = idxRaw  # Record last index

        elif I_countryHasCode[iCountry] != 0:
            dataCountry[iCountry][idxCountry_endIdx] = idxRaw  # Record last index

        else:
            dataCountry[iCountry][idxCountry_endIdx] = idxRaw  # Record last index

    # We have dataCountry, now what?
    #   dataCountry contains index ranges for each country
    #   We can now go through each year and see if the country has corresponding data
    #       If it does, add to the main matrix
    #
    # Go through dataCountry to fill in dat
    for iCountry in range(len(I_countryHasCode)):
        if I_countryHasCode[iCountry] == 1:
            # nameCountry = dataCountry[iCountry][idxCountry_name] # not used
            codeCountry = dataCountry[iCountry][idxCountry_code]

            # For this country, get starting and ending index corresponding to dat_raw
            #   Loop through these indices to get Year and Data information
            #       Use to fill in dat
            startIdx = dataCountry[iCountry][idxCountry_startIdx]
            endIdx = dataCountry[iCountry][idxCountry_endIdx]

            for idxRaw in range(startIdx, endIdx + 1):
                curYear = int(dat_raw[idxRaw][idxRaw_year])

                # Make sure we are within our year thresholds
                if curYear <= yearThresStart and curYear >= yearThresEnd:
                    # Get data point / observation
                    #   Some data sets report: "mean [95% CI]"
                    #       ex: 91.1 [69.6-118.8]
                    
                    haveData = True
                    if isinstance( dat_raw[idxRaw][idxRaw_data] ,str ):
                        try:
                            curData = dat_raw[idxRaw][idxRaw_data].split(' ', 1)[0]
                        except:
                            curData = dat_raw[idxRaw][idxRaw_data]
                        
                        try:
                            byteTest = curData[0].encode('utf-8')
                            if byteTest < b"0" or byteTest > b"9":
                                haveData = False
                        except:
                            haveData = False
                        
                    else:
                        curData = dat_raw[idxRaw][idxRaw_data]
                    
                    if haveData:
                        # Get dat index to match the year
                        idxDat = yearThresStart - curYear

                        # Get country index
                        for iCode in range(len(listCountryCode)):
                            if codeCountry == listCountryCode[iCode]:
                                # Found match, remember that we have headers
                                #   -> index = 1+iCode

                                # Define dat indicies
                                idxDat_country = 1 + iCode
                                idxDat_dataset = 2 + iDS

                                # Set data
                                dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                                break
    return dat
# End of getData_struct10
###############################################################################
###############################################################################
###############################################################################
def getData_struct20(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int) -> list:
    # Data is organized by year first, and by country secondly
    #   There is no gender information

    # Go through each row and identify the year and country
    # Adjust country name if appropriate
    # Find matching year and country in main matrix, dat
    #   Ignore first row - headers
    for iRow in range(1,len(dat_raw)):
        curYear = int( dat_raw[iRow][idxRaw_year] )
        if curYear <= yearThresStart and curYear >= yearThresEnd:
            nameCountry = dat_raw[iRow][idxRaw_country]

            nameCountry = adjCountryName(nameCountry)

            # Make sure country exists within WHO country list
            for idxWHO in range(1, len(dat_WHO_country)):
                if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                    # Found match by name
                    #   Find match in dat for code
                    codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                    for iCode in range(len(listCountryCode)):
                        if codeCountry == listCountryCode[iCode]:
                            # Found match by code

                            # Define dat indicies
                            idxDat = yearThresStart - curYear
                            idxDat_country = 1 + iCode
                            idxDat_dataset = 2 + iDS

                            # Get data point / observation
                            #   Some data sets report: "mean [95% CI]"
                            #       ex: 91.1 [69.6-118.8]
                            haveData = True
                            if isinstance( dat_raw[iRow][idxRaw_data] ,str ):
                                try:
                                    curData = dat_raw[iRow][idxRaw_data].split(' ', 1)[0]
                                except:
                                    curData = dat_raw[iRow][idxRaw_data]

                                try:
                                    byteTest = curData[0].encode('utf-8')
                                    if byteTest < b"0" or byteTest > b"9":
                                        haveData = False
                                except:
                                    haveData = False

                            else:
                                curData = dat_raw[iRow][idxRaw_data]

                            if haveData:
                                # Set data
                                dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                            break

                    break

    return dat
# End of getData_struct20
###############################################################################
###############################################################################
###############################################################################
def getData_struct30(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int,
                     idxRaw_indicator: int,
                     stringIndicator: str ) -> list:
    # Data is organized by indicator, then country then year

    # Go through each row and match desired indicator
    # If matched, identify the year and country
    # Adjust country name if appropriate
    # Find matching year and country in main matrix, dat
    #   Ignore first row - headers
    
    minColWidth = max(idxRaw_country,idxRaw_year,idxRaw_data,idxRaw_indicator)
    
    for iRow in range(1,len(dat_raw)):
        # Check if indicator matches
        if len(dat_raw[iRow]) >= minColWidth:
            if stringIndicator == dat_raw[iRow][idxRaw_indicator]:
                # Match found!

                curYear = int( dat_raw[iRow][idxRaw_year] )
                if curYear <= yearThresStart and curYear >= yearThresEnd:
                    nameCountry = dat_raw[iRow][idxRaw_country]

                    nameCountry = adjCountryName(nameCountry)

                    # Make sure country exists within WHO country list
                    for idxWHO in range(1, len(dat_WHO_country)):
                        if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                            # Found match by name
                            #   Find match in dat for code
                            codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                            for iCode in range(len(listCountryCode)):
                                if codeCountry == listCountryCode[iCode]:
                                    # Found match by code

                                    # Define dat indicies
                                    idxDat = yearThresStart - curYear
                                    idxDat_country = 1 + iCode
                                    idxDat_dataset = 2 + iDS

                                    # Get data point / observation
                                    #   Some data sets report: "mean [95% CI]"
                                    #       ex: 91.1 [69.6-118.8]
                                    haveData = True
                                    if isinstance( dat_raw[iRow][idxRaw_data] ,str ):
                                        try:
                                            curData = dat_raw[iRow][idxRaw_data].split(' ', 1)[0]
                                        except:
                                            curData = dat_raw[iRow][idxRaw_data]

                                        try:
                                            byteTest = curData[0].encode('utf-8')
                                            if byteTest < b"0" or byteTest > b"9":
                                                haveData = False
                                        except:
                                            haveData = False

                                    else:
                                        curData = dat_raw[iRow][idxRaw_data]

                                    if haveData:
                                        # Set data
                                        dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                                    break

                            break

    return dat
# End of getData_struct30
###############################################################################
###############################################################################
###############################################################################
def getData_struct40(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int ) -> list:
    # Data is organized by country and year (rows are country, columns are year)

    # 
    minColWidth = max(idxRaw_country,idxRaw_data)
    
    for iRow in range(1+idxRaw_year,len(dat_raw)):
        
        if len(dat_raw[iRow]) >= minColWidth:
        
            nameCountry = dat_raw[iRow][idxRaw_country]

            nameCountry = adjCountryName(nameCountry)
            
            # Make sure country exists within WHO country list
            for idxWHO in range(1, len(dat_WHO_country)):
                if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                    # Found match by name
                    #   Find match in dat for code
                    codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                    for iCode in range(len(listCountryCode)):
                        if codeCountry == listCountryCode[iCode]:
                            # Found match by code                            
                            # Ready to go through years
                            for iYR in range(idxRaw_data, min( len(dat_raw[idxRaw_year]) , len(dat_raw[iRow]) ) ):
                                if isinstance( dat_raw[idxRaw_year][iYR] ,str):
                                    try:
                                        curYear = int( dat_raw[idxRaw_year][iYR] )
                                    except:
                                        curYear = 0
                                else:
                                    curYear = dat_raw[idxRaw_year][iYR]
                                
                                if curYear <= yearThresStart and curYear >= yearThresEnd:
                                    # Define dat indicies
                                    idxDat = yearThresStart - curYear
                                    idxDat_country = 1 + iCode
                                    idxDat_dataset = 2 + iDS

                                    # Get data point / observation
                                    #   Some data sets report: "mean== [95% CI]"
                                    #       ex: 91.1 [69.6-118.8]
                                    haveData = True
                                    if isinstance( dat_raw[iRow][iYR] ,str ):
                                        try:
                                            curData = dat_raw[iRow][iYR].split(' ', 1)[0]
                                        except:
                                            curData = dat_raw[iRow][iYR]

                                        try:
                                            byteTest = curData[0].encode('utf-8')
                                            if byteTest < b"0" or byteTest > b"9":
                                                haveData = False
                                        except:
                                            haveData = False

                                    else:
                                        curData = dat_raw[iRow][iYR]

                                    if haveData:
                                        # Set data
                                        dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                            break

                    break
        

    return dat
# End of getData_struct40
###############################################################################
###############################################################################
###############################################################################
def getData_struct41(dat: list, iDS: int,
                     dat_raw: list,
                     idxRaw_country: int,
                     idxRaw_year: int,
                     idxRaw_data: int,
                     idxRaw_indicator: int,
                     stringIndicator: str ) -> list:
    # Data is organized by indicator, then country, then year is columns (plus parsing of years)

    # 
    minColWidth = max(idxRaw_country,idxRaw_data)
    
    for iRow in range(1+idxRaw_year,len(dat_raw)):
        # Check if indicator matches
        if len(dat_raw[iRow]) >= minColWidth:
            if stringIndicator == dat_raw[iRow][idxRaw_indicator]:
                # Match found!
                nameCountry = dat_raw[iRow][idxRaw_country]

                nameCountry = adjCountryName(nameCountry)
                
                # Make sure country exists within WHO country list
                for idxWHO in range(1, len(dat_WHO_country)):
                    if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                        # Found match by name
                        #   Find match in dat for code
                        codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                        for iCode in range(len(listCountryCode)):
                            if codeCountry == listCountryCode[iCode]:
                                # Found match by code                            
                                # Ready to go through years
                                for iYR in range(idxRaw_data, min( len(dat_raw[idxRaw_year]) , len(dat_raw[iRow]) ) ):
                                    if isinstance( dat_raw[idxRaw_year][iYR] ,str):
                                        if (' ' in dat_raw[idxRaw_year][iYR]):
                                            try:
                                                curYear = int( dat_raw[idxRaw_year][iYR].split(' ', 1)[0] )
                                            except:
                                                curYear = 0
                                        else:
                                            try:
                                                curYear = int( dat_raw[idxRaw_year][iYR] )
                                            except:
                                                curYear = 0
                                    else:
                                        curYear = dat_raw[idxRaw_year][iYR]
                                    
                                    if curYear <= yearThresStart and curYear >= yearThresEnd:
                                        # Define dat indicies
                                        idxDat = yearThresStart - curYear
                                        idxDat_country = 1 + iCode
                                        idxDat_dataset = 2 + iDS
    
                                        # Get data point / observation
                                        #   Some data sets report: "mean== [95% CI]"
                                        #       ex: 91.1 [69.6-118.8]
                                        haveData = True
                                        if isinstance( dat_raw[iRow][iYR] ,str ):
                                            try:
                                                curData = dat_raw[iRow][iYR].split(' ', 1)[0]
                                            except:
                                                curData = dat_raw[iRow][iYR]
    
                                            try:
                                                byteTest = curData[0].encode('utf-8')
                                                if byteTest < b"0" or byteTest > b"9":
                                                    haveData = False
                                            except:
                                                haveData = False
    
                                        else:
                                            curData = dat_raw[iRow][iYR]
    
                                        if haveData:
                                            # Set data
                                            dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                                break

                        break
                

    return dat
# End of getData_struct41
###############################################################################
###############################################################################
###############################################################################
def getData_struct42(dat: list, iDS: int,
                         dat_raw: list,
                         idxRaw_country: int,
                         idxRaw_year: int,
                         idxRaw_data: int,
                         idxRaw_indicator: int,
                         stringIndicator: str) -> list:


    # Data is organized by country, then indicator and year are columns

    #
    minColWidth = max( len(dat_raw[idxRaw_year]) , len(dat_raw[idxRaw_indicator]) )

    # Go through columns first to find indicator
    for iCol in range(idxRaw_data,minColWidth):
        if stringIndicator == dat_raw[idxRaw_indicator][iCol]:
            # Match found!
            # Get year
            haveYear = True
            if isinstance(dat_raw[idxRaw_year][iCol], str):
                strYear = dat_raw[idxRaw_year][iCol].lstrip()

                if (' ' in strYear):

                    if len(strYear) >= 7:
                        if strYear[0:7] == "No data":
                            haveYear = False

                    if haveYear:
                        try:
                            curYear = int( strYear.split(' ', 1)[0] )
                        except:
                            haveYear = False
                else:
                    try:
                        curYear = int( dat_raw[idxRaw_year][iCol] )
                    except:
                        haveYear = False
            else:
                try:
                    curYear = int( dat_raw[idxRaw_year][iCol] )
                except:
                    haveYear = False

            if haveYear:
                # Is curYear within our range?
                if curYear <= yearThresStart and curYear >= yearThresEnd:
                    # Get country
                    for iRow in range(1 + idxRaw_year, len(dat_raw)):
                        nameCountry = dat_raw[iRow][idxRaw_country]

                        nameCountry = adjCountryName(nameCountry)

                        # Make sure country exists within WHO country list
                        for idxWHO in range(1, len(dat_WHO_country)):
                            if nameCountry == dat_WHO_country[idxWHO][idxWHO_country]:
                                # Found match by name
                                #   Find match in dat for code
                                codeCountry = dat_WHO_country[idxWHO][idxWHO_code]
                                for iCode in range(len(listCountryCode)):
                                    if codeCountry == listCountryCode[iCode]:
                                        # Found match by code
                                        # Define dat indicies
                                        idxDat = yearThresStart - curYear
                                        idxDat_country = 1 + iCode
                                        idxDat_dataset = 2 + iDS

                                        # Get data point / observation
                                        #   Some data sets report: "mean== [95% CI]"
                                        #       ex: 91.1 [69.6-118.8]haveData = True
                                        haveData = True
                                        if isinstance(dat_raw[iRow][iCol], str):
                                            strData = dat_raw[iRow][iCol].lstrip()

                                            if (' ' in strData):
                                                if len(strData) >= 7:
                                                    if strData[0:7] == "No data":
                                                        haveData = False

                                                if haveData:
                                                    try:
                                                        strData = strData.split(' ', 1)[0]
                                                    except:
                                                        haveData = False

                                            if haveData:
                                                if len(strData) == 3 and strData == "Yes":
                                                    curData = 1
                                                elif len(strData) == 2 and strData == "No":
                                                    curData = 0
                                                else:
                                                    try:
                                                        curData = int( strData )
                                                    except:
                                                        haveData = False
                                        else:
                                            try:
                                                curData = int( dat_raw[iRow][iCol] )
                                            except:
                                                haveData = False

                                        if haveData:
                                            # Set data
                                            dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                                        break
                                break

    return dat
# End of getData_struct42
###############################################################################
###############################################################################
###############################################################################





# Define all data


#   Describe each data set
#       1 = Under Five Mortality
#       2 = Physician Density
#       3 = EconomicFreedom
#       4 = Mean years of schooling, both sexes (William)
#       5 = Mean years of schooling, female (William)
#       6 = Mean years of schooling, male (William)
#       7 = Mean BMI, both sexes (Eric)
#       8 = Mean BMI, male (Eric)
#       9 = Mean BMI, female (Eric)
#       10 = Soft Drinks, thousand hectolitres (Anna)
#       11 = Insufficient Activity, age standardized estimate, both sexes (Anna)
#       12 = Insufficient Activity, age standardized estimate, female (Anna)
#       13 = Insufficient Activity, age standardized estimate, male (Anna)
#       14 = Gross National Income, per capita (Anna)
#       15 = Alcohol Consumption, litres (Anna)
#       16 = Improved Water Exposure, Rural (William)
#       17 = Improved Water Exposure, Urban (William)
#       18 = Improved Water Exposure, Total (William)
#       19 = Life Expectancy at Birth, Both Sexes (William)
#       20 = Life Expectancy at Birth, Female (William)
#       21 = Life Expectancy at Birth, Male (William)
#       22 = Life Expectancy at 60, Both Sexes (William)
#       23 = Life Expectancy at 60, Female (William)
#       24 = Life Expectancy at 60, Male (William)
#       25 = GDP per capita (Ryan)
#       26 = Household COnsumption (Ryan)
#       27 = Women In Parliament
#       28 = Urbanization
#       29 = Happiness, Avg [Life Ladder]
#       30 = Happiness, Freedom to Make Life Choices
#       31 = Total Population
#       32 = Have Program to reduce unhealthy diet (William)
#       33 = Have Program to reduce physical inactivity (William)
#       34 = Have Program to reduce harmful use of alcohol (William)
#       35 = Have Program to reduce cardiovascular disease (William)
#       36 = Have Program to reduce diabetes (William)
#       37 = Have Program to reduce tobacco use (William)
#       38 = McDonalds (Anna)


nDataset = 38
labelIndicator = [None for x in range(nDataset)]
codeIndicator = [None for x in range(nDataset)]
filename = [None for x in range(nDataset)]
idxRaw_country = [None for x in range(nDataset)] # Column Country
idxRaw_year = [None for x in range(nDataset)] # Column Year
idxRaw_data = [None for x in range(nDataset)] # Data of interest
idxRaw_indicator = [None for x in range(nDataset)] # Column indicator
stringIndicator = [None for x in range(nDataset)] # Use if indicators are interspersed

structData = [None for x in range(nDataset)]
# 01 = organized by country, given year
#
# 10 = organized by country, then year (no gender)
# 11 = same as 10, but with gender
#
# 20 = organized by year, then country (no gender)
#
# 30 = organized by indicator, then country then year
#
# 40 = organized by country and year together (country is row, year is column)
# 41 = organized by indicator, then country, then year is columns (plus parsing of years)

iDS = 0
#       Under Five Mortality
labelIndicator[iDS] = "Under Five Mortality (Probability)"
codeIndicator[iDS] = 8
filename[iDS] = 'data_UnderFiveMortality.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 4 # Data of interest

structData[iDS] = 10


iDS = iDS+1
#       Physician Density
labelIndicator[iDS] = "Physician Density"
codeIndicator[iDS] = 52
filename[iDS] = 'data_PhysicianDensity.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 2 # Data of interest

structData[iDS] = 10


iDS = iDS+1
#       EconomicFreedom
labelIndicator[iDS] = "EconomicFreedom"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EconomicFreedom.csv'
idxRaw_country[iDS] = 2 # Column Country
idxRaw_year[iDS] = 0 # Column Year
idxRaw_data[iDS] = 3 # Data of interest

structData[iDS] = 20


iDS = iDS+1
#       Years of schooling (Both Sexes)
labelIndicator[iDS] = "YearsSchooling_BothSexes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_YearsOfSchool_William.csv'
idxRaw_country[iDS] = 3 # Column Country
idxRaw_year[iDS] = 4 # Column Year
idxRaw_data[iDS] = 6 # Data of interest
idxRaw_indicator[iDS] = 1 # Column indicator
stringIndicator[iDS] = "Mean years of schooling (ISCED 1 or higher), population 25+ years, both sexes"

structData[iDS] = 30


iDS = iDS+1
#       Years of schooling (Female)
labelIndicator[iDS] = "YearsSchooling_Female"
codeIndicator[iDS] = 0
filename[iDS] = 'data_YearsOfSchool_William.csv'
idxRaw_country[iDS] = 3 # Column Country
idxRaw_year[iDS] = 4 # Column Year
idxRaw_data[iDS] = 6 # Data of interest
idxRaw_indicator[iDS] = 1 # Column indicator
stringIndicator[iDS] = "Mean years of schooling (ISCED 1 or higher), population 25+ years, female"

structData[iDS] = 30


iDS = iDS+1
#       Years of schooling (Male)
labelIndicator[iDS] = "YearsSchooling_Male"
codeIndicator[iDS] = 0
filename[iDS] = 'data_YearsOfSchool_William.csv'
idxRaw_country[iDS] = 3 # Column Country
idxRaw_year[iDS] = 4 # Column Year
idxRaw_data[iDS] = 6 # Data of interest
idxRaw_indicator[iDS] = 1 # Column indicator
stringIndicator[iDS] = "Mean years of schooling (ISCED 1 or higher), population 25+ years, male"

structData[iDS] = 30


iDS = iDS+1
#       Mean BMI (both sexes)
labelIndicator[iDS] = "MeanBMI_BothSexes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_MeanBMI_Eric.csv'
idxRaw_country[iDS] = 4 # Column Country
idxRaw_year[iDS] = 2 # Column Year
idxRaw_data[iDS] = 7 # Data of interest
idxRaw_indicator[iDS] = 6 # Column indicator
stringIndicator[iDS] = "Both sexes"

structData[iDS] = 30


iDS = iDS+1
#       Mean BMI (female)
labelIndicator[iDS] = "MeanBMI_Female"
codeIndicator[iDS] = 0
filename[iDS] = 'data_MeanBMI_Eric.csv'
idxRaw_country[iDS] = 4 # Column Country
idxRaw_year[iDS] = 2 # Column Year
idxRaw_data[iDS] = 7 # Data of interest
idxRaw_indicator[iDS] = 6 # Column indicator
stringIndicator[iDS] = "Female"

structData[iDS] = 30


iDS = iDS+1
#       Mean BMI (male)
labelIndicator[iDS] = "MeanBMI_Male"
codeIndicator[iDS] = 0
filename[iDS] = 'data_MeanBMI_Eric.csv'
idxRaw_country[iDS] = 4 # Column Country
idxRaw_year[iDS] = 2 # Column Year
idxRaw_data[iDS] = 7 # Data of interest
idxRaw_indicator[iDS] = 6 # Column indicator
stringIndicator[iDS] = "Male"

structData[iDS] = 30


iDS = iDS+1
#       Soft Drinks (thousand hectolitres)
labelIndicator[iDS] = "SoftDrinks_Hectolitres_1000x"
codeIndicator[iDS] = 0
filename[iDS] = 'data_SoftDrinks_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 3 # Data of interest
idxRaw_indicator[iDS] = 2 # Column indicator
stringIndicator[iDS] = "Thousand hectolitres"

structData[iDS] = 30


iDS = iDS+1
#       Insufficient Activity, age standardized (both sexes)
labelIndicator[iDS] = "Insuff_Activity_BothSexes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_InsufficientActivity_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 3 # Data of interest

structData[iDS] = 10


iDS = iDS+1
#       Insufficient Activity, age standardized (female)
labelIndicator[iDS] = "Insuff_Activity_Female"
codeIndicator[iDS] = 0
filename[iDS] = 'data_InsufficientActivity_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 4 # Data of interest

structData[iDS] = 10


iDS = iDS+1
#       Insufficient Activity, age standardized (Male)
labelIndicator[iDS] = "Insuff_Activity_Male"
codeIndicator[iDS] = 0
filename[iDS] = 'data_InsufficientActivity_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Column Year
idxRaw_data[iDS] = 5 # Data of interest

structData[iDS] = 10


iDS = iDS+1
#       Gross National Income, per capita
labelIndicator[iDS] = "NationalIncome"
codeIndicator[iDS] = 0
filename[iDS] = 'data_GrossNationalIncome_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts

structData[iDS] = 40


iDS = iDS+1
#       Alcohol Consumption, litres
labelIndicator[iDS] = "AlcoholConsumption_Litres"
codeIndicator[iDS] = 0
filename[iDS] = 'data_Alochol_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 2 # Row Year
idxRaw_data[iDS] = 3 # Column where data starts

structData[iDS] = 40


iDS = iDS+1
#       Improved Water Exposure, Rural
labelIndicator[iDS] = "ImprovedWater_Rural"
codeIndicator[iDS] = 0
filename[iDS] = 'data_ImprovedWater_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 2 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Improved Water Exposure, Urban
labelIndicator[iDS] = "ImprovedWater_Urban"
codeIndicator[iDS] = 0
filename[iDS] = 'data_ImprovedWater_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 3 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Improved Water Exposure, Total
labelIndicator[iDS] = "ImprovedWater_Total"
codeIndicator[iDS] = 0
filename[iDS] = 'data_ImprovedWater_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at Birth, Both Sexes
labelIndicator[iDS] = "LifeExpectancy_Birth_BothSexes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 2 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at Birth, Female
labelIndicator[iDS] = "LifeExpectancy_Birth_Female"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 3 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at Birth, Male
labelIndicator[iDS] = "LifeExpectancy_Birth_Male"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at 60, BothS exes
labelIndicator[iDS] = "LifeExpectancy_Birth_BothSexes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 5 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at 60, Female
labelIndicator[iDS] = "LifeExpectancy_Birth_Female"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 6 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Life Expectancy at 60, Male
labelIndicator[iDS] = "LifeExpectancy_Birth_Male"
codeIndicator[iDS] = 0
filename[iDS] = 'data_LifeExpectancy_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 7 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       GDP per capita
labelIndicator[iDS] = "GDP"
codeIndicator[iDS] = 0
filename[iDS] = 'data_GDP_Ryan.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 4 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts

structData[iDS] = 40


iDS = iDS+1
#       Household Consumption Expenditure
labelIndicator[iDS] = "HouseholdConsumption"
codeIndicator[iDS] = 0
filename[iDS] = 'data_HHC_Ryan.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 4 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts

structData[iDS] = 40


iDS = iDS+1
#       % Women in Parliament
labelIndicator[iDS] = "WomenInParliament"
codeIndicator[iDS] = 0
filename[iDS] = 'data_WomenInParliament.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 4 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts

structData[iDS] = 40


iDS = iDS+1
#       % Urbanization
labelIndicator[iDS] = "Urbanization_Percent"
codeIndicator[iDS] = 0
filename[iDS] = 'data_Urbanization.csv'
idxRaw_country[iDS] = 2 # Column Country
idxRaw_year[iDS] = 0 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts
idxRaw_indicator[iDS] = 0 # Column indicator
stringIndicator[iDS] = "Urban population (% of total)"

structData[iDS] = 41


iDS = iDS+1
#       Happiness, Avg [Life Ladder]
labelIndicator[iDS] = "Happiness_Avg"
codeIndicator[iDS] = 0
filename[iDS] = 'data_Happiness.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 2 # Column Year
idxRaw_data[iDS] = 3 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Happiness, Freedom to Make Life Choices
labelIndicator[iDS] = "ChoiceFreedom"
codeIndicator[iDS] = 0
filename[iDS] = 'data_Happiness.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 2 # Column Year
idxRaw_data[iDS] = 7 # Column where data starts

structData[iDS] = 10


iDS = iDS+1
#       Total Population
labelIndicator[iDS] = "Population"
codeIndicator[iDS] = 0
filename[iDS] = 'data_Population.csv'
idxRaw_country[iDS] = 2 # Column Country
idxRaw_year[iDS] = 0 # Row Year
idxRaw_data[iDS] = 4 # Column where data starts
idxRaw_indicator[iDS] = 0 # Column indicator
stringIndicator[iDS] = "Population, total"

structData[iDS] = 41


iDS = iDS+1
#       Have program to reduce unhealthy diet
labelIndicator[iDS] = "HaveProgram_BadDiet"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan to reduce unhealthy diet related to NCDs"

structData[iDS] = 42


iDS = iDS+1
#       Have program to reduce physical inactivity
labelIndicator[iDS] = "HaveProgram_PhysicalInactivity"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan to reduce physical inactivity"

structData[iDS] = 42


iDS = iDS+1
#       Have program to reduce harmful use of alcohol
labelIndicator[iDS] = "HaveProgram_Alochol"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan to reduce the harmful use of alcohol"

structData[iDS] = 42


iDS = iDS+1
#       Have program to reduce cardiovascular disease
labelIndicator[iDS] = "HaveProgram_CVD"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan for cardiovascular diseases"

structData[iDS] = 42


iDS = iDS+1
#       Have program to reduce diabetes
labelIndicator[iDS] = "HaveProgram_Diabetes"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan for diabetes"

structData[iDS] = 42


iDS = iDS+1
#       Have program to reduce tobacco use
labelIndicator[iDS] = "HaveProgram_Tobacco"
codeIndicator[iDS] = 0
filename[iDS] = 'data_EduPrograms_William.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 1 # Row Year
idxRaw_data[iDS] = 1 # Column where data starts
idxRaw_indicator[iDS] = 0 # Row indicator
stringIndicator[iDS] = "Existence of operational policy/strategy/action plan to decrease tobacco use"

structData[iDS] = 42


iDS = iDS+1
#       McDonalds
labelIndicator[iDS] = "McDonalds"
codeIndicator[iDS] = 0
filename[iDS] = 'data_McDonalds_Anna.csv'
idxRaw_country[iDS] = 0 # Column Country
idxRaw_year[iDS] = 2012 # Given Year
idxRaw_data[iDS] = 2 # Column data

structData[iDS] = 1





# Grab WHO country codes
dat_WHO_country = loadData_csv(folderpath + "quandl_WHO_codeCountry.csv")
idxWHO_country = 0
idxWHO_code = 1



# Initialize our final matrix
#   Year data
#       What is the most recent year we would be interested in?
# yearThresStart = 2015 # Defined above
#       What is the earliest year we would be interested in?
yearThresEnd = yearThresStart-int(2*maxDiffYear)


#   Country list
#       Only use countries that are within the WHO country code list
listCountry = [None for x in range( len(dat_WHO_country)-1 )]
for i in range(1,len(dat_WHO_country)):
    listCountry[i-1] = dat_WHO_country[i][idxWHO_country]

listCountry = list(set(listCountry))
listCountry.sort()

#   Get a list of country codes
listCountryCode = [None for x in range( len(listCountry) )]
for i in range( len(listCountry) ):
    for i2 in range( len(dat_WHO_country) ):
        if listCountry[i]==dat_WHO_country[i2][idxWHO_country]:
            listCountryCode[i] = dat_WHO_country[i2][idxWHO_code]

#   Ready to initialize
#       [Year] [Country Name] [Country Code] [Indicator 1] [Indicator 2] ...
# dat = [None for x in range( yearThresStart-yearThresEnd+1 )]
dat = [ [None for x in range(2)] for y in range(yearThresStart-yearThresEnd+1) ]
for i in range(yearThresStart-yearThresEnd+1):
    # Set year
    dat[i][0] = yearThresStart-i

    # Set country list
    #   Initialize
    dat[i][1] = [ [None for x in range(2+nDataset)] for y in range(1+len(listCountry)) ]
    #   Set headers
    dat[i][1][0][0] = "Country Name"
    dat[i][1][0][1] = "Country Code"

    for i2 in range(nDataset):
        dat[i][1][0][2+i2] = labelIndicator[i2]

    #   Fill country names and codes
    for i2 in range( len(listCountry) ):
        dat[i][1][1+i2][0] = listCountry[i2]
        dat[i][1][1+i2][1] = listCountryCode[i2]



# Ready to loop through data
for iDS in range(nDataset):
    # Load data
    dat_raw = loadData_csv(folderpath + filename[iDS])

    if len(dat_raw)==1 and dat_raw[0] is None:
        print("No data loaded for: " + labelIndicator[iDS])
    else:
        print("Data loaded for: " + labelIndicator[iDS])



        if structData[iDS] == 10:
            dat = getData_struct10(dat,iDS,dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS] )
        elif structData[iDS] == 20:
            dat = getData_struct20(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS])
        elif structData[iDS] == 30:
            dat = getData_struct30(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS],
                                   idxRaw_indicator[iDS],
                                   stringIndicator[iDS] )
        elif structData[iDS] == 40:
            dat = getData_struct40(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS] )
        elif structData[iDS] == 41:
            dat = getData_struct41(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS],
                                   idxRaw_indicator[iDS],
                                   stringIndicator[iDS] )
        elif structData[iDS] == 42:
            dat = getData_struct42(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS],
                                   idxRaw_indicator[iDS],
                                   stringIndicator[iDS])
        elif structData[iDS] == 1:
            dat = getData_struct01(dat, iDS, dat_raw,
                                   idxRaw_country[iDS],
                                   idxRaw_year[iDS],
                                   idxRaw_data[iDS])



# Find most recent year with BMI data
# For each variable, get most recent data without being more recent than BMI data
haveData = False
strTarget = "BMI"
rYear = 0
rIdx = 0
search_startIdx = 1
search_endIdx = 20
for iCol in range( len(dat[0][1][0] )):
    if strTarget in dat[0][1][0][iCol]:
        # Found match!
        # Get most recent year of data
        for iYr in range(len(dat)):
            for idx in range(search_startIdx,search_endIdx):
                if dat[iYr][1][idx][iCol] is not None:
                    haveData = True
                    rYear = dat[iYr][0]
                    rIdx = iYr

                    break

            if haveData:
                break

        if haveData:
            break

if haveData:
    # For each variable, get most recent data without being more recent than BMI data

    # Initialize
    #   How many rows?
    nRow = len( dat[rIdx][1] )
    #   How many columns?
    nCol = len( dat[rIdx][1][0] )
    #   Initialize
    rDat = [None for x in range(nRow)]
    for iRow in range(nRow):
        rDat[iRow] = [None for x in range(nCol)]

    #   Fill headers
    iRow = 0
    for iCol in range(nCol):
        rDat[iRow][iCol] = dat[rIdx][1][0][iCol]

    #   Fill countries
    for iRow in range(1,nRow):
        rDat[iRow][0] = dat[rIdx][1][iRow][0]

    # Get data
    for iRow in range(1,nRow):
        for iCol in range(1,nCol):
            # Get most recent data

            for iYr in range(rIdx,min(rIdx+maxDiffYear,len(dat))):
                if dat[iYr][1][iRow][iCol] is not None:
                    rDat[iRow][iCol] = dat[iYr][1][iRow][iCol]

                    break

    ###############################################################################
    ###############################################################################
    ###############################################################################

    # Get information to narrow down which variables/countries to use
    import copy
    rDat2 = copy.deepcopy(rDat)
    nCol_ignore = 2
    nRow_ignore = 1

    #   Step 1
    #       Remove variables and countries with less than 10% data
    nRow = len(rDat2)
    nCol = len(rDat2[0])

    nRow_step1_start = nRow
    nCol_step1_start = nCol

    for iCol in range(nCol-nCol_ignore):
        temp = 0
        idx = nCol-1-iCol
        for iRow in range(nRow_ignore,nRow):
            if rDat2[iRow][idx] is not None:
                temp = temp+1

        temp = int(temp/(nRow-nRow_ignore)*100)
        if temp < 10:
            # Delete column
            for iRow in range(nRow):
                del rDat2[iRow][idx]

    nCol = len(rDat2[0])

    for iRow in range(nRow-nRow_ignore):
        temp = 0
        idx = nRow-1-iRow
        for iCol in range(nCol_ignore,nCol):
            if rDat2[idx][iCol] is not None:
                temp = temp+1

        temp = int(temp/(nCol-nCol_ignore)*100)
        if temp < 10:
            # Delete row
            del rDat2[idx]

    nRow = len(rDat2)

    nRow_step1_end = nRow
    nCol_step1_end = nCol


    print("Step 1 - remove <10% data - removed " +
          str(nRow_step1_start-nRow_step1_end) + " rows and " +
          str(nCol_step1_start-nCol_step1_end) + " columns")
    # print("nRow = " + str(nRow_step1_start) + " - nCol = " + str(nCol_step1_start))
    # print("nRow = " + str(nRow_step1_end) + " - nCol = " + str(nCol_step1_end))

    #   Step 2
    #       Remove variables and countries with less than (mean-2*std) data
    import statistics

    nRow_step2_start = nRow
    nCol_step2_start = nCol

    #       Step 2 - countries
    tempList = [None for x in range(nRow-nRow_ignore)]
    for iRow in range(nRow - nRow_ignore):
        idx = nRow - 1 - iRow
        idxList = (nRow-nRow_ignore)-1-iRow

        tempList[idxList] = 0
        for iCol in range(nCol_ignore, nCol):
            if rDat2[idx][iCol] is not None:
                tempList[idxList] = tempList[idxList] + 1

    #           Get threshold
    thres_step2 = statistics.mean(tempList)-2*statistics.stdev(tempList)
    #           Apply threshold
    for iRow in range(nRow - nRow_ignore):
        idx = nRow - 1 - iRow
        idxList = (nRow - nRow_ignore) - 1 - iRow

        if tempList[idxList] < thres_step2:
            # Delete row
            del rDat2[idx]

    nRow = len(rDat2)

    #       Step 2 - variables
    tempList = [None for x in range(nCol - nCol_ignore)]
    for iCol in range(nCol - nCol_ignore):
        idx = nCol - 1 - iCol
        idxList = (nCol-nCol_ignore)-1-iCol

        tempList[idxList] = 0
        for iRow in range(nRow_ignore, nRow):
            if rDat2[iRow][idx] is not None:
                tempList[idxList] = tempList[idxList] + 1

    #           Get threshold
    thres_step2 = statistics.mean(tempList) - 2 * statistics.stdev(tempList)
    #           Apply threshold
    for iCol in range(nCol - nCol_ignore):
        idx = nCol - 1 - iCol
        idxList = (nCol - nCol_ignore) - 1 - iCol

        if tempList[idxList] < thres_step2:
            # Delete column
            for iRow in range(nRow):
                del rDat2[iRow][idx]

    nCol = len(rDat2[0])



    nRow_step2_end = nRow
    nCol_step2_end = nCol

    print("Step 2 - remove <(mean-2*std)% data - removed " +
          str(nRow_step2_start - nRow_step2_end) + " rows and " +
          str(nCol_step2_start - nCol_step2_end) + " columns")
    # print("nRow = " + str(nRow_step2_start) + " - nCol = " + str(nCol_step2_start))
    # print("nRow = " + str(nRow_step2_end) + " - nCol = " + str(nCol_step2_end))



    print("Trimmed results - " + str(nRow_step2_end-nRow_ignore) +
          " countries and " + str(nCol_step2_end-nCol_ignore) + " variables")



    # Get data where each country has values for every variable
    rDat3 = copy.deepcopy(rDat2)
    nRow = len(rDat3)
    nCol = len(rDat3[0])

    for iRow in range(nRow - nRow_ignore):
        idx = nRow - 1 - iRow
        for iCol in range(nCol_ignore, nCol):
            if rDat3[idx][iCol] is None:
                # Delete row
                del rDat3[idx]
                break

    nRow = len(rDat3)

    print("Number of countries with data for every variable = " + str(nRow-nRow_ignore))








###############################################################################
###############################################################################
###############################################################################
# Write to CSV file
#   Open writer
with open('testWrite3_allData.csv','w') as csvfile:
    hWrite = csv.writer(csvfile,delimiter=',',lineterminator='\n')

    # Go through each year and write the data in YrGrp
    for iYr in range( len(dat) ):
        # Do we have any data for this year?
        if dat[iYr][1] != None:
            # Have data

            #   Write data
            cYear = dat[iYr][0]
            for iRow in range( len(dat[iYr][1]) ):
                hWrite.writerow([cYear] + dat[iYr][1][iRow])

with open('testWrite3_mostRecent.csv','w') as csvfile:
    hWrite = csv.writer(csvfile,delimiter=',',lineterminator='\n')

    # Go through each year and write the data in YrGrp
    for iRow in range( len(rDat) ):
        #   Write data
        hWrite.writerow(rDat[iRow])

with open('testWrite3_mostRecent_trim.csv','w') as csvfile:
    hWrite = csv.writer(csvfile,delimiter=',',lineterminator='\n')

    # Go through each year and write the data in YrGrp
    for iRow in range( len(rDat2) ):
        #   Write data
        hWrite.writerow(rDat2[iRow])

with open('testWrite3_mostRecent_trimAllVar.csv','w') as csvfile:
    hWrite = csv.writer(csvfile,delimiter=',',lineterminator='\n')

    # Go through each year and write the data in YrGrp
    for iRow in range( len(rDat3) ):
        #   Write data
        hWrite.writerow(rDat3[iRow])