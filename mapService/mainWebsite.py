import streamlit as st
import folium
from streamlit_folium import st_folium
from controller.analytic_controller import AnalyticController



class Web:
    def __init__(self):
        self.APP_TITLE = 'Heat Map'
        self.APP_SUB_TITLE = 'Sourse: Челябинск'

    def display_price_filter(self):
        start_price, end_price = st.sidebar.select_slider(
            "Укажите цену:",
            options=range(1000, 10000000),
            value=(10000, 1000000))
        return start_price, end_price

    def display_total_area_filter(self):
        start_total_area, end_total_area = st.sidebar.select_slider(
            "Укажите площадь:",
            options=range(0, 300),
            value=(0, 300))
        return start_total_area, end_total_area

    def display_floor_filter(self):
        start_floor, end_floor = st.sidebar.select_slider(
            "Укажите этаж:",
            options=range(0, 100),
            value=(0, 100))
        return start_floor, end_floor

    def display_housing_type_filter(self):
        new_building = st.checkbox('Новостройка')
        resale = st.checkbox('Вторичка')
        return new_building, resale

    def display_repair_filter(self):
        repair = st.checkbox('Ремонт')

    def display_map(self, price, total_area, housing_type, repair, floor):
        map = AnalyticController().get_map("Челябинск", price=price, housing_type=housing_type, repair=repair,total_area=total_area, floor=floor)

        st_map = st_folium(map, width=700, height=450)


    # def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}',
    #                         is_median=False):
    #     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    #     df = df[df['Report Type'] == report_type]
    #     if state_name:
    #         df = df[df['State Name'] == state_name]
    #     df.drop_duplicates(inplace=True)
    #     if is_median:
    #         total = df[field].sum() / len(df[field]) if len(df) else 0
    #     else:
    #         total = df[field].sum()
    #     st.metric(title, string_format.format(round(total)))


    def main(self):
        st.set_page_config(self.APP_TITLE)
        st.title(self.APP_TITLE)
        st.caption(self.APP_SUB_TITLE)

        # FILTERS
        self.start_price, self.end_price = self.display_price_filter()
        self.start_total_area, self.end_total_area = self.display_total_area_filter()
        self.start_floor, self.end_floor = self.display_floor_filter()
        self.new_building, self.resale = self.display_housing_type_filter()
        self.repair = self.display_repair_filter()
        st.write()




if __name__ == "__main__":
    Web().main()