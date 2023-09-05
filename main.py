# importing the module
from datetime import date, timedelta
import argparse
import csv
import yaml

config = yaml.safe_load(open("config.yml"))

def isValid(country):
    return country in config['allowed']

def displaySummary(currentCountry, minus180):
    if not isValid(currentCountry):
        print('please provide valid country')
        return
    today = date.today()
    currentDate = minus180
    d = {}
    isStartDateBeforeSpecified = False
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                newDate = date.fromisoformat(row[0])
                leaving = row[1]
                interval = 0
                if currentDate < newDate:
                    interval = (newDate - currentDate).days + 1
                    currentDate = newDate
                if minus180 < newDate :
                    isStartDateBeforeSpecified = True
                d[leaving] = d.get(leaving, 0) + interval
                line_count += 1
    d[currentCountry] = d.get(currentCountry, 0) + (today - currentDate).days + 1
    print(d)

def addInfo(date, from_country):
    if not isValid(from_country):
        print('Please provide valid data')
        print('Valid countries: ' + ', '.join(config['allowed']))
        return
    
    with open('data.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, from_country])
    print('info added')

def isDataValid(currentCountry):
    if not isValid(currentCountry):
        print('please provide valid country')
        return False

    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        csvDate = None
        csvCountry = None
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif line_count == 1:
                csvDate = date.fromisoformat(row[0])
                csvCountry = row[1]
                if not isValid(csvCountry):
                    print(f'Country {csvCountry} from row {line_count} is not valid')
                    return False
                line_count += 1
            else:
                newDate = date.fromisoformat(row[0])
                newCountry = row[1]
                if not isValid(newCountry):
                    print(f'Country {newCountry} from row {line_count} is not valid')
                    return False
                if newDate < csvDate:
                    print(f'Date on line {line_count} is before the previous line, please fix')
                    return False
                if newCountry == csvCountry:
                    print(f'Country on line {line_count} is the same as on the previous line, please fix')
                    return False
                csvDate = newDate
                csvCountry = newCountry
                line_count += 1
    if csvCountry == currentCountry:
        print('Current country should be different from the last from csv file')
        return False
    
    return True

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument('action', help = 'Specify action, can be add, summery')
parser.add_argument('-d', '--Date', help = 'Input date')
parser.add_argument('-f', '--From', help = 'Add from')
parser.add_argument('-c', '--Current', help = 'Current country')

# Read arguments from command line
args = parser.parse_args()
option = args.action
if option == 'add':
        addInfo(date.fromisoformat(args.Date), args.From)
elif option == 'summary':
        if isDataValid(args.Current):
            today = date.today()
            minus180 = today - timedelta(days=config['period-in-days'])
            if args.Date:
                minus180 = date.fromisoformat(args.Date)
            displaySummary(args.Current, minus180)
else:
    print('non specified')
 