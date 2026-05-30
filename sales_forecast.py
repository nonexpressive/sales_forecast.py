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
   selected_month = st.selectbox(
       'Select a 2025 month to forecast: ',
       forecast_months
   )

   if selected_month in df_2024['Month'].values and selected_month in df_2025['Month'].values:
       sales_2024 = df_2024[df_2024['Month'] == selected_month]['Sales'].iloc[0]
       sales_2025 = df_2025[df_2025['Month'] == selected_month]['Sales'].iloc[0]

       growth_rate = (sales_2025 - sales_2024) / sales_2024
       predicted_2026 = sales_2025 * (1+ growth_rate)

       if predicted_2026 > sales_2024 and predicted_2026 > sales_2025:
           predicted_color = 'green'
       elif predicted_2026 < sales_2024 and predicted_2026 < sales_2025:
           predicted_color = 'red'
       else:
           predicted_color = 'goldenrod'
       st.markdown(
           f"Predicted {selected_month} 2026 Sales: "
           f"<span style='color: {predicted_color};'>${predicted_2026:.2f}</span>",
           unsafe_allow_html=True
       )
       
   else:
       st.write('Data unavailable')

# Creates tabs.
def tabs():
    tab1, tab2 = st.tabs(['Comparisons', 'Forecast'])

    with tab1:
        st.header('Comparisons')
        compare_selected_month()

    with tab2:
        st.header('Forecasts')
        forecast_2026_sales()
        st.write('Sales forecasts are based on 2024 and 2025 sales data.\n' \
        'If predicted sales are more than 2024 and 2025 sales, the number' \
        ' will appear green. If predicted sales are in between 2024 and 2025 ' \
        'sales, the number will appear yellow. If predicted sales are ' \
        'less than both 2024 and 2025 sales, the number will appear red.')          

get_input()
tabs()



