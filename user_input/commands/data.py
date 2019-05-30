import data.unclassified
import data.raw

def process(commands=None):
    """ Run commands for 'data' subparser """
    if commands.migrate:
        migrate()

    if commands.classify:
        classify()

def classify():
    print("Classifying data...")
    import data.unclassified
    data.unclassified.process()

def migrate(txt="Importing data from raw.xlsx..."):
    print(txt)
    import data.raw
    data.raw.migrate()
