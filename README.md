# Obtaining Alberta Gazette Incorporation Data

To obtain the raw .txt files from Alberta Gazette:
```
python3 gazette.py
```
We can obtain all new incorporations, and namechanges (each time a company officially changes its name) by using the gazette_parser.py file.

To parse the raw .txt files into csv files or pickled lists:
```
python3 gazette_parser.py arg
```
where arg can be {pickles} or {csv} to output the files as a pickled list of incorporation and namechange objects,
or individual csvs for each timeperiod and master csvs with all time periods stacked.
