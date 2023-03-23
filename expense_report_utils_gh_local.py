from fpdf import FPDF
import os
from calendar import monthrange
import pandas as pd
import numpy as np
import datetime
import pytz
import copy

import re
import time
import os
import copy




class PDF(FPDF):
    LEFT_MARGIN  = 2.54
    TOP_MARGIN = 2.45
    SINGLE_LINE_SPACE = 0.5
    MIDDLE = 11.1
    DATE_ALIGN = 1.22 + LEFT_MARGIN
    FIRST_LINE_TABLE = 8.9 + SINGLE_LINE_SPACE
    TITLE_FONT_SIZE = 11
    UPPER_BLOCK_FONT_SIZE = 11
    TABLE_FONT_SIZE  = 11
    TABLE_LINE_SPACE = 16/31
    ENERGY_ALIGN = 5.0 + DATE_ALIGN
    COST_ALIGN = 5.2 + ENERGY_ALIGN
    COMPANY_ALIGN_X = 10.5
    COMPANY_ALIGN_Y = 26.5
    
    def set_color_black(self):
        self.set_text_color(0,0,0)      
       
    def get_fonts(self):
        self.add_font('SourceSansPro-BoldItalic','','SourceSansPro-BoldItalic.ttf',uni=True)
        self.add_font('SourceSansPro-Regular','', 'SourceSansPro-Regular.ttf',uni=True)
        self.add_font('SourceSansPro-Italic','','SourceSansPro-Italic.ttf',uni=True)
        
    def titles(self):
        self.set_xy(0.0,0.0)
        self.set_font('SourceSansPro-Regular','', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=25.0, h=10.0, align='L', txt="L", border=0) 
        
    def write_title(self):
        self.set_xy(self.LEFT_MARGIN,self.TOP_MARGIN +0.5)
        self.set_font('SourceSansPro-BoldItalic','',self.TITLE_FONT_SIZE )
        self.set_color_black()
        self.cell(w=1,h=1, align='L', txt='Monthly Energy Expense Report', border =0)
        
    def put_logo(self):
        self.set_xy(14.5,1.2)
        self.image('fps_logo.png',link='fps_logo.png', type='png',w=4.05, h=1.91*1.05) 
        
    def write_client_name(self,client_name,line=3):
        self.set_xy(self.LEFT_MARGIN,self.TOP_MARGIN + self.SINGLE_LINE_SPACE*line)
        self.set_font('SourceSansPro-Regular','' , self.UPPER_BLOCK_FONT_SIZE)
        self.set_color_black()
        self.cell(w=1, h= 1, align='L', txt='Client: '+client_name, border=0)
        
    def write_report_number(self,report_number,line=4):
        self.set_xy(self.LEFT_MARGIN,self.TOP_MARGIN + self.SINGLE_LINE_SPACE*line)
        self.set_font('SourceSansPro-Regular','', self.UPPER_BLOCK_FONT_SIZE)
        self.set_color_black()
        self.cell(w=1, h= 1, align='L', txt='Report Number: '+report_number, border=0)
        
    def write_period_start(self, period_start, line=5):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN+ line*self.SINGLE_LINE_SPACE)
        self.set_color_black()
        self.cell(w=1, h=1, align='L',txt='Period start: '+period_start, border=0)
        
    def write_period_end(self,period_end, line=6):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN+ line*self.SINGLE_LINE_SPACE)
        self.set_color_black()
        self.cell(w=1,h=1,align='L', txt= 'Period end: '+period_end,border=0)
        
    def write_elec_provider(self,electricity_provider,line=8):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN + line*self.SINGLE_LINE_SPACE)
        self.set_color_black()
        self.cell(w=1,h=1, align='L', txt= 'Electricity provider: '+electricity_provider,border=0)
        
    def write_tariff_name(self,tariff_name, line=9):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN + line*self.SINGLE_LINE_SPACE)
        self.set_color_black()
        self.cell(w=1,h=1, align='L',txt= 'Tariff name: '+ tariff_name,border=0 )
        
    def write_tariff_gbpkwh(self,tariff_gbp_kwh,line=10):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN + line*self.SINGLE_LINE_SPACE)
        self.set_color_black()
        self.cell(w=1,h=1, align='L', txt= 'Tariff (£/kWh): '+str(tariff_gbp_kwh),border=0)
        
    def write_vat_rate(self,vat_rate, line = 11):
        self.set_xy(self.LEFT_MARGIN, self.TOP_MARGIN + line*self.SINGLE_LINE_SPACE)
        self.cell(w=1,h=1, align='L',txt= 'VAT Rate: '+str(vat_rate)+'%',border=0)
        
    def write_date(self,date,line=3):
        self.set_xy(self.MIDDLE, self.TOP_MARGIN+ self.SINGLE_LINE_SPACE*line)
        self.set_color_black()
        self.cell(w=1,h=1,align='L',txt='Date: '+date,border=0)
        
    def write_charger_reference(self,charger_reference,line=5):
        self.set_xy(self.MIDDLE, self.TOP_MARGIN + self.SINGLE_LINE_SPACE*line)
        self.set_color_black()
        self.cell(w=1,h=1,align='L', txt='Charger reference: '+charger_reference,border=0)
        
    def write_charger_name(self,charger_name,line=6):
        self.set_xy(self.MIDDLE, self.TOP_MARGIN + self.SINGLE_LINE_SPACE*line)
        self.cell(w=1,h=1, align='L', txt= 'Charger name: '+ charger_name,border=0)
        
    def write_charger_address(self,charger_address,line=7):
        self.set_xy(self.MIDDLE, self.TOP_MARGIN + self.SINGLE_LINE_SPACE*line)
        if len(charger_address) > 21:
            first_bit = charger_address.split()[0:2]
            second_bit = charger_address.split()[2:]
            
            first_bit = ' '.join(first_bit)
            second_bit = ' '.join(second_bit)
            self.cell(w=1,h=1, align='L', txt= 'Charger address: '+ first_bit ,border=0)
            self.set_xy(self.MIDDLE, self.TOP_MARGIN + self.SINGLE_LINE_SPACE*(line+1))
            self.cell(w=1,h=1,align='L', txt = second_bit,border=0)
        else:
            self.cell(w=1,h=1,align='L',txt='Charger address: '+charger_address,border=0)
        
    def put_table_header(self):
        self.set_xy(2.54,8.5+self.SINGLE_LINE_SPACE)
        self.image('table_template.png',link='table_template.png', type='png',w = 14.53,h=0.62)
        
    def put_table_lines(self):
        self.set_xy(0,0)
        self.set_line_width(0.005)            
        self.rect(2.55,9.12+self.SINGLE_LINE_SPACE,w=14.524,h=16)
        self.rect(7.1,9.12+self.SINGLE_LINE_SPACE,w=4.8, h=16)
        self.line(2.55,16+9.12+self.SINGLE_LINE_SPACE,2.54+14.524,16+9.12+self.SINGLE_LINE_SPACE) 
        #bottom three boxes containing 'total','energy use total' and the rest
        #now with added '(VAT)' and total inc vat
        self.rect(2.55,9.12+16+self.SINGLE_LINE_SPACE,w=14.524,h=0.85+ self.SINGLE_LINE_SPACE*2)
        self.rect(7.1,9.12+16+self.SINGLE_LINE_SPACE,w=4.8,h=0.85+self.SINGLE_LINE_SPACE*2)
        
    def put_month_dates_and_total(self,month,year):
        import datetime
        self.this_month = month
        self.this_year = year
        self.this_month_last_day= monthrange(year, month)[1]
        month_date_list = []
        for i in range(1,self.this_month_last_day + 1):
            s = datetime.datetime(year,month,i)
            s= s.strftime("%d/%m/%Y")
            month_date_list.append(s)
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(i-1))
            self.set_font('SourceSansPro-Regular','' , self.UPPER_BLOCK_FONT_SIZE)
            self.cell(w=1,h=1,align='R',txt=s,border=0)
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(31))    
            self.cell(w=1,h=1, align='R',txt='Total:',border=0)
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*32)
            self.cell(w=1,h=1, align='R', txt='(VAT)',border=0)
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*33)
            self.cell(w=0.75,h=1, align='R', txt='Total',border=0)
            self.set_font('SourceSansPro-Italic','',size= self.TABLE_FONT_SIZE)
            self.cell(w=0.7,h=1, align='R', txt= 'inc. ',border=0)
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*33)           
            self.set_font('SourceSansPro-Regular','',size= self.TABLE_FONT_SIZE)
            self.cell(w=2,h=1, align='R', txt='VAT:',border=0)
        
    def put_custom_dates_and_total(self,post_table_for_pdf):
        import datetime
        counter = 1
        for i in post_table_for_pdf.index:
            s = i.strftime("%d/%m/%Y")
            self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(counter-1))
            self.set_font('SourceSansPro-Regular','' , self.UPPER_BLOCK_FONT_SIZE)
            self.cell(w=1,h=1,align='R',txt=s,border=0)
            counter += 1
            
        self.set_xy(self.DATE_ALIGN+1.2, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(31))
        self.cell(w=1,h=1, align='R',txt='Total:',border=0)
        
        self.set_xy(self.DATE_ALIGN+1.2, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*32)
        self.cell(w=1,h=1, align='R', txt='(VAT)',border=0)
        
        self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*33)
        self.cell(w=0.77,h=1, align='R', txt='Total',border=0)
        
        self.set_font('SourceSansPro-Italic','',size= self.TABLE_FONT_SIZE)
        self.cell(w=0.77,h=1, align='R', txt= 'inc. ',border=0)
        
        self.set_xy(self.DATE_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*33)       
        self.set_font('SourceSansPro-Regular','',size= self.TABLE_FONT_SIZE)
        self.cell(w=2.2,h=1, align='R', txt='VAT:',border=0)                   
        
    def put_energy_list(self, energy_list):
        energy_list.append(sum(energy_list))        
        for i in range(1,len(energy_list)+1):
            output = (abs(round(energy_list[i-1],4)))
            output  = "{:.2f}".format(output)

            self.set_xy(self.ENERGY_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(i-1))
            if i == max(range(1,len(energy_list)+1)):
                self.set_xy(self.ENERGY_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(31))
                
            self.set_font('SourceSansPro-Regular','' , self.UPPER_BLOCK_FONT_SIZE)
            self.cell(w=1,h=1,align='R',txt=output,border=0)
            
    def put_cost_list(self, cost_list,vat_rate):
        import copy
        cost_list.append(sum(cost_list))
        for i in range(1,len(cost_list)+1):
            pre_format_cost = abs(round(cost_list[i-1],4))
            cost = "{:.2f}".format(pre_format_cost)

            self.set_xy(self.COST_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(i-1))
            if i == max(range(1,len(cost_list)+1)):
                pre_total = copy.deepcopy(pre_format_cost)
                cost = '£ '+cost
                self.set_xy(self.COST_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*(31))               
            
            self.set_font('SourceSansPro-Regular','' , self.UPPER_BLOCK_FONT_SIZE)
            self.cell(w=1,h=1,align='R',txt=cost,border=0)
        
        vat_figure= vat_rate*0.01*pre_total
        final_total = vat_figure + pre_total        

        vat_figure =  "{:.2f}".format(vat_figure)
        final_total =  "{:.2f}".format(final_total)
        
        vat_figure ='£ '+vat_figure
        final_total = '£ '+final_total
        
        self.set_xy(self.COST_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*32)
        self.cell(w=1,h=1, align='R', txt=vat_figure, border= 0)
            
        self.set_xy(self.COST_ALIGN, self.FIRST_LINE_TABLE + self.TABLE_LINE_SPACE*33)
        self.cell(w=1,h=1, align='R', txt=final_total,border=0)
       
    def footer(self):
        text_line1 = 'Registered Office: The Oast House, Moat Lane, Cowden, Kent TN8 7DP.'
        self.set_y(-7)
        self.set_font('SourceSansPro-Regular','', 10)
        self.cell(w=0, h=10, align='C',txt=text_line1,border=0)
        text_line2 = 'Company No: 10980144'
        self.set_y(-6.5)
        self.set_font('SourceSansPro-Regular','', 10)
        self.cell(w=0, h=10, align='C',txt=text_line2,border=0)
        




