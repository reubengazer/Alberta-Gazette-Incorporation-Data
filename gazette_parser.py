##############################################
## By: Reuben S. Gazer (March 2019, AltaML) ##
##############################################

# Parser for the Alberta Gazette text files downloaded from gazette.py script       #
# Makes a saving directory called gazette_CSVs/ and inner directories for each year #
# between 2006 and 2008 (inclusive) for saving individual relevant files.           #

#############################################

import pandas as pd
import os
import sys
import pickle
from corporation_classes import Incorporation, NameChange


def main(outfolder = './gazette_data/', outtype = sys.argv[1]):
    """
    Creates files that house all incorporations and namechanges from 2006-2018 in Alberta Gazette .txt data files. 
    Skips over a few dates that have small errors like indents, extra spaces, or something else.
    In reality, these can be identified and changed by hand, but for the sake of "smooth scripting"
    straight after running the download script, these are skipped over.
    
    Outtype can be 'csv' or 'pickles'.
    
    If outtype == 'csv':
    - Makes individual csvs for each time period and saves them to relevant date folder
    - Stacks all tables in the end into two master csv tables: incorporations_2006-2018.csv, namechanges_2006-2018.csv
    
    If outtype == 'pickles':
    - Exports lists of pickled objects:  incorporations_2006-2018.pickle, namechanges_2006-2018.pickle
    - Here, the classes in the pickled lists are defined in corporation_classes.py datafile that is imported.
    
    COMMAND LINE SCRIPT ARGUMENTS:
    
    - 'pickles' -> outputs a pickled list of incorporations and namechanges
    - 'csv' -> outputs individual CSVs for each timeperiod as well as master CSVs
    
    """
    
    # Check if gazette data exists (whether gazette.py has been run) #
    data_exists_check()
    # Check whether save directories exists, and if not, create them #
    save_directory_check()
    # Files that have extra spaces, indents, etc. and won't run smoothly through.
    bad_dates = ['2006/18_Sep30','2006/17_Sep15','2016/18_Sept30','2017/11_Jun15','2018/10_May31']
    # Instantiate empty lists for keeping data before saving out.
    incorporations, namechanges = [], [] 
    # Format default output as CSVs if no sys.argv[1] provided
    if not sys.argv[1]:
        outtype = 'csv'
    
    # Begin parsing files by year #
    for year in range(2006,2018+1):
        files = os.listdir('cache/gazette/'+str(year))
        for filename in files:
            if filename.endswith('.txt'):
                date_string = str(year) + '/' + filename[:-4]
                if date_string not in bad_dates:
                    # The following returns pandas DataFrames if outtype is 'csv', list of pickles if outtype is 'pickles' #
                    inc, nmch = make_incorporations_and_namechange(date_string,outfolder = outfolder,outtype = outtype)
                    if outtype == 'csv':
                        incorporations.append(inc)
                        namechanges.append(nmch)
                    elif outtype == 'pickles':
                        incorporations += inc
                        namechanges += nmch
    
    # Write out files #
    
    if outtype == 'csv': 
        make_master_tables(incorporations,namechanges)
                    
    elif outtype =='pickles': 
        # Incorporations #
        pickle_out = open(outfolder + "incorporations_2006-2018.pickle","wb")
        pickle.dump(incorporations, pickle_out)
        pickle_out.close()
        # Namechanges #
        pickle_out = open(outfolder + "namechanges_2006-2018.pickle","wb")
        pickle.dump(namechanges, pickle_out)
        pickle_out.close()
        
        
def data_exists_check():
    """Check whether the gazette.py script has been run, and therefore that the 
    cache/gazette/ directory exists with Alberta Gazette data files inside."""
    
    if not os.path.isdir('cache/gazette'):
        sys.exit("We don't have the Alberta Gazette data. Please run 'gazette.py' to download relevant files.")
    
               
def save_directory_check():
    """Check whether saving directories exists, and if it doesn't, make it."""
    
    savepath = './gazette_data/'
    
    if os.path.isdir(savepath):
        print(f"Save directory {savepath} exists.")
    else:
        print(f"Creating save directory in local folder, {savepath} for saving of all CSV files.")
        print(f"Creating a directory for each year between (and including) 2006-2018 inside {savepath}")
        os.mkdir(savepath)
        for year in range(2006,2019):
            os.mkdir(savepath+str(year))
        
    
def make_incorporations_and_namechange(date_string: str, outfolder = './gazette_CSVs/',outtype='csv'):
    """Make all of the incorporations and namechanges for a given date and save into a csv file."""
    # Incorporations #
    incorporations = get_incorporations(date_string)
    incorporations = [create_incorporation_object(inc) for inc in incorporations]
    
    # Name Changes #
    namechanges = get_namechanges(date_string)
    namechanges = [create_namechange_object(namechange) for namechange in namechanges]
    
    if outtype == 'csv':
        incorporations_df = pd.DataFrame([inc.to_dict() for inc in incorporations]) 
        incorporations_df.to_csv(outfolder + date_string + '_incorporations.csv',index=False)
        namechanges_df = pd.DataFrame([namechange.to_dict() for namechange in namechanges]) 
        namechanges_df.to_csv(outfolder + date_string + '_namechanges.csv',index=False)
        return(incorporations_df,namechanges_df)
    
    if outtype == 'pickles':
        return(incorporations,namechanges)
    
    
