from flask import Flask, request, redirect, url_for, flash, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, \
RadioField, SelectField, TextAreaField, SubmitField

from wtforms.validators import DataRequired
from wtforms.widgets import TextInput
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 定義表單類
class StockForm(FlaskForm):
    stock_code = StringField('Stock Code', validators=[DataRequired(message="required")], widget=TextInput())
    submit = SubmitField('Get Stock Info')
    selectArea = SelectField('你的興趣', choices=[('sports','運動'),('travel','旅遊'),('movie','電影')])
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = StockForm()
    if form.validate_on_submit():
        stock_code = form.stock_code.data
        # For demonstration purposes, using a mock URL. Replace with the actual file path or URL.
        url = "path/to/your/0050_TW.parquet"
        try:
            df = pd.read_parquet(url)
            print(df)
            stock_info = df.loc[df['StockCode'] == stock_code, "Close"]
            if not stock_info.empty:
                response = f"Stock Code: {stock_code}, Close Price: {stock_info.values[0]}"
            else:
                response = "Stock code not found."
        except Exception as e:
            response = f"An error occurred: {e}"
        return render_template_string(render_form(form) + f"<br>{response}")
    else:
        # Add debug information to check why the form is not validating
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")
    
    return render_template_string(render_form(form))

def render_form(form):
    # 生成並返回表單的純文本表示
    form_html = f"""
    <form method="POST">
    Get Stock Information:<br>
    Stock Code: {form.stock_code.label} {form.stock_code()}<br>
    {form.submit()}
    </form>
    """
    return form_html

if __name__ == '__main__':
    app.run(debug=True)