def format_date(str_date):
    year = str_date[0:4]
    month = str_date[5:7]
    day = str_date[-2:]
    return day+'/'+month+'/'+year


def produce_pdf(pdf, d, month_input, year_input, post_table_for_pdf,vat_rate,input_date=None, take_custom_dates=True):

    pdf.add_page()
    pdf.get_fonts()
    pdf.put_logo()
    pdf.write_title()
    pdf.write_client_name(d['client_name'])
    pdf.write_report_number(d['report_number'])
    
    pdf.write_period_start(d['period_start'])
    pdf.write_period_end(d['period_end'])
    pdf.write_elec_provider(d['provider'])
    pdf.write_tariff_name(d['tariff_name'])
    pdf.write_tariff_gbpkwh(d['tariff'])
    pdf.write_vat_rate(vat_rate)
    if input_date != '':
        pdf.write_date(input_date)
    elif input_date == '':
        pdf.write_date(d['day'])
    pdf.write_charger_reference(d['charger_reference'])
    pdf.write_charger_name(d['charger_name'])
    pdf.put_table_header()
    pdf.put_table_lines()
    

    if take_custom_dates == False:
        pdf.put_month_dates_and_total(month_input,year_input)

    if take_custom_dates == True:
        pdf.put_custom_dates_and_total(post_table_for_pdf)

        
    
    pdf.put_energy_list(post_table_for_pdf['energy_use'].tolist())
    pdf.put_cost_list(post_table_for_pdf['cost'].tolist(),vat_rate)
    
    return pdf

