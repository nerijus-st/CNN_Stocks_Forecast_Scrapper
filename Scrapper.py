import csv
import os
import re
import sys
import time
from datetime import datetime

import pandas
import requests
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bs4 import BeautifulSoup

start_time = datetime.now()


class Scrapper:
    filename = sys.argv[1]

    def __init__(self):
        self.forecast_file = "forecast_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        self.cnn_scrapper()
        self.draw_graph()

    def cnn_scrapper(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                symbol = row['Symbol']
                print("Scrapping {}".format(symbol))

                # request = requests.get("http://money.cnn.com/quote/forecast/forecast.html?symb={}".format(symbol))
                request = self.get_content("http://money.cnn.com/quote/forecast/forecast.html?symb={}".format(symbol))
                content = request.content

                soup = BeautifulSoup(content, "html.parser")

                forecast = soup.find("div", {"class": "wsod_twoCol clearfix"})

                if forecast is not None:
                    self.create_csv(symbol, forecast)

    def get_content(self, url):
        try:
            return requests.get(url)
        except Exception:
            # sleep for a bit in case that helps
            time.sleep(3)
            # try again
            return self.get_content(url)

    def create_csv(self, symbol, forecast):
        if os.path.exists(self.forecast_file + ".csv") is False:
            headers = ["Symbol", "Analysts", "Months", "Median_target",
                       "High", "Low", "Median_pct", "Last_price", "Color"]
            self.create_headers(headers)

        forecast_text = [forecast.find("p").text]

        if forecast_text[0] != 'There is no forecast data available.':
            forecast = [symbol] + self.format_forecast(forecast_text)

            with open(self.forecast_file + ".csv", 'a+', newline="") as csvfile:
                forecast_writer = csv.writer(csvfile, dialect='excel')
                # for item in forecast:
                #     forecast_writer.writerow([item])
                forecast_writer.writerow(f for f in forecast)

    def create_headers(self, headers):
        with open(self.forecast_file + ".csv", 'a+', newline="") as csvfile:
            forecast_writer = csv.writer(csvfile, dialect='excel')
            forecast_writer.writerow(header for header in headers)

    def format_forecast(self, forecast):
        forecast_formatted = []

        analysts = int(self.reg_search('(?<=The )[0-9]+', forecast[0]))
        months = int(self.reg_search('(?<=offering )[0-9]+', forecast[0]))
        median_target = float(self.reg_search('(?<=median target of )[0-9]+.[0-9]+', forecast[0]).replace(',', ''))
        high = float(self.reg_search('(?<=high estimate of )[0-9]+.[0-9]+', forecast[0]).replace(',', ''))
        low = float(self.reg_search('(?<=low estimate of )[0-9]+.[0-9]+', forecast[0]).replace(',', ''))
        median_pct = float(self.reg_search('(?<=represents a ).[0-9]+.[0-9]+', forecast[0]).replace(',', ''))
        last_price = float(self.reg_search('(?<=last price of )[0-9]+.[0-9]+', forecast[0]).replace(',', ''))
        color = self.get_color(median_pct)

        forecast_formatted.extend([analysts, months, median_target, high, low, median_pct, last_price, color])

        return forecast_formatted

    @staticmethod
    def reg_search(reg, val):
        found = re.search(reg, val)
        if found:
            return found.group(0)
        else:
            return '0'

    def draw_graph(self):
        print("************************")
        print("Will draw a graph now...")
        df = pandas.read_csv(self.forecast_file + ".csv")

        source = ColumnDataSource(df)

        # y = df["Median_pct"]
        x = [symb for symb in df["Symbol"]]

        output_file(self.forecast_file + ".html")

        p = figure(x_range=x,
                   title="CNN IT Stocks Forecast", logo=None)  # sizing_mode="scale_width"

        p.title.text_font_size = "36px"
        p.circle(x='Symbol', y='Median_pct', color="Color", size=15, source=source)

        hover = HoverTool(tooltips=[("Symbol", "@Symbol"), ("Analysts", "@Analysts"), ("Months", "@Months"),
                                    ("Median target", "@Median_target"), ("High", "@High"), ("Low", "@Low"),
                                    ("Median %", "@Median_pct"), ("Last_price", "@Last_price")])
        p.add_tools(hover)
        show(p)

    @staticmethod
    def get_color(median_pct):
        if median_pct <= -50:
            return "darkred"
        elif -50 < median_pct <= -15:
            return "red"
        elif -15 < median_pct <= 0:
            return "orange"
        elif 0 < median_pct <= 10:
            return "yellow"
        else:
            return "green"


scrapper = Scrapper()
print("************************")
print("Total runtime: {}".format(datetime.now() - start_time))
print("************************")
