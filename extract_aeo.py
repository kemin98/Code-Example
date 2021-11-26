'''
Rubric

(20/20)  Correctly use any methods specified in the question
15/15  Uses spacy
5/5   Uses pypdf

(13/20)  Gets the correct result
0/5   Includes csv files with submission
5/5   Includes comment block outlining logic and weaknesses of code
8/8   Result makes sense/is valid
0/2   Csv files are well-formatted (good column names, readable)
- no CSV generated and the data frames you generate are all broken out and hard to follow

(13/15)  Code runs without errors
10/10  No major errors
3/5   No minor errors
- code returned nothing originally, had to include print statements to see results

(15/15)  Uses methods taught in class
8/8   Uses tokens
2/2   Parses pdf
5/5   Iterates to traverse (children, ancestors, etc)

(10/10)  Use of GitHub to commit assignment on time
1/1   Good commit messages
9/9   Pushed on time

(4.5/5)   Good use of Python Style
1/1   Correct spacing around operators
2/2   Correct Indentation (4 spaces)
0.5/1   No excessive blank lines / sporadic spacing (between logic blocks, at the end of the code, etc)
- sporadic spacing throughout
1/1   Blank lines after function definitions

(5/5)   Good use of comments and variable naming
1/1   Appropriate amount of comments
2/2   Functions are well-named/well defined
1/1   Variables are well-named
1/1   Comments are useful and accurate

(3.5/5)   Writing clear, succinct, code
2/3   Code is easy to understand
0.5/1   Does not include unnecessary print statements
- No need to print data frame, should have returned CSV
1/1   Code is not overly long (< ~500 lines)

(4.5/5)   Properly generalizing code
1.5/2  Does not repeat code
- think about how you could have avoided some repeating code inside your functions
2/2   Creates and uses functions
1/1   Functions do not have overlapping functionality

Total: 88.5
Grader: Shai
'''


# url = 'https://www.eia.gov/outlooks/aeo/pdf/aeo2019.pdf'
# url = 'https://www.eia.gov/outlooks/aeo/pdf/aeo2018.pdf'

#The logic of my code is to count the times down_words/up_words appear together with a specific type of energy sources. Genrally,
#if up_words appear more frequently on average than down_words, then that aspect of that energy is probably going to rise. I 
#accomplish this "counting" task by coding down_words to -1 and up_words to 1, and calculate the summation for each aspect of 
#each specific energy source. One weakness of my code is that it considers less about negation words, but it works fine in these 
#two pdf since most of the texts I parsed contained few negations. Another weakness is when upwords and downwords appear together 
#in a sentence. In this case it would be difficult to see whether there is a up trend or down trend without actually looking at
#that sentence. Also, if there are multiple energy sources appear in the same sentence and there happens to be a combination of
#upwords and downwords to describe them, it would be hard to tell from this code that which words apply to which energy sources.

import PyPDF2 #pip install PyPDF2
import os
import math
import spacy
import pandas as pd

PATH = r'C:\Users\Kemin\Desktop'
energy_type = ['coal', 'nuclear', 'oil', 'wind', 'solar']
down_words = ['lower', 'declining', 'low', 'decline', 'decreasing', 'drops']
up_words = ['high', 'higher', 'increasing', 'rising', 'rises', 'rise',
            'dominant', 'grow', 'greater', 'records', 'increases', 'growth', 'mostly',
            'lowest','strong']


# Extract texts from key takeaway parts in the pdf. Since the each page contains two slides, there is a way
# to locate the exact page number after knowing the slide number, which I located first from the table of contents part.
def get_key_take_away(fname):
    pdf = open(os.path.join(PATH, fname), 'rb')
    pdf = PyPDF2.PdfFileReader(pdf)
    
    page_number_finder = [(pdf.getPage(pnum).extractText().index('slide number'), pnum) for pnum in range(pdf.getNumPages()) 
             if 'slide number' in pdf.getPage(pnum).extractText()]

    start_page = int(pdf.getPage(page_number_finder[0][1]).extractText()[page_number_finder[0][0]+13])

    start_page = math.ceil(start_page/2)

    end_page = int(pdf.getPage(page_number_finder[0][1]).extractText()[page_number_finder[0][0]+14:page_number_finder[0][0]+16])-1

    end_page = math.ceil(end_page/2)

    key_takeaway = [pdf.getPage(pnum).extractText() for pnum in range(start_page, end_page)]

    key_takeaway = '\n'.join(key_takeaway)

    key_takeaway = key_takeaway.replace('\n', ' ')

    key_takeaway = key_takeaway.encode('ascii', 'ignore').decode(encoding="utf-8")
    
    return key_takeaway


#Here I create the dataframe to store the energy outlook value
def create_df():
    
    key_takeaway_dict = [ {'energy type': 'coal',      'price': 0, 'emissions': 0 , 'production': 0, 'export/import': 0},
                          {'energy type': 'nuclear',   'price': 0, 'emissions': 0 , 'production': 0, 'export/import': 0},
                          {'energy type': 'wind',      'price': 0, 'emissions': 0 , 'production': 0, 'export/import': 0},
                          {'energy type': 'solar',     'price': 0, 'emissions': 0 , 'production': 0, 'export/import': 0},
                          {'energy type': 'oil',       'price': 0, 'emissions': 0 , 'production': 0, 'export/import': 0},
                          ]

    key_takeaway_df = pd.DataFrame(key_takeaway_dict)
    return key_takeaway_df


