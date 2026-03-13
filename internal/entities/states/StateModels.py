from pydantic import BaseModel


class Score(BaseModel):
    user_id: int | None
    amount: float
    guarantor: bool
    is_payment: bool


class Account(BaseModel):
    id_account: int
    score: Score


class ShoppingCart(BaseModel):
    category: str | None = None
    subcategory: str | None = None
    name: str | None = None
    price: float | None = None
    description: str | None = None
    count: int = 1
    guarantor: bool | None = None
    message_id: int | None = None
    deal_id: int | None = None
    account_id: str = None
    tracker_id: str | None = None
    payment: bool | None = False
    ids_accounts_data: list[int] | None = None


class Deal(BaseModel):
    id: int = None
    user_id: int = None
    category: str = None
    subcategory: str = None
    price: int | float = None
    description: str = None
    data: str = None
    name: str = None
    guarant_type: bool = None


class AccountMD(BaseModel):
    category: str = None
    name: str = None
    description: str = None
    price_no: float = None
    price_yes: float = None
    link: str = None
    count: int = 1
