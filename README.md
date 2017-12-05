<h1>CNN_Stocks_Forecast_Scrapper</h1>

This code will scrap CNN Money forecasts with given stocks in .csv format, parse them and will create a new .csv with scrapped date. Then will use this new file to draw a graph for visualizing highest and lowest predictions with more details for stocks.

<h3>Usage</h3>

Execute Scrapper.py and pass .csv with Stocks you want to parse. Stocks in given .csv file must be 1 per row with header of "Symbol".

<img src="https://user-images.githubusercontent.com/11758021/33607343-7de3b37c-d9c9-11e7-9369-cb8dd011abe0.png" />

Current status is shown in terminal

<img src="https://user-images.githubusercontent.com/11758021/33607756-ceaba084-d9ca-11e7-8258-986a85ac75a1.png" />

This will create a new forecast_(date).csv and forecast_(date).html files. Forecast_(date).html will open up immediately in default browser after completion.

You will get forecast details on hover.

Stocks with prediction higher than 10% will be in green, between 0% and 10% in yellow (exclusive), between 0% and -10% in orange(inclusive), below -10%(exclusive) in red.

<img src="https://user-images.githubusercontent.com/11758021/33607579-505a6b0c-d9ca-11e7-86aa-99e4a699ade3.png" />
