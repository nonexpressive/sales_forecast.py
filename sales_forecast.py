import pandas as pd
import streamlit as st

df_2026 = pd.read_excel('2026_sales.xlsx')
df_2025 = pd.read_excel('sales_2025.xlsx')

# List of months to pull from.
months = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']

# List of months for 2026 predictions to pull from.
forecast_months = ['June', 'July', 'August', 'September',
                   'October', 'November', 'December']

# Display sales information
def display_sales(df, selected_month):
    if selected_month in df['Month'].values:
        selected_row = df[df['Month'] == selected_month]
        sales = selected_row['Sales'].iloc[0]

        st.write('Sales: ', f'${sales:.2f}')
    else:
        st.write('Data unavailable')

# Get user input: Has the user select a month
# and displays the sales data from that month.
def get_input():
    st.title('Sales Forecast')

    st.subheader('2025 Sales Data')
    select_month_2025 = st.selectbox(
        'Select a month for 2025: ', months
    )

    display_sales(df_2025, select_month_2025)

    st.subheader('2026 Sales Data')
    select_month_2026 = st.selectbox(
        'Select a month for 2026: ', months
    )

    display_sales(df_2026, select_month_2026)

# Compares each month's sales data.
def compare_all_months():
    comparison = pd.merge(
        df_2025,
        df_2026,
        on='Month',
        suffixes=('_2025', '_2026')
    )

    comparison['Difference'] = comparison['Sales_2026'] - comparison['Sales_2025']
    st.write(comparison)

# Compares each month's sales data and displays a
# selectbox so the user can compare each month.
def compare_selected_month():
    select_month = st.selectbox(
        'Select a month to compare: ',
        months
    )

    if select_month in df_2025['Month'].values and select_month in df_2026['Month'].values:
        sales_2025 = df_2025[df_2025['Month'] == select_month]['Sales'].iloc[0]
        sales_2026 = df_2026[df_2026['Month'] == select_month]['Sales'].iloc[0]
        
        difference = sales_2026 - sales_2025
        if difference >= 0:
            st.markdown(
                f"Difference from 2025 to 2026: "
                f"<span style='color: green;'>+${difference:.2f}</span>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                f"Difference from 2025 to 2026: "
                f"<span style='color: red;'>-${abs(difference):.2f}</span>",
                unsafe_allow_html=True
            )

        st.write(f'{select_month} 2025 Sales: ', f'${sales_2025:.2f}')
        st.write(f'{select_month} 2026 Sales: ', f'${sales_2026:.2f}')

    else:
        st.write('Data unavailable')

# Forecasting 2026 sales.
def forecast_2026_sales():
    df_2025['Growth'] = df_2025['Sales'].pct_change()
    average_growth = df_2025['Growth'].mean()

    last_sales = df_2025['Sales'].iloc[-1]

    predicted_sales = {}

    for month in forecast_months:
        last_sales = last_sales * (1 + average_growth)
        predicted_sales[month] = last_sales

    selected_month = st.selectbox('Select a 2026 month to forecast: ',
                                      forecast_months)
        
    st.write(
        f'Predicted {selected_month} 2026 Sales:',
        f'${predicted_sales[selected_month]:.2f}'
        )

# Creates tabs.
def tabs():
    tab1, tab2 = st.tabs(['Comparisons', 'Forecast'])

    with tab1:
        st.header('Comparisons')
        compare_selected_month()

    with tab2:
        st.header('Forecasts')
        forecast_2026_sales()

get_input()
tabs()



