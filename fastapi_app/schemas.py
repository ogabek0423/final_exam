from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    password: str
    email: str
    is_staff: bool = False
    is_active: bool = True
    is_superuser: bool = False


class RegisterUser(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    date_joined: Optional[datetime]


class LoginUser(BaseModel):
    username: str
    password: str


class TelegramUserBase(BaseModel):
    username: str
    fullname: str
    chat_id: int
    id: int



class CategoryBase(BaseModel):
    name: str
    id: int
    slug: str



class ProductBase(BaseModel):
    name: str
    image: str
    description: str
    category_id: int
    price: float
    count: int
    endurance: int
    id: int
    slug: str




class CouponBase(BaseModel):
    code: str
    value: float
    id: int

class PaymentBase(BaseModel):
    user_id: int
    product_list: str
    amount: float
    pay_type: str
    coupon_id: Optional[int] = None
    id: int



class UserInfoBase(BaseModel):
    user_id: int
    your_photo: str
    city: str
    street: str
    home_number: str
    user_number: str
    id: int



class StaffInfoBase(BaseModel):
    user_id: int
    photo: str
    work_time: str
    phone: str
    experience: str
    id: int
    slug: str


class BlogBase(BaseModel):
    text: str
    user_id: int
    id: int
    created_time: str
    slug: str


class ProblemBase(BaseModel):
    problem_text: str
    user_email: str
    id: int
    slug: str


class JwtModel(BaseModel):
    authjwt_secret_key: str = '192ba1860ccd8dcb1577983848289f3792e3c896fd7df9277a773d39d2c9e291'
    # authjwt_access_token_expired: timedelta = timedelta(minutes=3)
    # authjwt_refresh_token_expired: timedelta = timedelta(minutes=3600)

