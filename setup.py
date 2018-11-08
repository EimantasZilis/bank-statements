import calendar

"""
Specify parameters for transaction data.
"""

# Specify input/output transaction file directories
inFilePath = 'C:\\Users\\Eimantas\\Desktop\\transactions.txt'
outFilePath = 'C:\\Users\\Eimantas\\Desktop\\transactions.csv'
outPlotPath = 'C:\\Users\\Eimantas\\Desktop\\graphs\\'

# Set debug mode for extra information  
debug = False

# Specify column names to be used in parsed data (i.e. output CSV)
columnDefs = {
    'Date': 'datetime64',
    'Amount': 'float',
    'Type': 'str',
    'Desc': 'str',
    'Original transaction': 'str'
}

# Specify month dictionary 
monthDict = {
    monthName.upper(): monthNumber
    for monthNumber, monthName in enumerate(calendar.month_abbr)
}

# Define type for a given keyword in transaction description
transactionTypesDict = {
    'Eating out': [
        'KFC',
        'MCDONALD',
        'COOPERS',
        'SUSHI',
        'CROSSE',
        'SUBWAY',
        'WASABI',
        'BELL INN',
        'TORTILLA',
        'NANDOS',
        'KOKORO',
        'AMERICAN DINER',
        'LAS IGUANAS',
        'TOP 1 FOREVER RESTAURA',
        'ITSU',
        'FRANKIE & BENNYS',
        'CHINOS',
        'JUST-EAT'
        ],
        
    'Groceries': [
        'SAINSBURYS',
        'TESCO',
        'LIDL',
        'MORRISON',
        'ASDA',
        'BOOTS',
        'WAITROSE',
        'FIVE STARS',
        'HATFIELD',
        'SUPERDRUG',
        'RAY\'S CHEMIST',
        'M&S',
        'CARD FACTORY',
        'THE WORKS',
        'WH SMITH',
        'ST JOHN RETAIL'
        ],
        
    'Travel': [
        'RAIL',
        'TRAIN',
        'TICKET',
        'TFL',
        'TSGN',
        'EAST MIDLANDS TRAI'
        ],
        
    'Holidays': [
        'RYANAIR',
        'NATIONAL EXPRESS',
        'WDFE STANSTED'
        ],

    'Clothes': [
        'SPORTSDIRECT',
        'FRASER',
        'JOHN LEWIS',
        'PRIMARK',
        'DEBENHAMS',
        'NEXT',
        'MARKS&SPENCER',
        'MOSS BROS'
        ],
        
    'Entertainment': [
        'NERO',
        'ODEON',
        'STARBUCKS',
        'MARTINI',
        'LETTUCE',
        'BAR',
        'TEXAN',
        'CHIQUITO',
        'WIBBAS DOWN INN',
        'FIVE GUYS',
        'BLUEBIRD BOATS',
        'ALCHEMIST',
        'GO WILD',
        'THE WHITE SWAN',
        'MAGICMADHOUSE',
        'MUTE SWAN',
        'PIANO WORKS',
        'THE BISHOP'
        ],

    'Home': [
        'ONEPLUS',
        'IKEA',
        'HOMEBASE',
        'ARGOS',
        'AMAZON',
        'ULTIMATESHIELD',
        ],

    'Gym': [
        'MYPROTEIN',
        'NIKE',
        ],
        
    'Other': [
        'FEE',
        'GOOGLE',
        'EURO',
        'OHLSON',
        'CREW EXPERIENCE',
        'UDEMY',
        'HAMLEY\'S OF LONDON',
        'WATERSTONES',
        'POST OFFICE',
        'DRY CLEANERS',
        'THEORY TEST'
        ],
    'Bad': [
        'FASTER PAYMENT RECEIVED'       # Paying into credit card
    ]
}

def inputPath():
    return inFilePath

def outputPath():   
    return outFilePath

def debugMode():
    return debug

def getOutputPlotPath():
    return outPlotPath

def getColumnNames():
    names = []
    for columnDef in columnDefs:
        names.append(columnDef)
    return names

def getColumnTypes():
    types = []
    for cKey in columnDefs:
        types.append(columnDefs[cKey])
    return types

def getTransactionTypeDict():
    return transactionTypesDict

def getMonthDict():
    return monthDict
