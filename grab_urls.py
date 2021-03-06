import argparse
from datetime import date, timedelta
from sh import wget, links2
from os import mkdir
import zipfile
import csv

parser = argparse.ArgumentParser(
    description='grab urls from gdeltproject.com by date')
parser.add_argument('--start', help='start date, YYYY-MM-DD', required=True)
parser.add_argument('--end', help='end date, YYYY-MM-DD', required=True)
parser.add_argument('--words', help='words to filter by', nargs="+")
args = parser.parse_args()



#wget http://data.gdeltproject.org/events/

syear, smonth, sday = args.start.split('-')
eyear, emonth, eday = args.end.split('-')

d1 = date(int(syear), int(smonth), int(sday))  # start date
d2 = date(int(eyear), int(emonth), int(eday))  # end date

delta = d2 - d1         # timedelta


mkdir('data')
mkdir('data/items')
    
for i in range(delta.days + 1):
    date = str(d1 + timedelta(days=i)).replace('-','')
    wget("-P", "data",
         "http://data.gdeltproject.org/events/%s.export.CSV.zip" % date)

    zf = zipfile.ZipFile("data/%s.export.CSV.zip" % date, "r")
    zf.extractall('data')

    # grab the urls
    urls = []
    with open("data/%s.export.CSV" % date, 'r') as data:
        reader = csv.reader(data, delimiter='\t')
        for row in reader:
            url = row[57]
            if args.words:
                present = False
                for w in args.words:
                    if w in url.lower():
                        present = True
                if present:
                    urls.append(url)
            else:
                urls.append(url)

    
    # download html dumps of them
    n = 0
    for url in urls:
        try:
            with open('data/items/%s_%s_item.txt' % (date, n), 'w') as f:
                f.write('\n\n\n\n' + url + '--------------------------\n\n\n\n')
                f.write(str(links2('-dump', url)))
        except:
            pass
        n += 1
