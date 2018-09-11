import transaction
import datetime
import setup
import numpy as np

def get():
    """
    Gets data from bank statements in the text file and returns
    parsed data. It gets data based from the inputFilePath from setup
    module. The format of the text file has to be:
    
    2016
    DD MMM XXX WWW ZZZZ 123.4
    DD MMM XXX WWW ZZZZ 567.8
    ...
    ...
    2017
    DD MMM XXX YYY ZZZ 901.3
    ...
    ...
    2018
    ...

    DD = day, MMM = month, XXX, WWW, ZZZ are some text strings.
    Numbers at the end are transaction amounts.
    
    This is terrible implementation, but it will do for now.
    Ideally, we want to point it to a folder with PDF statements and it
    should get the data from there. Something to consider in the future...
        
    Output:
        data                 List of lists containing parsed data
                               - data[0]: dates (str) as dd-mm-yyyy format
                               - data[1]: amounts (int)
                               - data[2]: transaction types (list)
                               - data[3]: transaction descriptions (desc)
                               - data[4]: original transaction lines (string)
    """ 
    year = []
    data = [[],[],[],[],[]]
    sortedData = data
    badLines = 0

    debug = setup.debugMode()
    inputFilePath = setup.inputPath()
    print('Reading transaction data from:\n>',inputFilePath)
    with open(inputFilePath,"r") as inputFile:
        lines = inputFile.readlines()
        print(len(lines),'transaction lines found.\n')

        for line in lines:
            line = line.strip('\n')
            
            # Get year
            checkYear = line[:4]
            if (checkYear == '2017') or (checkYear == '2018'):
                year = checkYear
                badLines += 1           
                continue
            elif not(line):
                badLines += 1
                continue                
            
            processedLine, error = transaction.process(line, year)
            if error:
                if debug:
                    print('Ignoring bad transaction line:')
                    print(' > Date:',processedLine[0].strftime("%d-%m-%Y"))
                    print(' > Amount:',processedLine[1])
                    print(' > Description:',processedLine[3],'\n')
                badLines += 1
                continue
            
            for xl in range(5):
                data[xl].append(processedLine[xl])

    print(badLines,'bad lines found and ignored.')
    print('Sorting',len(data[0]),'transaction lines by date...\n')
    
    dateArray = np.array(data[0])
    sortOrder = dateArray.argsort()
    for xl in range(len(data)):
        dataArray = np.array(data[xl])
        sortedData[xl] = dataArray[sortOrder].tolist()
    
    # Convert datetime object into dd-mm-yyyy format
    newDateFormat = [date.strftime("%d-%m-%Y") for date in sortedData[0]]
    sortedData[0] = newDateFormat
    return sortedData


def writeCSV(columns=[]):
    """
    Write data to CSV to path specified in setup module.
    Input:
        columns            Data to write under each column
    """
    
    columnCount = len(columns)
    if not(columnCount):
        print('No data given to write to CSV.')
        print(' > Check input data.')
        return

    # Get file info
    outputFilePath = setup.outputPath()
    outputFile = open(outputFilePath,"w")
        
    # Write column names
    columnNames =  ['Date', 'Amount', 'Type', 'Desc', 'Original transaction']
    outputFile.write(','.join(columnNames))
    outputFile.write('\n') 

    # All columns should have the same nuber of rows
    rowCount = len(columns[0])   
    for xr in range(rowCount):
        row = [str(column[xr]) for column in columns]
        outputFile.write(','.join(row))
        outputFile.write('\n')

    outputFile.close()
    print('Wrote',rowCount,'rows of data to:\n>',outputFilePath,'\n')
    return
    
