from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class SignUpForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    username = StringField("Tên người dùng", validators=[DataRequired(), length(min=2)])
    password1 = PasswordField("Tạo mật khẩu", validators=[DataRequired(), length(min=6)])
    password2 = PasswordField("Nhập lại mật khẩu", validators=[DataRequired(), length(min=6)])
    submit = SubmitField("Đăng kí")

class LoginForm(FlaskForm):
    email = EmailField("Nhập email", validators=[DataRequired()])
    password = PasswordField('Nhập mật khẩu', validators=[DataRequired()])
    submit = SubmitField("Đăng nhập")

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Nhập mật khẩu hiện tại', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('Nhập mật khẩu mới', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Nhập lại mật khẩu', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Đổi mật khẩu')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Tên sản phẩm', validators=[DataRequired()])
    current_price = FloatField('Giá hiện tại', validators=[DataRequired()])
    previous_price = FloatField('Giá trước', validators=[DataRequired()])
    in_stock = IntegerField('Số lượng trong kho', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Ảnh sản phẩm', validators=[DataRequired()])
    flash_sale = BooleanField('Sale')

    add_product = SubmitField('Thêm sản phẩm')
    update_product = SubmitField('Cập nhật')

class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Chưa xử lý', 'Chưa xử lý'), ('Đã duyệt đơn', 'Đã duyệt đơn'),
                                                        ('Out for delivery', 'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Đã huỷ', 'Đã huỷ')])

    update = SubmitField('Cập nhật trạng thái')