#This is the main Function that runs all the sub-functions and get the final result    
def get_energy_outlook(fname):
    
    key_takeaway_df = create_df()
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(get_key_take_away(fname))

    see_the_emission_change(doc,key_takeaway_df)
    see_the_emission_change(doc,key_takeaway_df)
    see_the_production_change(doc,key_takeaway_df)
    see_the_export_status(doc,key_takeaway_df)
    key_takeaway_df = key_takeaway_df.applymap(decide_increase_or_decrease)
    print(key_takeaway_df)
    return key_takeaway_df
    

# This function aims to get the outlook for price change. I coded +1 as a signal for increase, and -1 for decrease, 0 for 
# not clear or unknown. 
def see_the_price_change(doc,key_takeaway_df):
    for sent in list(doc.sents):
        for token in sent:
            if 'prices' in token.text or 'price' in token.text:
                for child_token in (list(token.children)):
                                if child_token.text in energy_type:
                                    for updown_token in sent:
                                        if updown_token.text in down_words:
                                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == child_token.text), 'price'] -= 1
                                        if updown_token.text in up_words:
                                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == child_token.text), 'price'] += 1
    for sent in list(doc.sents): 
        if 'costs of renewable' in sent.text:
                for updown_token in sent:
                    if updown_token.text in down_words:
                         key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'wind'), 'price'] -= 1
                         key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'solar'), 'price'] -= 1
                    if updown_token.text in up_words:
                         key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'wind'), 'price'] += 1
                         key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'solar'), 'price'] += 1    
        
                
#This function aims to get the outlook for emission change. I coded +1 as a signal for increase, and -1 for decrease, 0 for 
# not clear or unknown. My logic is that emission is directly related with energy/electricity generation(renewable energy don't
#apply) And there is also a substitution effect, where if generation from renewable energy goes down, generation/emission from
#coal and oil will increase.
def see_the_emission_change(doc,key_takeaway_df):
    for sent in list(doc.sents): 
            if ('renewable' and 'generation') in sent.text:
                    for updown_token in sent:
                        if updown_token.text in down_words:
                             key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'coal'), 'emissions'] += 1 
                             key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'oil'), 'emissions'] += 1 
                        if updown_token.text in up_words:
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'coal'), 'emissions'] -= 1
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'oil'), 'emissions'] -= 1
                            

##This function aims to get the outlook for production change. I coded +1 as a signal for increase, and -1 for decrease, 0 for 
# not clear or unknown. If there is a retirement of certain plant, for example, nuclear plant, then nuclear power production will
#decrease. If there is more generation from renewable sources, more renewable energy production should be true.
def see_the_production_change(doc,key_takeaway_df):
    for sent in list(doc.sents):
        for token in sent:
            if 'production' in token.text:
                for child_token in (list(token.children)):
                                if child_token.text in energy_type:
                                    for updown_token in sent:
                                        if updown_token.text in down_words:
                                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == child_token.text), 'production'] -= 1
                                        if updown_token.text in up_words:
                                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == child_token.text), 'production'] += 1

        for token in sent:
            if 'retirements' in token.text:
                for etype_token in sent:
                     if etype_token.text in energy_type:
                                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == etype_token.text), 'production'] -= 1
    for sent in list(doc.sents): 
            if ('renewable' and 'generation') in sent.text:
                    for updown_token in sent:
                        if updown_token.text in up_words:
                             key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'wind'), 'production'] += 1 
                             key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'solar'), 'production'] += 1 
                        if updown_token.text in down_words:
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'wind'), 'production'] -= 1
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'solar'), 'production'] -= 1

                                            
        
##This function aims to get the outlook for export change. I coded +1 as a signal for export, and -1 for import, 0 for 
# not clear or unknown. If there is a retirement of certain plant, for example, coal, then coal production/export will
#decrease. There is also a negation word needs to be taken care of on line 175. Exports don't apply to renewable energy and 
#nuclear energy.
def see_the_export_status(doc,key_takeaway_df):
    for sent in list(doc.sents):
        if ('exports' in sent.text) or ('export' in sent.text) or ('exporter' in sent.text) or ('exporting' in sent.text):
            for etype_token in sent:
                if etype_token.text in energy_type:
                    for updown_token in sent:
                        if updown_token.text in up_words:
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == etype_token.text), 'export/import'] += 1 
                        if updown_token.text in down_words:
                            key_takeaway_df.loc[(key_takeaway_df['energy type'] == etype_token.text), 'export/import'] -= 1
                        
        
            for token in sent:
                if 'retirements' in token.text:
                    for etype_token in sent:
                     if etype_token.text in energy_type:
                         key_takeaway_df.loc[(key_takeaway_df['energy type'] == etype_token.text), 'export/import'] -= 1   
                        
    for sent in list(doc.sents):
        if (('exports' in sent.text) or ('export' in sent.text) or ('exporter' in sent.text)) and ('not' in sent.text):
             for etype_token in sent:
                if etype_token.text in energy_type:
                    key_takeaway_df.loc[(key_takeaway_df['energy type'] == etype_token.text), 'export/import'] = 0
                    
                                            
    key_takeaway_df.loc[(key_takeaway_df['energy type'] == 'nuclear'), 'export/import'] = 0 

#Here I convert the coded numerical value into meaningful strings as I have discussed
def decide_increase_or_decrease(value):
        if isinstance(value, int) and value < 0:
            return 'decrease'
        if isinstance(value, int) and value == 0:
            return 'not clear or unknown'
        elif isinstance(value, int) and value > 0:
            return 'increase'
        else:
            return value

#Here I run the entire function and get the result
outlook_2019 = get_energy_outlook('aeo2019.pdf')

outlook_2018 = get_energy_outlook('aeo2018.pdf')


