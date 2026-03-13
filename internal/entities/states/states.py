from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    enter_buyer_wallet = State()
    change_seller_wallet = State()
    cancel_buy = State()
    change_balance = State()
    change_about_shop = State()
    change_photo_shop = State()
    enter_new_acc_type = State()
    enter_acc_type_to_del = State()