def make_master_tables(incorporations,namechanges,outfolder = './gazette_CSVs/'):    
    """Stack all of the dataframes into master tables and save them to the outfolder as csv files."""
    master_incorporations = pd.concat(incorporations,axis=0)
    master_incorporations.to_csv(outfolder + 'incorporations_masterlist_2006-2018.csv')
    master_namechanges.to_csv(outfolder + 'namechanges_masterlist-2006-2018.csv')
    print(f"Saved master tables for INCORPORATIONS and NAMECHANGES to {outfolder}.")
                    
        
def get_incorporations(date_string: str) -> list:
    """Select the chunk of text that has the new incorporation information in it.
    Save the file temporarily as the same date file with '_incorporations.txt' appended to filename."""
    
    f = open('cache/gazette/' + date_string + '.txt','r')
    lines = f.readlines()
    incorporation_lines = []
    
    parsing = False
    for line in lines:
        if line.startswith("Corporate Registrations"):
            parsing = True
        elif line.startswith("Corporate Name Changes"):
            parsing = False
        if parsing: # in the incorporation section
            incorporation_lines.append(line.rstrip())
                
    # Remove the first 4 entries of the list which are header lines.
    del incorporation_lines[0:4]
    # Remove the footer lines that look blank, but really contain either '\n' or '.'
    incorporation_lines = [x for x in incorporation_lines if len(x) > 5]
            
    return(incorporation_lines)

    
def get_namechanges(date_string: str) -> list:
    """Select the chunk of text that has the name change information in it.
    Save the file temporarily as the same date file with '_name_changes.txt' appended to filename."""
    
    f = open('cache/gazette/' + date_string + '.txt','r')
    lines = f.readlines()
    namechange_lines = []
    
    parsing = False
    for line in lines:
        if line.startswith("Corporate Name Changes"):
            parsing = True
        elif line.startswith("Corporations Liable for Dissolution"):
            parsing = False
        if parsing: 
            namechange_lines.append(line.rstrip())
                
    # Remove the first 4 entries of the list which are header lines.
    del namechange_lines[0:4]
    # Remove footer lines that look blank but really contain either '\n' or '.'
    namechange_lines = [x for x in namechange_lines if len(x) > 5]
    
    return(namechange_lines)


def create_incorporation_object(inc: str):
    """Parse a new incorporation line into an Incorporation class and return it."""
    company_type, ID = get_company_type_and_id(inc)
    date = get_date(inc)
    address = get_address(inc)
    number = get_number(inc)
    incorp_object = Incorporation(ID,company_type,date,address,number)
    return(incorp_object)


def create_namechange_object(inc: str):
    """Parse a name change into a NameChange class and return it."""
    company_type, ID = get_company_type_and_id(inc)
    date = get_date(inc)
    new_name = get_new_name(inc)
    effective_date = get_date(inc)
    number = get_number(inc)
    namechange_object = NameChange(ID,company_type,date,new_name,effective_date,number)
    return(namechange_object)


def get_company_type_and_id(inc: str) -> str:
    """Returns the type of company, given by the long list in the list "company_types". """
    
    company_types = ['Named Alberta Corporation','Numbered Alberta Corporation','Other Prov/Territory Corps',
                    'Certified General Accounting Professional Corporation',
                     'Certified Management Accounting Professional Corporation','Federal Corporation','Alberta Society',
                    'Chartered Accounting Professional Corporation','Medical Professional Corporation',
                    'Foreign Corporation','Legal Professional Corporation','Chiropractic Professional Corporation',
                    'Alberta Cooperative','Religious Society','Liability Partnership','Non-Profit Private Company',
                    'Dental Professional Corporation','Extra-Provincial Cooperative','Non-Profit Public Company',
                     'Recreation Private Company','Optometry Professional Corporation',
                     'Private Act Non-Profit Corporation','Extra-Provincial Loan Corporation',
                     'Recreation Public Company','Rural Utilities','Private Corporation','Trust Corporation',
                    'Foreign Cooperative','Private Act Corporation','Credit Union Amalgamated',
                    'Alberta Lodge','Public Corporation','Chartered Professional Accountant Professional Corporation',
                    'Credit Union']
    
    for company_type in company_types:
        if company_type in inc:
            return(company_type,inc.split(company_type)[0].strip())
    

def get_date(inc: str) -> str:
    """Return the date the company incorporated/registered."""
    if 'Registered Address:' in inc:
        date_list = inc.split('Registered Address:')[0].split()[-3:]
        date = date_list[0] + ' ' + date_list[1] + ' ' + date_list[2]
    elif 'New Name:' in inc:
        date_list = inc.split('New Name:')[0].split()[-3:]
        date = date_list[0] + ' ' + date_list[1] + ' ' + date_list[2]
        date = date[:-1]
    return(date)


def get_address(inc: str) -> str:
    """Return the registered address of the incorporation."""
    address = inc.split('Registered Address:')[1].split('No:')[0].strip()[:-1]
    return(address)


def get_number(inc: str) -> str:
    """Return the number (No. #######) at the end of the line."""
    number = inc.split()[len(inc.split())-1].strip()[:-1]
    return(number)


def get_new_name(inc: str) -> str:
    """Return the new name of a name-changed company."""
    new_name = inc.split('New Name:')[1].split('Effective Date:')[0].strip() 
    return(new_name)
  
    
if __name__ == '__main__':
    main()
    
    