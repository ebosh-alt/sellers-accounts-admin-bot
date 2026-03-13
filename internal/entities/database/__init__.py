from internal.entities.database.accounts import Account, Accounts
from internal.entities.database.accounts_data import AccountData, AccountsData
from internal.entities.database.categories import Category, Categories
from internal.entities.database.chats import Chat, Chats
from internal.entities.database.deals import Deal, Deals
from internal.entities.database.sellers import Seller, Sellers
from internal.entities.database.shops import Shop, Shops
from internal.entities.database.users import User, Users

users: Users = Users()
sellers: Sellers = Sellers()
deals: Deals = Deals()
accounts: Accounts = Accounts()
accounts_data: AccountsData = AccountsData()
chats: Chats = Chats()
shops: Shops = Shops()
categories: Categories = Categories()
# acceptable_account_categories: AcceptableAccountCategories = AcceptableAccountCategories()

__all__ = ("Deal", "deals",
           "Chat", "chats",
           "User", "users",
           "Seller", "sellers",
           "Account", "accounts",
           "AccountData", "accounts_data",
           "Category", "categories",
           "Shop", "shops",
           # "AcceptableAccountCategory", "acceptable_account_categories",
           )
