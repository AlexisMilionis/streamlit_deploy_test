import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns
from constants import Constants
import plotly.express as px
import pandas as pd
# Create figure with secondary y-axis
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Metrics:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.billing_account_fields = ["ΛΟΓΑΡ. ΥΔΡΕΥΣΗΣ", "ΛΟΓΑΡΙΑΣΜΟΣ ΛΑΘΡΑΙΑΣ ΥΔΡΟΛΗΨΙΑΣ"]
        self.rest_billing_account_fields = ["BEBAIΩΜΕΝΗ ΠΡΟΣΑΥΞΗΣΗ", "ΑΠΟΔΕΙΞΗ ΕΙΣΠΡΑΞΗΣ ΔΙΚΑΣΤΙΚΩΝ ΕΞΟΔΩΝ", "ΒΕΒΑΙΩΜΕΝΟΣ ΤΟΚΟΣ ΕΚΠΡΟΘΕΣΜΗΣ ΟΦΕΙΛΗΣ", "ΛΟΙΠΩΝ ΥΠΗΡΕΣΙΩΝ"]
                
        # total consumption
        self.portfolio['consumption'] = self.portfolio['ΚΥΒΙΚΑ 1'].fillna(0) + \
                                    self.portfolio['ΚΥΒΙΚΑ 2'].fillna(0) + \
                                    self.portfolio['ΚΥΒ.3'].fillna(0) + \
                                    self.portfolio['ΚΥΒ.4'].fillna(0) + \
                                    self.portfolio['ΚΥΒ.5'].fillna(0)
        self.bills = self.portfolio[self.portfolio['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.billing_account_fields)]
        # self.bills = self.bills[self.bills['consumption'] > 0] # Filter out rows with zero consumption
        
        # self.consumption_per_supply_id = self.bills.groupby('ΑΡ.ΠΑΡΟΧΗΣ').agg({'consumption': 'sum'}).reset_index()
        # self.debt_per_supply_id = self.bills.groupby('ΑΡ.ΠΑΡΟΧΗΣ').agg({'ΟΦΕΙΛΗ': 'sum'}).reset_index()
        self.supply_metrics = self.bills.groupby('ΑΡ.ΠΑΡΟΧΗΣ').agg({
            'consumption': 'sum',
            'ΟΦΕΙΛΗ': 'sum'
        }).reset_index()
        self.supply_metrics = self.supply_metrics[self.supply_metrics['consumption'] > 0] # Filter out rows with zero consumption
        self.supply_metrics['price_per_cubic_meter'] = self.supply_metrics['ΟΦΕΙΛΗ'] / self.supply_metrics['consumption']
        
    def calc_total_consumption(self):
        # ΣΥΝΟΛΙΚΗ ΚΑΤΑΝΑΛΩΣΗ ΣΤΟ ΛΟΓΑΡΙΑΣΜΟ
        return self.bills['consumption'].sum()
    
    def calc_median_consumption(self):
        # ΔΙΑΜΕΣΗ ΚΑΤΑΝΑΛΩΣΗ ΣΤΟ ΛΟΓΑΡΙΑΣΜΟ - ΜΟΝΟ ΛΟΓΑΡΙΑΣΜΟΥΣ ΥΔΡΕΥΣΗΣ
        return self.bills['consumption'].median()
    
    def calc_total_debt(self):
        # ΣΥΝΟΛΙΚΗ ΟΦΕΙΛΗ ΣΤΟ ΛΟΓΑΡΙΑΣΜΟ
        return self.portfolio['ΟΦΕΙΛΗ'].sum()
    
    def calc_median_debt_bills_only(self):
        # ΔΙΑΜΕΣΗ ΟΦΕΙΛΗ ΣΤΟ ΛΟΓΑΡΙΑΣΜΟ
        return self.bills['ΟΦΕΙΛΗ'].median()
    
    def calc_total_debt_bills_only(self):
        # ΣΥΝΟΛΙΚΗ ΟΦΕΙΛΗ ΣΤΟΥΣ ΛΟΓΑΡΙΑΣΜΟΥΣ ΥΔΡΕΥΣΗΣ
        return self.bills['ΟΦΕΙΛΗ'].sum()
    
    def calc_total_debt_non_bills(self):
        # ΣΥΝΟΛΙΚΗ ΟΦΕΙΛΗ ΣΤΟΥΣ ΛΟΓΑΡΙΑΣΜΟΥΣ ΜΗ ΥΔΡΕΥΣΗΣ
        return self.portfolio[self.portfolio['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.rest_billing_account_fields)]['ΟΦΕΙΛΗ'].sum()

    def calc_debt_per_consumption(self):
        # ΜΕΣΗ ΟΦΕΙΛΗ ΑΝΑ ΚΥΒΙΚΟ ΣΤΟ ΛΟΓΑΡΙΑΣΜΟ - ΜΟΝΟ ΛΟΓΑΡΙΑΣΜΟΥΣ ΥΔΡΕΥΣΗΣ + ΜΗ ΜΗΔΕΝΙΚΗ ΚΑΤΑΝΑΛΩΣΗ
        return self.calc_total_debt_bills_only() / self.bills[self.bills['consumption'] > 0].sum()
    
    def calc_top_debts(self):
        # Ν ΥΨΗΛΟΤΕΡΕΣ ΟΦΕΙΛΕΣ 
        top_debt_rows = self.supply_metrics.nlargest(5, 'ΟΦΕΙΛΗ')
        # print(f"Top debt ids: {top_debt_rows[['ΑΡ.ΠΑΡΟΧΗΣ', 'ΟΦΕΙΛΗ']]}")
        df = top_debt_rows[['ΑΡ.ΠΑΡΟΧΗΣ', 'ΟΦΕΙΛΗ']].reset_index(drop=True)
        df.index = df.index + 1
        df.rename(columns={'ΟΦΕΙΛΗ': 'Debt (€)', 'ΑΡ.ΠΑΡΟΧΗΣ': 'Supply ID'}, inplace=True)
        return df

    def calc_top_consumptions(self):
        # Ν ΥΨΗΛΟΤΕΡΕΣ ΚΑΤΑΝΑΛΩΣΕΙΣ - ΜΟΝΟ ΛΟΓΑΡΙΑΣΜΟΥΣ ΥΔΡΕΥΣΗΣ
        top_consumption_rows = self.supply_metrics.nlargest(5, 'consumption')
        # print(f"Top consumption ids: {top_consumption_ids[['ΑΡ.ΠΑΡΟΧΗΣ', 'consumption']]}")
        df = top_consumption_rows[['ΑΡ.ΠΑΡΟΧΗΣ', 'consumption']].reset_index(drop=True)
        df.index = df.index + 1
        df.rename(columns={'consumption': 'Consumption (m³)', 'ΑΡ.ΠΑΡΟΧΗΣ': 'Supply ID'}, inplace=True)
        return df

    def calc_top_debts_per_consumption_per_supply(self):
        # Ν ΠΑΡΟΧΕΣ ΜΕ ΥΨΗΛΟΤΕΡΕΣ ΤΙΜΕΣ ΑΝΑ ΚΥΒΙΚΟ
        supply_metrics_filtered = self.supply_metrics[self.supply_metrics['price_per_cubic_meter'] != float('inf')]
        top_debts_per_consumption_rows = supply_metrics_filtered.nlargest(5, 'price_per_cubic_meter')
        # print(f"calc_top_debts_per_consumption_per_supply ids: {top_debts_per_consumption_rows[['ΑΡ.ΠΑΡΟΧΗΣ', 'price_per_cubic_meter']]}")
        df = top_debts_per_consumption_rows[['ΑΡ.ΠΑΡΟΧΗΣ', 'price_per_cubic_meter']].reset_index(drop=True)
        df.index = df.index + 1
        df.rename(columns={'price_per_cubic_meter': 'Price per cubic meter (€/m³)', 'ΑΡ.ΠΑΡΟΧΗΣ': 'Supply ID'}, inplace=True)
        return df

    def calc_bill_debt_vs_consumption_vs_time(self, supply_id=None):
        if supply_id:
            self.bills = self.bills[self.bills['ΑΡ.ΠΑΡΟΧΗΣ'] == int(supply_id)]
            if self.bills.empty:
                st.warning(f"No data found for Supply ID: {supply_id}")
                return

        processed_month = self.bills['Processed_Month'].unique()
        
        monthly_data = []
        
        for i, month in enumerate(processed_month):
            month_data = self.bills[self.bills['Processed_Month'] == month]
            month_bills = month_data[month_data['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.billing_account_fields)]
            monthly_consumption = month_bills['consumption'].sum()
            monthly_bill_debt = month_bills['ΟΦΕΙΛΗ'].sum()
            
            # Convert YYYYMM format to readable date
            year = int(str(month)[:4])
            month_num = int(str(month)[4:6])
            month_label = pd.to_datetime(f"{year}-{month_num:02d}-01").strftime('%b %Y')
            
            monthly_data.append({
                'Month': month,
                'Month_Label': month_label,
                'Consumption': monthly_consumption,
                'Debt': monthly_bill_debt
            })
            
        df = pd.DataFrame(monthly_data)
        df = df.sort_values('Month')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add debt trace (left y-axis)
        fig.add_trace(
            go.Scatter(x=df['Month_Label'], y=df['Debt'], name="Bill Debt (€)", 
                    line=dict(color=Constants.PRIMARY_COLOR, width=2)),
            secondary_y=False,
        )
        
        # Add consumption trace (right y-axis)
        fig.add_trace(
            go.Scatter(x=df['Month_Label'], y=df['Consumption'], name="Consumption (m³)", 
                    line=dict(color='#FF6B6B', width=2)),
            secondary_y=True,
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Bill Debt (€)", secondary_y=False)
        fig.update_yaxes(title_text="Consumption (m³)", secondary_y=True)
        
        fig.update_layout(
            title_text="Monthly Bill Debt vs Consumption",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def display_monthly_kpis(self):
        
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.metric(label="Total Debt (€)", value=f"{self.calc_total_debt():,.1f}", border=True)
        with row1_col2:
            st.metric(label="Median Debt from billings (€)", value=f"{self.calc_median_debt_bills_only():,.1f}", border=True)
        
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.metric(label="Total Debt from billings (€)", value=f"{self.calc_total_debt_bills_only():,.1f}", border=True)
        with row2_col2:
            st.metric(label="Total Debt from Accrued Late Payment Charges (€)", value=f"{self.calc_total_debt_non_bills():,.1f}", border=True)
            
        row3_col1, row3_col2 = st.columns(2)
        with row3_col1:
            st.metric(label="Total Consumption (m³)", value=f"{self.calc_total_consumption():,.1f}", border=True)
        with row3_col2:
            st.metric(label="Median Consumption (m³)", value=f"{self.calc_median_consumption():,.1f}", border=True)
            
        row4_col1, row4_col2, row4_col3 = st.columns(3)
        with row4_col1:
            st.write("Top 5 monthly Debts")
            st.dataframe(self.calc_top_debts())
        with row4_col2:
            st.write("Top 5 monthly Consumptions")
            st.dataframe(self.calc_top_consumptions())
        with row4_col3:
            st.write("Top 5 monthly Price per cubic meter (€/m³)")
            st.dataframe(self.calc_top_debts_per_consumption_per_supply())
            
    
    def display_historical_kpis(self):

        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            st.metric(label="Median Debt from billings (€)", value=f"{self.calc_median_debt_bills_only():,.1f}", border=True)
        with row1_col2:
            st.metric(label="Median Consumption (m³)", value=f"{self.calc_median_consumption():,.1f}", border=True)
        with row1_col3:
            st.metric(label="Median Debt from Accrued Late Payment Charges (€)", value=f"{self.calc_total_debt_non_bills():,.1f}", border=True)
        self.calc_bill_debt_vs_consumption_vs_time()
    
    def display_supply_id_info(self, supply_id):
        supply_data = self.portfolio[self.portfolio['ΑΡ.ΠΑΡΟΧΗΣ'] == int(supply_id)]
        if supply_data.empty:
            st.warning(f"No data found for Supply ID: {supply_id}")
            return
        total_consumption = supply_data['consumption'].sum()
        total_debt = supply_data['ΟΦΕΙΛΗ'].sum()
        bill_debt = supply_data[supply_data['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.rest_billing_account_fields)]['ΟΦΕΙΛΗ'].sum()
        non_bill_debt = supply_data[~supply_data['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.rest_billing_account_fields)]['ΟΦΕΙΛΗ'].sum()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Consumption (m³)", value=total_consumption, border=True)
        with col2:
            st.metric(label="Total Debt (€)", value=total_debt, border=True)
        with col3:
            st.metric(label="Debt from billings (€)", value=bill_debt, border=True)
        with col4:
            st.metric(label="Debt from Accrued Late Payment Charges (€)", value=non_bill_debt, border=True)
        
    def display_historical_supply_id_info(self, supply_id):
        supply_data = self.portfolio[self.portfolio['ΑΡ.ΠΑΡΟΧΗΣ'] == int(supply_id)]
        if supply_data.empty:
            st.warning(f"No data found for Supply ID: {supply_id}")
            return
        total_consumption = supply_data['consumption'].sum()
        total_debt = supply_data['ΟΦΕΙΛΗ'].sum()
        bill_debt = supply_data[supply_data['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.rest_billing_account_fields)]['ΟΦΕΙΛΗ'].sum()
        non_bill_debt = supply_data[~supply_data['ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'].isin(self.rest_billing_account_fields)]['ΟΦΕΙΛΗ'].sum()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Consumption (m³)", value=total_consumption, border=True)
        with col2:
            st.metric(label="Total Debt (€)", value=total_debt, border=True)
        with col3:
            st.metric(label="Debt from billings (€)", value=bill_debt, border=True)
        with col4:
            st.metric(label="Debt from Accrued Late Payment Charges (€)", value=non_bill_debt, border=True) #TODO: na allaksei, einai lathos giati pairnei kai alles times tou typos logariasmou
        self.calc_bill_debt_vs_consumption_vs_time(supply_id=supply_id)



    def build_scatterplot(self):
        fig = px.scatter(
            self.supply_metrics,
            x='consumption',
            y='ΟΦΕΙΛΗ',
            title="Water Consumption vs Debt per Supply ID",
            hover_data=['ΑΡ.ΠΑΡΟΧΗΣ'],  # Supply ID shown on hover
            labels={
                "consumption": "Total Water Consumption (m³)",
                "ΟΦΕΙΛΗ": "Total Debt (€)"
            },
            color_discrete_sequence=[Constants.PRIMARY_COLOR]
        )

        st.plotly_chart(fig)
        
        
    

