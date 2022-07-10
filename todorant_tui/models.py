import datetime as dt
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class Settings(BaseModel):
    first_day_of_week: int = Field(alias="firstDayOfWeek")
    updated_at: dt.datetime = Field(alias="updatedAt")
    language: str


class UserInfo(BaseModel):
    name: str


class State(BaseModel):
    planning: str
    settings: Settings
    user_info: UserInfo = Field(alias="userInfo")


class User(BaseModel):
    _id: str
    name: str
    email: Optional[str]
    facebook_id: Optional[str] = Field(alias="facebookId")
    telegram_id: Optional[str] = Field(alias="telegramId")
    apple_sub_id: Optional[str] = Field(alias="appleSubId")
    token: Optional[int]
    settings: Optional[Dict[Any, Any]]
    timezone: Optional[int]
    telegram_zen: Optional[int] = Field(alias="telegramZen")
    telegram_language: Optional[str] = Field(alias="telegeamLanguage")
    subscription_status: Optional[str] = Field(alias="subscriptionStatus")
    subscription_id: Optional[str] = Field(alias="subscriptionId")
    apple_receipt: Optional[str] = Field(alias="appleReceipt")
    google_receipt: Optional[str] = Field(alias="googleReceipt")
    created_on_apple: Optional[bool] = Field(alias="createdOnApple")


class TodoUser(BaseModel):
    id: str = Field(alias='_id')


class TodoBase(BaseModel):
    id: Optional[str] = Field(alias='_id')
    text: str
    completed: bool
    frog: bool
    frog_fails: int = Field(alias="frogFails")
    skipped: bool
    order: int
    month_and_year: str = Field(alias="monthAndYear")
    date: Optional[str]
    time: Optional[str]
    go_first: Optional[bool] = Field(alias="goFirst")
    encrypted: bool
    created_at: dt.datetime = Field(alias='createdAt')
    updated_at: dt.datetime = Field(alias='updatedAt')
    delegate_accepted: Optional[bool] = Field(alias='delegateAccepted')
    delegator: Optional[str]
    deleted: bool
    repetitive: bool
    user: TodoUser
    client_id: Optional[str] = Field(alias='clientId')

    def get_full_date(self) -> Optional[str]:
        if self.date:
            return f"{self.month_and_year}-{self.date}"
        return None


class TodoCreate(BaseModel):
    text: str
    completed: bool
    frog: bool
    month_and_year: str = Field(
        alias="monthAndYear",
        description='Assigned month and year in the format "2019-01"')
    date: Optional[str] = Field(
        default=None, description='Assigned date in the format "01"')
    time: Optional[str] = Field(
        default=None, description='Exact time in the format "23:01"')

    @validator('month_and_year', pre=True)
    def validate_month_and_year(cls, v: str) -> str:
        month_year = v.split('-')
        if len(month_year) != 2 and all(map(str.isdigit, month_year)):
            raise ValueError('month_and_year must be in format "2019-01"')
        year, month = month_year
        dt.datetime(year=int(year), month=int(month), day=1)
        return v

    @validator('date', pre=True)
    def validate_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) == 1:
            v = '0' + v
        now = dt.datetime.now()
        dt.datetime(year=now.year, month=now.month, day=int(v))
        return v

    @validator('time', pre=True)
    def validate_time(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        hour_minute = v.split(':')
        if len(hour_minute) != 2 and all(map(str.isdigit, hour_minute)):
            raise ValueError('month_and_year must be in format "2019-01"')
        hour, minute = hour_minute
        now = dt.datetime.now()
        dt.datetime(year=now.year, month=now.month, day=now.day,
                    hour=int(hour), minute=int(minute))
        return v


class TodoUpdate(TodoBase):
    id: Optional[str] = Field(alias='_id')
    created_at: dt.datetime = Field(alias='createdAt')
    updated_at: dt.datetime = Field(alias='updatedAt')
    delegate_accepted: Optional[bool] = Field(alias='delegateAccepted')
    delegator: Optional[str]
    deleted: bool
    repetitive: bool
    user: TodoUser
    client_id: Optional[str] = Field(alias='clientId')


class Current(BaseModel):
    todos_count: int = Field(alias='todosCount')
    incomplete_todos_count: int = Field(alias='incompleteTodosCount')
    points: int = 0
    todo: Optional[TodoBase] = None
