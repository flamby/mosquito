from abc import ABC, abstractmethod
from .enums import TradeState as ts


class Base(ABC):
    """
    Base class for all strategies
    """

    action_request = ts.none
    actions = []

    def __init__(self, args, verbosity=2):
        super(Base, self).__init__()
        self.verbosity = verbosity
        self.args = args
        self.min_history_ticks = 5
        self.group_by_field = 'pair'

    def get_min_history_ticks(self):
        """
        Returns min_history_ticks
        """
        return self.min_history_ticks

    @staticmethod
    def get_dataset_count(df, group_by_field):
        """
        Returns count of dataset and pairs_count (group by provided string)
        """
        pairs_group = df.groupby([group_by_field])
        # cnt = pairs_group.count()
        pairs_count = len(pairs_group.groups.keys())
        dataset_cnt = pairs_group.size().iloc[0]
        return dataset_cnt, pairs_count

    @abstractmethod
    def calculate(self, data, wallet):
        pass

