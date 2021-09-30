import csv
import traceback

'''
    Takes a DOI and checks against all other seen DOIs for duplicates.
'''
class doichecker:

    doi_dict = {}

    def __init__(self):
        self.doi_dict = {}
        try:
            file = open('doilist.csv', 'x')
            file.close()
        except:
            print('doi csv list file already exists')

    # If running from a different machine without access to the master key of seen DOIs, supplement with list of database contents
    def create_inheritance(self, doi_dict):
        for doi in doi_dict.keys():
            # make sure doi not already known to prevent database bloat
            if not self.duplicate(doi_dict[doi]):
                self.appenddoi(doi, target=1)

    # return true if a duplicate doi is passed in
    # add to records if no duplicate is found
    def duplicate(self, doi):
        duplicate = False

        # check fast access list of DOIs
        # check inherited file of all previously seen DOIs
        if doi in self.doi_dict:
            print('match found in fast access list')
            duplicate = True
        else:
            self.appenddoi(doi, target=0)

        if self.duplicate_in_file(doi):
            print('match found in file')
            duplicate = True
        else:
            self.appenddoi(doi, target=1)

        return duplicate

    # check the hereditary file in working directory for duplicate doi
    def duplicate_in_file(self, doi):
        with open('doilist.csv', 'r') as file:
            r = csv.reader(file)

            try:
                # iterate over DOIs in file and check against questionable DOI
                for row in r:
                    if row[0] == doi:
                        print('\tmatches', doi, '==', row[0])
                        return True
                    else:
                        print('\t', row[0], ' doesn\'t match', doi)
            except:
                print('Failed to read rows')
                traceback.print_exc()

        file.close()
        return False

    # add doi to file/fast access list
    def appenddoi(self, doi, target=0):
        # append to fast access list
        if target == 0:
            self.doi_dict[doi] = True

        else:
            # append to file list
            print('appending to csv list file')
            with open('doilist.csv', 'a') as file:
                file.write(doi + ',\n')
            file.close()
