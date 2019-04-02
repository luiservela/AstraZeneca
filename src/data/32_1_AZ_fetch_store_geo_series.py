# This script  fetches all gse series with Organism=Homo Sapiens of the GEO Database and creates a xml file out of it
from Bio import Entrez
import sys
import os
import time
Entrez.email = "A.N.Other@example.com" # Always tell NCBI who you are
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2
# retmax = maximum number of retrieved series


## Set paths
# cdir = dir of this script
cdir = os.path.dirname(os.path.realpath(__file__))
# basedir = root dir of the repository
basedir = os.path.dirname(os.path.dirname(cdir))

dir_data_out = basedir+"/data/raw/geo_data/"
if not os.path.exists(dir_data_out):
    os.makedirs(dir_data_out)

filenamebase="all_gse_series_homo_sapiens"

# use_small_number_of_series = True when only a small number of series shall be extracted. The number of series is specified by small_number_of_series
use_small_number_of_series = False
small_number_of_series = 10

# if use_id=True then the ids are used to fetch the data but then only one by one they can be extracted.
# if use_id=False then the fetching can be performed via larger batchsizes but makes neccesary to perform the initial esearch with usehistory="y" and the fetch with the WebEnv and query_key arguments.
use_id = False
if(use_id):
    batch_size = 1
    use_hist_val = 'n'
else:
    batch_size = 5000
    use_hist_val = 'y'

search_term = input("Input search terms that shall be contained in the desired geo DataSets. Please look at\nhttps://www.ncbi.nlm.nih.gov/geo/info/qqtutorial.html\nfor all possibilities. To construct a complex query, specify the search terms, their fields, and the Boolean operations to perform on the terms using the following syntax:\nterm [field] OPERATOR term [field]\nwhere term is the search terms, field is the search field, and OPERATOR is the Boolean operator ('AND', 'OR', 'NOT') which must be capitalized. When you press enter without giving a string expression for the query the following standard query is performed,\nGSE[ETYP] AND Homo[Organism]\nwhich retrieves all geo series with studies performed for/on humans."

if(len(search_term) == 0):
    search_term = "GSE[ETYP] AND Homo[Organism]"
    handle = Entrez.esearch(db="gds", term=search_term, retmax=small_number_of_series, usehistory=use_hist_val)
else:
    handle = Entrez.esearch(db="gds", term=search_term, retmax=small_number_of_series, usehistory=use_hist_val)

record = Entrez.read(handle)
total_n_series = int(record['Count'])
if total_n_series == 0:
    print("No geo series with the given search terms were found. Please repeat your query with different search terms.\n")
    sys.exit()
else:
    print("A total of "+str(total_n_series)+" geo DataSets that are compatible with the search query have beend found.")

if(not(use_small_number_of_series and not(use_id))):
    handle.close()

if(not use_small_number_of_series):
    handle = Entrez.esearch(db="gds", term=search_term, retmax=total_n_series, usehistory=use_hist_val)
    record = Entrez.read(handle)
    if(use_id):
        handle.close()

idlist = record['IdList']
count = int(len(idlist))
print('Total number of found entries: ' + str(count))

for start in range(0, count, batch_size):
    print(start)
    if batch_size == 1:
        end = start
        if(use_id):
            ival = start
    else:
        end = min(count, start + batch_size)
        if(use_id):
            ival = slice(start, end, 1)
    if(use_id):
        print("Going to download record with id {}".format(idlist[ival]))
    else:
        print("Going to download record %i to %i" % (start+1, end))
    attempt = 1
    not_fetched = True
    while ((attempt <= 3) and not_fetched):
        try:
            if(use_id):
                fetch_handle = Entrez.esummary(db="gds", id=idlist[ival], retmode="xml")
            else:
                fetch_handle = Entrez.esummary(db="gds", retstart=start, retmax=min(10000, batch_size), retmode="xml", webenv=record['WebEnv'], query_key=record['QueryKey'])
            data = fetch_handle.read()
            fetch_handle.close()

            out_handle = open(dir_data_out+filenamebase+"_part"+str(int(start/batch_size))+".xml", "a")
            out_handle.write(data)
            out_handle.close()

            not_fetched = False
        except HTTPError as err:
            not_fetched = True
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                attempt += 1
                time.sleep(3)
            else:
                raise
