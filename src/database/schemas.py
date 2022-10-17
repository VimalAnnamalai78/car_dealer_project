from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Login(BaseModel):
    dealer_mobile: int
    dealer_password: str


class ResetPassword(BaseModel):
    dealer_password: str
    old_password: str


class FuelVariant(str, Enum):
    petrol = 'petrol'
    diesel = 'diesel'


class GearType(str, Enum):
    manual = 'manual'
    automatic = 'automatic'


class Cars(BaseModel):

    reg_num: str
    model_type: str
    model_color: str
    company_name: str
    model_name: str
    model_year: int
    price: int
    travelled_kms: int
    variant = FuelVariant
    gear_type = GearType
    used_years: int
    engine_in_cc: int
    num_of_seats: int
    num_of_owners: int
    is_available: bool
    description: str
    dealer_id: int


class Dealers(BaseModel):

    dealer_name: str
    dealer_mobile: int
    dealer_password: str
    dealer_address: str
    access_token: Optional[str] = None


class UpdateDealers(BaseModel):

    dealer_name: str
    dealer_mobile: int
    dealer_address: str


class ShowCars(Cars):
    # created_on: Optional[datetime] = None
    # updated_on: Optional[datetime] = None

    class Config():
        orm_mode = True


class ShowDealers(Dealers):

    class Config():
        orm_mode = True