def make_details_dict(details_df,period_start,period_end):
    
    d = details_df.to_dict(orient='records')[0]
  
    if period_start.day != 1:
        period_start = period_start.replace(day=1)
    
    d['day'] = datetime.datetime.today()
    d['day'] = format_date(str(d['day'])[0:10])
    
    period_start_str = str(period_start)
    period_end_str = str(period_end)

    d['period_start'] = format_date(period_start_str)
    d['period_end']=  format_date(period_end_str)
    return d

def make_post_table(details_df,get_actual_period_end):
    pre_table_for_pdf = details_df[['day','energy_use','cost']].sort_values(by='day')

    month_input = pre_table_for_pdf['day'].iloc[0].month
    year_input = pre_table_for_pdf['day'].iloc[0].year

    pre_table_for_pdf = pre_table_for_pdf.set_index('day')  
    
    first_day= pre_table_for_pdf.index[0].day
    
    period_end_day = details_df['period_end'].iloc[0]
    last_day = pre_table_for_pdf.index[-1]
    last_day_number = last_day.replace(day = int(period_end_day)).day

    date_needed_last_day = last_day.replace(day = int(period_end_day))
    
    if get_actual_period_end == False:
        date_needed_last_day = date_needed_last_day
        last_day_number = last_day.replace(day = int(period_end_day)).day
    if get_actual_period_end == True:
        date_needed_last_day = last_day
        last_day_number = last_day.day
   
    details_dict = make_details_dict(details_df,pre_table_for_pdf.index[0], date_needed_last_day)

    num_of_days = last_day_number - first_day +1
    dummy_energy_list = [0]*num_of_days
    dummy_energy_list = [np.nan for a in dummy_energy_list]
    dummy_cost_list  = [details_dict['tariff']*a for a in dummy_energy_list]
    all_days_list = [datetime.date(year_input,month_input,a) for a in list(range(first_day,last_day_number+1))]

    post_table_for_pdf = pd.DataFrame(dummy_energy_list,all_days_list)
    post_table_for_pdf.columns =['energy_use']
    post_table_for_pdf['cost'] = dummy_cost_list

    for i in post_table_for_pdf.index:
        try:
            if pre_table_for_pdf['energy_use'].loc[i] != 0:
                post_table_for_pdf['energy_use'].loc[i] = pre_table_for_pdf['energy_use'].loc[i]
                post_table_for_pdf['cost'].loc[i] = pre_table_for_pdf['cost'].loc[i]
        except:
            pass

    post_table_for_pdf = post_table_for_pdf.fillna(0)
    return post_table_for_pdf, details_dict

