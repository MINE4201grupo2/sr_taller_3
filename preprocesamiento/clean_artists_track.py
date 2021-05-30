import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import math
import sys
import csv

chunksize = 10 ** 6
with pd.read_csv('data/userid-timestamp-artid-artname-traid-traname.tsv', encoding="utf-8", delimiter='\r', chunksize=chunksize, header=None) as reader, open('data/clean.tsv', 'w', encoding="utf-8") as fo:
#with pd.read_csv('data/test.tsv', encoding="utf-8", delimiter='\r', chunksize=chunksize, header=None) as reader,open('data/clean.tsv', 'w') as fo:
    for lines in reader:
      for i in lines.index:
        fo.write(lines[0][i].replace('"', '').replace("'", ""))
        fo.write("\r")

 