from flask import Flask,render_template,request, redirect
from bokeh.plotting import figure, output_file, save
from bokeh.models.formatters import DatetimeTickFormatter
import quandl
import datetime
import numpy as np
import pandas as pd

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('get_stocks_form.html')
    else:
        #request was a POST
        app.vars['name'] = request.form['name']
        cols = []
        if (request.form.get('col0') != None):
            cols.append(0)
            
        if (request.form.get('col3') != None):
            cols.append(3)

        if (request.form.get('col7') != None):
            cols.append(7)
            
        if (request.form.get('col10') != None):
            cols.append(10)            
        
        myname = app.vars['name']
        plot_stock_data(myname,cols)
        return render_template('stocks_plot.html')


def plot_stock_data(code,cols):
    stock_code = 'WIKI/' + code
    tday_str = datetime.datetime.now().strftime("%Y-%m-%d")
    month_before = int(tday_str[5:7])-1
    if month_before ==0:
        month_before = 12
    strt_date = tday_str[:5] + format(month_before, '02') + tday_str[7:]
    data = quandl.get(stock_code,start_date=strt_date,end_date=tday_str)
    title_str = 'Stock Price of ' + code + ' in last month'
    stock_plot = figure(title=title_str,x_axis_label='date',y_axis_label='price',plot_width=250*2, plot_height=250*2)
    colors = ["blue","red","green","yellow"]
    for col,color in zip(cols,colors):
        stock_plot.line(data.index.values,data[data.columns[col]],legend=str(data.columns[col]),line_color=color)
    
    stock_plot.xaxis.formatter = DatetimeTickFormatter(days = ['%m/%d', '%a%d'])
    output_file("templates/stocks_plot.html")
    save(stock_plot)


if __name__ == "__main__":
    app.run(debug=True)
