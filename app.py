import streamlit as st
import pandas as pd
import numpy as np
import nsepy
from figures import *


# title to graph
st.title("Nifty 50 Stock Analysis")




st.sidebar.title('Nifty 50 Stock Analysis')

option = st.sidebar.radio(
    'Compare stocks ?',
    ('Yes', 'No')
)
st.sidebar.markdown('###### if you want to see only 1 stock analysis select no')


if(option == 'No'):

    # sidebar
    company_symbol = st.sidebar.text_input("enter company code")
    start_date = st.sidebar.date_input('from')
    end_date = st.sidebar.date_input('till')
    category = st.sidebar.radio(
        'Select Analysis',
        ('General', 'Volume and Delivery Analysis', 'Intraday Analysis')
    )
    state = st.sidebar.button('submit')


    # date is in "year-month-day"
    data = nsepy.get_history(symbol=company_symbol, start=start_date, end=end_date)
    data['time'] = pd.to_datetime(data.index)
    data['time'] = data['time'].dt.strftime("%Y-%m-%d")
    data.set_index(data['time'], inplace=True)
    data.dropna(inplace=True)
    data['Intraday Volume'] = data['Volume'] - data['Deliverable Volume']

    if state:

        HIGH_IN_RANGE = max(data['High'])
        LOW_IN_RANGE = min(data['Low'])
        OPEN_HIGH = max(data['Open'])
        OPEN_LOW = min(data['Open'])
        CLOSE_HIGH = max(data['Close'])
        CLOSE_LOW = min(data['Close'])
        AVERAGE_TURNOVER = np.mean(data['Turnover'])
        AVERAGE_VOLUME_TRADED = np.mean(data['Volume'])
        AVERAGE_PERCENTAGE_DELIVERY_VOLUME = np.mean(data['%Deliverble'])


        if (category == 'General'):

            col1, col2 = st.columns(2)
            with col1:
                st.write("High ", HIGH_IN_RANGE)

            with col2:
                st.write("Low ", LOW_IN_RANGE)

            with col1:
                st.write('Open(High)', OPEN_HIGH)
            with col2:
                st.write('Open(Low)', OPEN_LOW)

            with col1:
                st.write('Close(High)', CLOSE_HIGH)
            with col2:
                st.write('Close(Low)', CLOSE_LOW)

            st.write('Average turnover ', AVERAGE_TURNOVER)
            st.write('Average volume of traded ', AVERAGE_VOLUME_TRADED)
            st.write('Average % of delivery volume ', round(AVERAGE_PERCENTAGE_DELIVERY_VOLUME, 3),'%')

            # Highes profit that could have been made
            data['lowest_cumulative_price'] = data['Close'].cummin()
            data['highest_profit'] = data['Close'] - data['lowest_cumulative_price']
            st.write('Highest profit that could have been made', round(data['highest_profit'].max(), 3))
            # st.write(data['highest_profit'].max())

            # Loss that could have been made
            data['highest_cumulative_price'] = data['Close'].cummax()
            data['highest_loss'] = data['Close'] - data['highest_cumulative_price']
            st.write('Loss that could have been made', round(data['highest_loss'].min(), 3))
            # st.write(data['highest_loss'].min())


            st.markdown('## Candle Stick')
            st.write(Draw_candlestick(data))

            st.markdown('## Price Analysis')
            st.write(Draw_price(data))

            st.markdown('## Trend Analysis')
            st.write(Draw_trend(data))

            st.markdown('## VWAP')
            st.write(Draw_VWAP(data))


        elif (category == 'Volume and Delivery Analysis'):
            st.markdown('## Total Volume Trade')
            st.write(Draw_Volume(data))

            st.markdown('## Total Deliverable Volume')
            st.write(Draw_Deliverable_volume(data))


            st.markdown('# when deliverable volums is above')
            st.markdown('### when deliverable volume is above average')
            # above 50 percentile's delivery
            average_volume = np.mean(data['Deliverable Volume'])
            st.table(data[data['Deliverable Volume'] > average_volume]
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])


            st.markdown('### when deliverable volume is above 75 percentile')
            # above 75 percentile volume
            tmp = data['Deliverable Volume'].quantile(0.75)
            st.table(data[data['Deliverable Volume'] > tmp]
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])

            st.markdown('### when deliverable volume is above 90 percentile')
            # above 90 percentile volume
            tmp = data['Deliverable Volume'].quantile(0.9)
            st.table(data[data['Deliverable Volume'] > tmp]
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])



            st.markdown('# when delivery volume is below')
            st.markdown('### when delivery volume is below average')
            # below 50 percentile's delivery
            average_volume = np.mean(data['Deliverable Volume'])
            st.table(data[data['Deliverable Volume'] < average_volume][
                ['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])


            st.write('### when delivery volume is below 75 percentile')
            # below 75 percentile volume
            tmp = data['Deliverable Volume'].quantile(0.75)
            st.table(data[data['Deliverable Volume'] < tmp]
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])


            st.write('### when delivery volume is below 90 percentile')
            # below 90 percentile volume
            tmp = data['Deliverable Volume'].quantile(0.9)
            st.table(data[data['Deliverable Volume'] < tmp]
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])


        elif (category == 'Intraday Analysis'):
            st.write('top 5 days with high trade volume')
            st.table(data.sort_values(by='Trades', ascending=False).head()
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])

            st.write('top 10 days with high price')
            st.table(data.sort_values(by='High', ascending=False).head(10)
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])

            st.write('top 10 low price')
            st.table(data.sort_values(by='Low', ascending=True).head(10)
                     [['Close', 'High', 'Low', 'Volume', '%Deliverble', 'Trades']])


            st.write('intraday volumne V/S Deliverable volumne')
            st.write(Draw_Intraday_pie(data))



if (option == 'Yes'):
    st.sidebar.markdown('# Select Companies')
    name1 = st.sidebar.text_input(label='select first company')
    name2 = st.sidebar.text_input(label='select second company')
    name3 = st.sidebar.text_input(label='select third company')
    name4 = st.sidebar.text_input(label='select fourth company')
    name5 = st.sidebar.text_input(label='select fifth company')

    start_date = st.sidebar.date_input(label='start date')
    end_date = st.sidebar.date_input(label='end date')

    company_arr = [name1, name2, name3, name4, name5]
    cnt = 0
    names = []
    button = None
    for i in company_arr:
        if(i != ''):
            cnt+=1
            names.append(i)
    if(cnt <= 1):
        st.warning('need to select atleast two companies')
    else:
        button = st.sidebar.button(label='submit')

    if (button):

        # fetching data from api
        data_object = []
        for i in range(len(names)):
            data_object.append(nsepy.get_history(symbol=names[i], start=start_date, end=end_date))

        for i in range(len(data_object)):
            data_object[i]['time'] = pd.to_datetime(data_object[i].index)

            # new code for testing
            data_object[i]['time'] = data_object[i]['time'].dt.strftime("%Y-%m-%d")

            data_object[i].set_index(data_object[i]['time'], inplace=True)
            data_object[i].dropna(inplace=True)
            data_object[i]['Intraday Volume'] = data_object[i]['Volume'] - data_object[i]['Deliverable Volume']


        st.write('price movements over time')
        st.write(Draw_multi_line_plot(data_object, names))

        st.write('deliverable volume')
        st.write(Draw_deliverables_pie(data_object, names))

        st.write('intraday')
        st.write(Draw_intraday_pie(data_object, names))

        st.write('vwap')
        st.write(Draw_vwap_pie(data_object, names))