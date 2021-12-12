import PyPDF2 #pip install PyPDF2
import os
import pandas as pd
#New Package
import wordninja
from pdfminer.high_level import extract_text


PATH = r'C:\Users\Kemin\Desktop\Report'

fname_2008 = '2008 report.pdf'
start_page_2008 = 12
end_page_2008 = 13

fname_2009 = '2009 report.pdf'
start_page_2009 = 11
end_page_2009 = 12

fname_2013 = '2013 report.pdf'
start_page_2013 = 13
end_page_2013 = 14

fname_2012 = '2012 report.pdf'
start_data_2012 = '96964'
mid_data_2012 = '94241'
end_data_2012 = '57993'
fix_data_2012 = '14939'
num_string_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
pages_2012 = [13, 14] 


fname_2011 = '2011 report.pdf'
start_data_2011 = '96306'
mid_data_2011 = '94190'
end_data_2011 = '56283'
fix_data_2011 = '14435'
pages_2011 = [13, 14] 


fname_2010 = '2010 report.pdf'
start_data_2010 = '95489'
mid_data_2010 = '92268'
end_data_2010 = '56053'
fix_data_2010 = '13298'
num_string_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
pages_2010 = [13, 14] 

variables_list = ['White', 'WhitenotHispanic', 'Black', 'Asian', 'Hispanic(anyrace)',
                  'Under65years','15to24years', '25to34years', '35to44years',
                  '45to54years', '55to64years', '65yearsandolder', 'Menwithearnings',
                  'Womenwithearnings']



num_string_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def pdf_reader_080913(fname, start_page, end_page):
    
    pdf = open(os.path.join(PATH, fname), 'rb')

    pdf = PyPDF2.PdfFileReader(pdf)
    
    text = []

    for pnum in range(start_page, end_page):
        page = pdf.getPage(pnum)
        text.append(page.extractText())
        
    text = ''.join(text)

    text = ''.join(c for c in text if c not in ',. ')
        
    return text


def table_parser_080913(fname, start_page, end_page):
    text = pdf_reader_080913(fname,start_page,end_page)
    data_list = []
    for variable in variables_list:
        index = text.index(variable)
        if variable[-1] not in ['r', 's', 'n']:
            while text[index] not in num_string_list:
                index = index + 1
            data_list.append(text[index:index+5])
               
    
        elif variable[-1] =='s' and variable not in ['15to24years', 'Womenwithearnings']:
            while text[index] != 's':
                index = index +1
            data_list.append(text[index+1:index+7])
        
        elif variable[-1] =='r':
            index = index+15
            while text[index] not in num_string_list:
                index = index + 1
            data_list.append(text[index:index+5])
    
        elif variable[-1] =='n':
            while text[index] != 'n':
                index = index +1
            data_list.append(text[index+1:index+6])
    
        elif variable == '15to24years':
            while text[index] != 's':
                index = index +1
            data_list.append(text[index+1:index+6])
        
        else:
            while text[index] != 's':
                index = index +1
            while text[index] not in num_string_list:
                index = index + 1
            data_list.append(text[index:index+5])
            
            data_list = space_remover(data_list)
            
            data_list = [int(s) for s in data_list]
            
            return data_list 

def space_remover(data_list):
    
    data_list = [s.strip('\n') for s in data_list]
    
    return data_list

def table_parser_13_fix(data_list_2013):
    
    data_list_2013 = [int(str(s).rstrip(str(s)[-1])) if data_list_2013.index(s) in [3,6,7,8,9,10] else s for s in data_list_2013]
    
    return data_list_2013


def pdf_reader_101112(fname, pages):
    
    text = extract_text(os.path.join(PATH, fname), "", pages)
    
    text = ''.join(text)
    
    text = ''.join(c for c in text if c not in ',. ')
    
    return text




def table_parser_101112(fname, pages, start_data, mid_data, end_data, fix_data):
    
    text = pdf_reader_101112(fname, pages)
    
    data_list = []

    index = text.index(start_data)
    
    for i in range(0,5):
        if i != 4:
            data = text[index:index+5]
            data_list.append(data)
            index = index+6
        else:
            data = text[index:index+5]
            data_list.append(data)
            index = index+5
    
    index = text.index(mid_data)
        
    for i in range(0,7):
        if i != 1:
            data = text[index:index+5]
            data_list.append(data)
            index = index+6
        else:
            data = text[index:index+5]
            data_list.append(data)
            index = index+5
    
    index = text.index(end_data)
    
    for i in range(0,2):
        data = text[index:index+5]
        data_list.append(data)
        index = index+6
    
    data_list[4] = fix_data
    data_list = space_remover(data_list)
    data_list = [int(s) for s in data_list]
    
    return data_list

data_list_2008 = table_parser_080913(fname_2008, start_page_2008, end_page_2008)  

data_list_2009 = table_parser_080913(fname_2009, start_page_2009, end_page_2009)  
        
data_list_2013 = table_parser_080913(fname_2013, start_page_2013, end_page_2013)  

data_list_2013 = table_parser_13_fix(data_list_2013)
        
data_list_2012 = table_parser_101112(fname_2012, pages_2012, start_data_2012, mid_data_2012, end_data_2012, fix_data_2012)        
        
data_list_2011 = table_parser_101112(fname_2011, pages_2011, start_data_2011, mid_data_2011, end_data_2011, fix_data_2011)          
    
data_list_2010 = table_parser_101112(fname_2010, pages_2010, start_data_2010, mid_data_2010, end_data_2010, fix_data_2010)

variables_list_df = [' '.join(wordninja.split(s)) for s in variables_list]

col_lists = [variables_list_df, data_list_2008, data_list_2009, data_list_2010, data_list_2011, data_list_2012, data_list_2013]

df_report = pd.concat([pd.Series(x) for x in col_lists], axis=1)

df_report.columns = ['categories', '2007', '2008', '2009', '2010', '2011', '2012']
