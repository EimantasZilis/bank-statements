import calendar

"""
Specify parameters for transaction data.
"""

# Specify input/output transaction file directories
inFilePath = 'C:\\Git\\bank-statements\\all_transactions.csv'
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
        'THE JOLLY COOPERS DRINKING',
        'SUSHI',
        'CROSSE',
        'SUBWAY',
        'WASABI',
        'BELL INN',
        'TORTILLA',
        'NANDOS',
        'KOKORO',
        'AMERICAN DINER',
        'FOREVER RESTAURA',
        'LAS IGUANAS',
        'TOP 1 FOREVER RESTAURA',
        'ITSU',
        'FRANKIE & BENNYS',
        'CHINOS',
        'JUST-EAT',
        'JUST EAT EXPRESS',
        'WRAP IT UP CANNON',
        'PIAZZA FIRENZE HAMPTON'
        'WINE & DELI CROYDON',
        'THE JOLLY COOPERS',
        'PLENTY HAMPTON'
        'PAPA JOHNS',
        'THE REAL CHINA HATFIELD',
        'SUBWAY EATING PLACES',
        'NANDOS',
        'KOKORO',
        'MCDONALDS',
        'FIVE GUYS',
        'PAPAJOHNS',
        'PIAZZA FIRENZE',
        'PLENTY HAMPTON',
        'LTR UK LUTON'
        ],
        
    'Groceries': [
        'SAINSBURYS',
        'TESCO',
        'LIDL',
        'MORRISON',
        'ASDA',
        'WAITROSE',
        'FIVE STARS',
        'M&S',
        'THE WORKS',
        'ST JOHN RETAIL',
        'WONDERTREE',
        'HOSTEL WORLD DUBLIN',
        'CO-OP GROUP'
        ],

    'Health and beauty': [
        'BOOTS',
        'SUPERDRUG',
        'RAY\'S CHEMIST',
        'MYPROTEIN',
        'CREW EXPERIENCE',
        'CREW EXPERIENCE BEAUTY AND BARBER',
        'PULSE CARSHALTON MEMBERSHIP CLUBS',
        'PEARL CHEMIST'
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
        'WDFE STANSTED',
        'USCUSTOMS ESTA',
        'LOVE HOLIDAYS TRAVEL AGENCIES',
        'AIRASIA',
        'NON-STERLING TRANSACTION'
        'AIR CHINA',
        'WIZZ AIR'
        ],

    'Clothes': [
        'SPORTSDIRECT',
        'FRASER',
        'JOHN LEWIS',
        'PRIMARK',
        'DEBENHAMS',
        'NEXT',
        'MARKS&SPENCER',
        'MOSS BROS',
        'NIKE'
        ],
        
    'Entertainment': [
        'NERO',
        'ODEON',
        'STARBUCKS',
        'WINE & DELI',
        'MARTINI',
        'MOONSHINE RACEWAY'
        'LETTUCE',
        'TEXAN',
        'ADVENTURE BAR'
        'CHIQUITO',
        'WIBBAS DOWN INN',
        'BLUEBIRD BOATS',   
        'ALCHEMIST',
        'GO WILD',
        'THE WHITE SWAN',
        'MOONSHINE RACEWAY'
        'SLUG AND LETTUCE'
        'CHIQUITO',
        'CHIQUITO 2025 O2'
        'SLUG AND LETTUCE LONDON'
        'ADVENTURE BAR LONDON',
        'MAGICMADHOUSE',
        'MUTE SWAN',
        'PIANO WORKS',
        'THE BISHOP',
        'SUBURBAN BAR EATING PLACES',
        'CHRISTOPHERS EATING PLACES',
        'THE FOUR THIEVES',
        'HAWKER HOUSE LONDON',
        'ALL BAR ONE',
        'SMITHFIELD',
        'BARRIO CENTRAL LONDON',
        'DIRTY MARTINI',
        'SUBURBAN BAR'
        ],

    'Home': [
        'ONEPLUS',
        'IKEA',
        'HOMEBASE',
        'ARGOS',
        'AMAZON',
        'ULTIMATESHIELD',
        'WILKO HOUSEHOLD',
        'AMZN Mktp UK BOOK STORES',
        'CARD FACTORY',
        'WH SMITH',
        'QUEENS ROAD LONDON'
        ],
        
    'Other': [
        'FEE',
        'GOOGLE',
        'EURO',
        'OHLSON',
        'UDEMY',
        'HAMLEY\'S OF LONDON',
        'WATERSTONES',
        'POST OFFICE',
        'DRY CLEANERS',
        'THEORY TEST',
        'NON-STERLING TRANSACTION',
        'VODAFONE LIMITED',
        'DVLA DRIVER',
        'HAMPTON & RICHMOND HAMPTON'
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
