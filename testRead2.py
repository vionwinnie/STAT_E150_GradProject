import os.path
import csv


###############################################################################
###############################################################################
###############################################################################
def loadData_csv(filepath: str) -> list:
    # Verify that filepath points to a valid file
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
    if len(nameCountry) > 6 and nameCountry[0:6] == "United":
        if len(nameCountry) > 14 and nameCountry[7:13] == "States":
            nameCountry = "USA"
        elif len(nameCountry) > 14 and nameCountry[7:14] == "Kingdom":
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
        elif dat_raw[idxRaw][idxRaw_country] != \
                dat_raw[idxRaw - 1][idxRaw_country]:
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
                    try:
                        curData = dat_raw[idxRaw][idxRaw_data].split(' ', 1)[0]
                    except:
                        curData = dat_raw[idxRaw][idxRaw_data]

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
                            try:
                                curData = dat_raw[iRow][idxRaw_data].split(' ', 1)[0]
                            except:
                                curData = dat_raw[iRow][idxRaw_data]

                            # Set data
                            dat[idxDat][1][idxDat_country][idxDat_dataset] = curData

                            break

                    break

    return dat
# End of getData_struct20
###############################################################################
###############################################################################
###############################################################################





# Define all data
#   Where is the data held?
folderpath = "C:\\Users\Paul Jonak\\Documents\\STAT_E150__gradProject\\"

#   Describe each data set
#       1 = Under Five Mortality
#       2 = Physician Density
#       3 = EconomicFreedom
nDataset = 3
labelIndicator = [None for x in range(nDataset)]
codeIndicator = [None for x in range(nDataset)]
filename = [None for x in range(nDataset)]
idxRaw_country = [None for x in range(nDataset)] # Column Country
idxRaw_year = [None for x in range(nDataset)] # Column Year
idxRaw_data = [None for x in range(nDataset)] # Data of interest

structData = [None for x in range(nDataset)]
# 10 = organized by country, then year (no gender)
# 11 = same as 10, but with gender
#
# 20 = organized by year, then country (no gender)
#

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





# Grab WHO country codes
dat_WHO_country = loadData_csv(folderpath + "quandl_WHO_codeCountry.csv")
idxWHO_country = 0
idxWHO_code = 1



# Initialize our final matrix
#   Year data
#       What is the earliest year we would be interested in?
yearThresEnd = 2000
#       What is the most recent year we would be interested in?
yearThresStart = 2015

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



# Write to CSV file
#   Open writer
with open('testWrite2.csv','w') as csvfile:
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