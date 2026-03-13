from .about_shop import about_shop_rt
from .acc_types import acc_types_rt
from .balance import balance_rt
from .deals import deals_rt
from .menu import admin_rt
from .seller_info import seller_info_rt
from .seller_wallet import seller_wallet_rt

admin_routers = (
    admin_rt,
    deals_rt,
    seller_info_rt,
    balance_rt,
    seller_wallet_rt,
    about_shop_rt,
    acc_types_rt,
)
