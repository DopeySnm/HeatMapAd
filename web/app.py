from flask import Flask, render_template, request
from controller.analytic_controller import AnalyticController
app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'Составить карту':
            min_total_area = request.form["min_total_area"]
            max_total_area = request.form["max_total_area"]
            min_price = request.form["min_price"]
            max_price = request.form["max_price"]
            min_floor = request.form["min_floor"]
            max_floor = request.form["max_floor"]
            housing_type = request.form["housing_type"]

            path_save_map = r"C:\Users\Acer\PycharmProjects\HeatMapAd\web\static\map.html"
            AnalyticController().get_map_html("Челябинск", name_path=path_save_map, max_price=max_price, min_price=min_price, max_total_area=max_total_area, min_total_area=min_total_area, min_floor=min_floor, max_floor=max_floor, housing_type=housing_type)
            return render_template('index.html', form="form")
    return render_template("index_base.html")

if __name__ =='__main__':
    app.run(debug=True)