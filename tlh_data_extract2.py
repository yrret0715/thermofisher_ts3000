import os
import sys
import csv

from bs4 import BeautifulSoup


def extract(fp):
    
    starting_line = "<tr><td><Font  Size=4>Raw sample data</td></tr>"
    header_html = "<tr><td><Font  Size=1>Time</td><td><Font  Size=1>Data</td>"
    to_replace = "<tr>"

    start_extracting = False
    lines = fp.readlines()

    cleaned_html_str = "<HTML><Body><Table>"

    for l in lines:
        stripped_l = l.rstrip('\n')
        if stripped_l.startswith(starting_line):
            start_extracting = True
        if start_extracting == True:
            if (stripped_l.find(header_html) != -1):
                stripped_l = stripped_l.replace(header_html, to_replace)
            if (stripped_l.startswith(starting_line) != True):
                cleaned_html_str += stripped_l 

    print("Raw data cleared.")
    return cleaned_html_str


def convert_to_csv(cleaned_html_str, html_fn):
    soup = BeautifulSoup(cleaned_html_str, 'html.parser')
    table = soup.select("table")[0]
    csv_fn = html_fn + ".csv"

    with open(csv_fn, "w") as csv_fp:
        wr = csv.writer(csv_fp)
        wr.writerows([[td.text for td in row.find_all("td")] for row in table.select("tr")])
        print("Cleared data written to: %s" % (csv_fn))
    return csv_fn

def pair_and_sort(cleaned_csv_name):
    with open(cleaned_csv_name, "r") as csv_fp:
        pairs = []
        rd = csv.reader(csv_fp, delimiter=',')
        for row in rd:              
            ts = [col for col in row if col.find('.') == -1]
            ds = [col for col in row if col.find('.') != -1]
            pairs.extend(zip(ts, ds))
        #print(pairs)
        pairs.sort(key=lambda x: int(x[0]))
        return pairs

def write_final_csv(pairs, final_csv_fn):
    with open(final_csv_fn, 'w') as csv_fp:
        wr = csv.writer(csv_fp)
        wr.writerow(['time', final_csv_fn[17:-8]])
        for row in pairs:
            wr.writerow(row)

        print("Final data written to: %s" % (final_csv_fn))
    

def main():
    fn = sys.argv[1]
    fp = open(fn, 'r')
    cleaned_html_str = extract(fp)
    cleaned_csv_name = convert_to_csv(cleaned_html_str, fp.name)
    sorted_time_data_pairs = pair_and_sort(cleaned_csv_name)
    final_csv_fn = "%s_%s" % ("final", cleaned_csv_name)
    write_final_csv(sorted_time_data_pairs, final_csv_fn)
    

if __name__ == '__main__':
    main()
