from abc import ABC, abstractmethod
from strategies.enums import TradeState
from termcolor import colored


class Base(ABC):
    """
    Base class for all exchanges
    """

    transaction_fee = 0.0
    pair_delimiter = '_'

    def __init__(self):
        super(Base, self).__init__()
        self.pair_delimiter = '_'

    @abstractmethod
    def return_open_orders(self, currency_pair='all'):
        """
        Returns your open orders
        """
        pass

    def get_pair_delimiter(self):
        """
        Returns exchanges pair delimiter
        """
        return self.pair_delimiter

    def get_transaction_fee(self):
        """
        Returns exchanges transaction fee
        """
        return self.transaction_fee

    @abstractmethod
    def cancel_order(self, order_number):
        """
        Cancels order for given order number
        """
        pass

    @classmethod
    def trade(cls, actions, wallet, trade_mode):
        """
        Apply given actions and returns updated wallet - Base class only simulates buy/sell.
        For exchange the buy/sel logic should be implemented here
        """

        for action in actions:
            print('applying action:', action.action, ', for pair: ', action.pair)
            # TODO: check if we already don't have the same action in process

            # In simulation we are just buying straight currency
        return wallet

    def get_buy_sell_all_amount(self, wallet, action):
        """
        Calculates total amount for ALL assets in wallet
        """
        if action.action == TradeState.none:
            return 0.0

        if action.rate == 0.0:
            print(colored('Got zero rate!. Can not calc. buy_sell_amount for pair: ' + action.pair, 'red'))
            return 0.0

        (symbol_1, symbol_2) = tuple(action.pair.split(self.pair_delimiter))
        amount = 0.0
        if action.action == TradeState.buy and symbol_1 in wallet:
            assets = wallet.get(symbol_1)
            amount = assets / action.rate
        elif action.action == TradeState.sell and symbol_2 in wallet:
            assets = wallet.get(symbol_2)
            amount = assets

        if amount <= 0.0:
            return 0.0

        txn_fee_amount = (self.transaction_fee * amount) / 100.0
        amount -= txn_fee_amount
        return amount
