import flet as ft
import yfinance as yf
from datetime import datetime

def totalnum(days,everymo,stock):
    count = 0
    currentprice = 0
    totaldividends = 0
    num = 0
    print(days)
    d = yf.Ticker(stock)
    dividends = d.history(interval = '1mo',start = days[0] ,end = days[len(days)-1])
    true_days = days[0:len(days)-1]
    print(true_days)
    
    print(dividends['Dividends'])
    for i in true_days:
        startday = d.history(start = i)
        currentprice = startday['Close'][0]
        print(count)
        print('didends is ',dividends['Dividends'][count])
        print(f'buyinday is {i},price is {currentprice}')
        if dividends['Dividends'][count]>0:
            print('current num is ',num)
            totaldividends += num*dividends['Dividends'][count]
            print('cumulate to today',totaldividends)
        num += everymo/startday['Close'][0]

        count += 1
    print(num)
    return num,currentprice,totaldividends
def outputdate(start,day,year):
    date_list = []
    for j in range(int(year),0,-1):
        for i in range(int(start),13):
            date = date = '20'+str(int(datetime.now().strftime('%y'))-j)+'-'+str(i)+'-'+day
            date_list.append(date)
        if j == 1:
            for i in range(1,int(start)+1):
                date = date = '20'+str(int(datetime.now().strftime('%y'))-j+1)+'-'+str(i)+'-'+day
                date_list.append(date)
                print('rrr')
        else:    
            for i in range(1,int(start)):
                date = date = '20'+str(int(datetime.now().strftime('%y'))-j+1)+'-'+str(i)+'-'+day
                date_list.append(date)
    return date_list    
def stocktolist():
    stocks_list = []
    key = 0
    while key != 'n' and key != 'N':
        stocks = input('what stock do u want to buy')
        stocks_list.append(stocks)
        key = input('another?')
        print(f'{key}')
    return stocks_list 
def maybecostset(num_vars, target_sum, step=100, current_vars=None):
    if current_vars is None:
        current_vars = []
        
    if num_vars == 1:
        if target_sum % step == 0 and target_sum >= 0:
            return [current_vars + [target_sum]]
        else:
            return []
    
    solutions = []
    for x in range(0, target_sum + 1, step):
        solutions.extend(maybecostset(num_vars - 1, target_sum - x, step, current_vars + [x]))
    return solutions
def ROI(earn,cost):
    
    earning_list = []
    for k in range(int(len(earn)/2)):
        earning = 0
        for i in range(2):
            earning += earn[k+i][0]*earn[k+i][1]+earn[k+i][2]
        earning_list.append((earning-cost)/cost)    
    return earning_list    

def main(page: ft.Page):  
    global start_station, end_station
    
    page.title = "stocks advision"
    page.window_width = 1000
    page.window_height = 800
    #page.theme = theme.Theme(color_scheme_seed="green")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
    date_list = []
    stock_list = []
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
    def date_click(e):
        month = month_text.value
        year = year_text.value
        day = day_text.value
        date_list = outputdate(month,day,year)
        date_out.value = str(f'date list is : {date_list}')
        page.update()
    num = []
    def stock_click(e):
        stock = stock_txt.value
        stock_list.append(stock)
        choose_txt.value = str(f'this list is : {stock_list}')
        page.update()
    def result_click(e): 
        month = month_text.value
        year = year_text.value
        day = day_text.value
        date_list = outputdate(month,day,year)
        date_out.value = str(f'date list is : {date_list}')   
        total = int(money_txt.value)
        ratio = maybecostset(len(stock_list),total)
        for i in range(len(ratio)):
            count2 = 0
            for k in stock_list:
                print(f'current stock is {k} and num')
                num.append(totalnum(date_list,ratio[i][count2],k))
                count2 += 1
        difference = ROI(num,12000)
        difference.index(max(difference))
        result_txt.value = str(f'finally we adjust u buy those stocks {stock_list} by ratio {ratio[difference.index(max(difference))]} with ROI {max(difference)}')   
        page.update()
    #object
    month_text = ft.TextField(label="which month do u want to start", width=300, text_size=18)
    day_text = ft.TextField(label="which day do u want to invest", width=300, text_size=18)
    year_text = ft.TextField(label="how long will u invest", width=300, text_size=18)
    money_txt = ft.TextField(label='enter ur everymo money?',width=300, text_size=18)
    stock_txt = ft.TextField(label='which stock do u want to invest?',width=300, text_size=18)
    choose_txt = ft.Text('',size=18)
    date_out = ft.Text("", size=18)
    result_txt = ft.Text("",size=18)
    date_button = ft.ElevatedButton(text=f"confirm the date", width=300, on_click=date_click)
    stock_button = ft.ElevatedButton(text=f'confirm ur stock', width=300, on_click=stock_click)
    result_button = ft.ElevatedButton(text=f'find best solution',width=300,on_click=result_click)
    page.add(
        stock_txt,
        stock_button,
        ft.Row(
            [ month_text,
            day_text,
            year_text],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
            date_out,
            choose_txt,
            money_txt,
            result_button,
            result_txt
            )

ft.app(target=main)