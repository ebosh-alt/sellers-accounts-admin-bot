from dataclasses import dataclass

from pydantic import BaseModel


class DataDeals(BaseModel):
    id: int
    category: str
    name: str
    price: float | int
    description: str
    data: str
    date: str
    guarantor: bool

    def len(self):
        return len(
            str(self.id)
            + str(self.category)
            + str(self.name)
            + str(self.price)
            + str(self.description)
            + str(self.data)
            + str(self.date)
            + str(self.guarantor)
        )


class CreatedWallet(BaseModel):
    status: str
    tracker_id: str | None = None
    token_name: str | None = None
    refer: str | None = None
    alter_refer: str | None = None
    description: str | None
    dest_tag: str | None = None
    extra_info: dict | None = None


class ReceivedOrder(BaseModel):
    status: str = None
    description: str = None
    tracker_id: str | None = None
    amount: float | None = None
    payed_amount: float | None = None
    token: str | None = None
    client_transaction_id: str | None = None
    date_create: str | None = None
    date_expire: str | None = None
    amount_delta: float | None = None
    receiver: str | None = None
    hash: str | None = None
    dest_tag: str | None = None
    callback_url: str | None = None
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    fiat_payed_amount: float | None = None
    fiat_underpayemnt_amount: float | None = None
    underpayemnt_amount: float | None = None
    merchant_uuid: str | None = None
    pay_form_url: str | None = None


class CreatedOrder(BaseModel):
    status: str = None
    description: str = None
    tracker_id: str | None = None
    amount: float | None = None
    dest_tag: str | None = None
    receiver: str | None = None
    date_expire: str | None = None


class CreatedMerchant(BaseModel):
    status: str
    description: str


class TransferredMerchantAccountBalance(BaseModel):
    status: str
    description: str | None


class Transaction(BaseModel):
    amount: float
    callback_url: str | None
    client_transaction_id: str
    date_create: str
    date_update: str
    dest_tag: str | None
    extra_info: dict | None
    hash: str
    receiver: str
    merchant_uuid: str
    status: str
    token: str
    token_major_name: str
    tracker_id: str
    transaction_commission: float
    transaction_description: str | None
    type: str
    amount_usd: float
    invoice_amount_usd: float
    course: float


class ReceivedTransaction(BaseModel):
    status: str
    description: str
    transaction: Transaction | None = None


@dataclass
class ApiPoint:
    create_wallet = "https://my.exnode.io/api/transaction/create/in"
    create_invoice = "https://my.exnode.io/api/crypto/invoice/create"
    get_order = "https://my.exnode.io/api/crypto/invoice/get"
    token_fetch = "https://my.exnode.io/user/token/fetch"
    create_order = "https://my.exnode.io/api/crypto/invoice/create"
    create_merchant = "https://my.exnode.io/api/merchant/create"
    transfer_merchant_account_balance = "https://my.exnode.io/api/merchant/transfer/all"
    create_withdrawal = "https://my.exnode.io/api/transaction/create/out"
    get_transaction = "https://my.exnode.io/api/transaction/get"
    token_list = "https://my.exnode.io/user/token/fetch"
    balance = "https://my.exnode.io/api/token/balance"
