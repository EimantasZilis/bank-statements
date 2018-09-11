import re
import datetime
import calendar

# Define mapping between month names and their numbers
monthDict = {
    monthName.upper(): monthNumber
    for monthNumber, monthName in enumerate(calendar.month_abbr)
}

# Define type for a given keyword in transaction description
typesDict = {
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

def getTypes(txt):
    """
    Given transaction description txt, it finds matching transaction
    types based on typesDict.

    If more than one type is found, it will return types.
    If no matching type is found, it will return 'Unspecified'

    Input:
        txt        Transaction description
    Output:
        types      Transaction types
    """
    if isinstance(txt, list):
        txt = ' '.join(txt)
        
    types = []
    for transType in typesDict:
        keywords = typesDict[transType]
        for keyword in keywords:
            found = re.search(keyword, txt, re.IGNORECASE)
            if found and transType not in types:
                types.append(transType)
                
    if not(types):
        types = 'Unspecified'
    return types

def parseLine(line, year):
    """
    Parse transaction line into useable info.
    It expects the line to be of the form of:
    DD MMM DD MMM TEXT TEXT ... TEXT AMOUNT
    The first DD MMM represents transaction day and month. 

    Input:
        line            Space-delimited transaction line (string)
        year            Year for transaction line 
    Output:
        Date            Returned as datetime object
        Amount
        Description
    """
    transaction = line.split(" ")

    # Convert date string into datetime object
    year_int = int(year)
    day_int = int(transaction[0])
    month_str = transaction[1].upper()
    month_int = monthDict[month_str]
    date = datetime.date(year_int, month_int, day_int)

    amount = transaction[-1]
    description = ' '.join(transaction[5:-1])
    return date, amount, description


def process(line,year):
    """
    Processes transaction line and validates it.
    Returns a list with broken down details of transaction
    Input:
        line        Space-delimited transaction line (string)
        year        Year for transaction line
    Output:
        newLine     List that contains:
                        - Transaction date (datetime object)
                        - Amount
                        - Transaction type
                        - Transaction text
                        - Original transaction line
        error       Error text. Line should be ignored if there are errors      
                                    
    """
  
    # Remove any unexpected commas.
    # They will cause problems if later exported into CSV.
    # Might want to generalise and return alphanumberic chars?
    line = re.sub(',', '', line)

    error = ''
    transDate, transAmount, transText = parseLine(line, year)
    transType = getTypes(transText)
    
    # Check for bad transcations
    if 'Bad' in transType:
        error = 'Paying in'
    try:
        transAmount = float(transAmount)
    except:
        error += 'Amount is not a number'

    transType = '|'.join(transType)
    newLine = [
        transDate,
        transAmount,
        transType,
        transText,
        line
    ]

    return newLine, error
    
    