def get_month(details_dict):
    return int(details_dict['period_start'].split('/')[1])

def get_year(details_dict):
    return int(details_dict['period_start'].split('/')[2])
    
def generate_reports(file_name, input_date= None, get_actual_period_end=True):
    

    

    print('reading from csv')
    details_df = pd.read_csv(file_name)
    details_df['day'] = pd.to_datetime(details_df['day'],dayfirst=True).dt.date
    details_df['cost'] = details_df['tariff']*details_df['energy_use']
    details_df['energy_use'] = details_df['energy_use'].apply(lambda x: round(x,4))
    details_df['cost'] = details_df['cost'].apply(lambda x: round(x,4))    
    vat_rate = details_df['vat_home'].iloc[0]
    unique_names = details_df['charger_name'].unique().tolist()

    list_detail_dfs  = []
    list_post_table_for_dfs = []  
    list_pdf_strings= []     

    for unique_name in unique_names:
        df_needed =  details_df[details_df['charger_name'] == unique_name]
        list_detail_dfs.append(df_needed)
        
        report_number = df_needed['report_number'].iloc[0]
        post_table_for_pdf,details_dict = make_post_table(df_needed,get_actual_period_end)
        list_post_table_for_dfs.append(post_table_for_pdf)        
        
        year_input = get_year(details_dict)
        month_input = get_month(details_dict)
        
        vat_rate = 100*details_dict['vat_home']
        pdf = PDF(orientation='P', unit='cm', format='A4')
        pdf = produce_pdf(pdf, details_dict, month_input, year_input, post_table_for_pdf,vat_rate, input_date, take_custom_dates =True)
        now = datetime.datetime.utcnow()

        
        pdf_name = report_number +'.pdf'
        pdf.output(pdf_name,'F')
        pdf_string = pdf.output(dest='S').encode('latin-1')
        
        list_pdf_strings.append(pdf_string)
        print('Generated PDF: ', pdf_name)
        print('_______________________________________________________')
    return details_df


list_csvs= os.listdir()
list_csvs = [f for f in list_csvs if '.csv' in f]
print('List of csvs found is:', list_csvs)
print('_______________________________________________________')
input_date = input('Enter date needed to be printed on report for date of issue in dd/mm/yyyy format. Press ENTER to use todays date: ')
for f in list_csvs:
    print('Reading csv: ',f )
    generate_reports(f,input_date)
    