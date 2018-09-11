"""
Specify parameters for transaction data.
"""

# Specify input/output transaction file directories
inFilePath = 'C:\\Users\\Eimantas\\Desktop\\transactions.txt'
outFilePath = 'C:\\Users\\Eimantas\\Desktop\\transactions.csv'

# Set debug mode for extra information
debug = False

def inputPath():
    return inFilePath

def outputPath():   
    return outFilePath

def debugMode():
    return debug
