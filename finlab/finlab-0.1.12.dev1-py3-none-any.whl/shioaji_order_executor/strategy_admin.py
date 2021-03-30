from shioaji_order_executor.utils import ShioajiApi, update_df, logger, get_snapshot
from shioaji_order_executor.models import StrategyPost
from shioaji_order_executor.account_admin import AccountAdmin
import pandas as pd


class StrategyAdmin(ShioajiApi):
    def update_strategy(self, strategy_list: list):
        """Update strategy settings,total size shold be smaller than net asset.
        Args:
          strategy_list(list): strategy dict in list,ex:
          [{'account': 'shioaji_stock',
            'name': 'self_a_strategy',
            'enable': 1,
            'schedule': '1 19 * * *',
            'size': 150000},
          {'account': 'shioaji_stock',
            'name': 'self_c_strategy',
            'enable': 1,
            'schedule': '2 19 * * *',
            'size': 220000}]
        Returns:
            dataframe:new strategy data.
        """
        # old strategy settings.If you set strategy initially,make df_old be None.
        try:
            df_old = pd.read_pickle(self.strategy_pkl_path)
        except Exception as e:
            logger.error(e)
            df_old = None
        new_post = {'data': strategy_list}
        df = update_df(StrategyPost, new_post, df_old)

        # check total size
        total_size = df['size'].sum()
        account = AccountAdmin(self.api)
        total_balance = account.get_total_balance()
        if total_size > total_balance:
            logger.error(f'total_size:{total_size}>total_balance:{total_balance}, please reset strategy size.')
            return None
        df.to_pickle(self.strategy_pkl_path)
        logger.info('success update')
        return df

    def check_strategy_enable(self, strategy: str):
        """Check if the strategy is on.
        Args:
          strategy(str): strategy name
        Returns:
            bool.
        """
        df = pd.read_pickle(self.strategy_pkl_path)
        df = df.set_index(['name'])
        result = False
        if strategy in df.index:
            if df.loc[strategy, 'enable'] == 1:
                result = True
        return result

    def get_strategy_position(self, strategy: str):
        """Get information about strategy position right now.
        Args:
          strategy(str): strategy name
        Returns:
            dict:{stock_id:quantity},ex:{'2606': 3}
        """
        df = pd.read_pickle(self.orders_pkl_path)
        df = df[df['strategy'] == strategy]
        df['deal_quantity'] = [-num if action == 'Sell' else num for action, num in
                               zip(df['action'], df['deal_quantity'])]
        df = df.groupby(['code'])['deal_quantity'].sum()
        df = df[df > 0]
        df = df.to_dict()
        return df

    def get_strategy_position_snapshot(self, strategy: str):
        """Get information about strategy position snapshot right now.
        Args:
          strategy(str): strategy name
        Returns:
            dict:{stock_id:price},ex:{'2606': 36}
        """
        df = self.get_strategy_position(strategy)
        stock_list = list(df.keys())
        df = get_snapshot(self.api, stock_list)
        return df

    def get_strategy_accounting_info(self, strategy: str):
        """Get information about strategy accounting info right now.
        Args:
          strategy(str): strategy name
        Returns:
            settlement(int): Get information about net asset value in strategy.
            stock_balance(int): Get information about stock balance in strategy.
            orders_info(dataframe): Get information about orders history in strategy.
        """
        check = self.check_strategy_enable(strategy)
        if check is False:
            return None
        try:
            df = pd.read_pickle(self.orders_pkl_path)
        except Exception as e:
            logger.error(e)
            return None
        df = df[df['strategy'] == strategy]
        data = []
        # balance
        for i in range(len(df['deals'].values)):
            deals_list = df['deals'].values[i]
            data.append(sum([i.price * i.quantity for i in deals_list]) * 1000)

        # strategy profit loss
        df['cost'] = data
        df['cost'] = [round(-cost * (1 + 1.425 / 1000)) if action == 'Buy' else round(cost * (1 - (3 + 1.425) / 1000))
                      for action, cost in zip(df['action'], df['cost'])]
        df['quantity'] = [-num if action == 'Sell' else num for action, num in zip(df['action'], df['quantity'])]

        position = self.get_strategy_position(strategy)
        snapshot = self.get_strategy_position_snapshot(strategy)
        # Total after-sales value
        stock_balance = sum(
            [round(position[k] * snapshot[k] * (1 - (3 + 1.425) / 1000) * 1000) for k, v in position.items()])

        df_old = pd.read_pickle(self.strategy_pkl_path)
        df_old = df_old.set_index(['name'])

        settlement = stock_balance + df['cost'].sum() + df_old.loc[strategy, 'size']
        orders_info = df.copy()
        return settlement, stock_balance, orders_info

    def get_all_strategy_balance(self):
        """Get information about all strategys balance value.
        Returns:
            dataframe
        """
        strategy_df = pd.read_pickle(self.strategy_pkl_path)
        strategy_list = list(strategy_df['name'])
        balance = [self.get_strategy_accounting_info(s)[1] for s in strategy_list]
        df = pd.DataFrame({'name': strategy_list, 'balance': balance})

        account_admin = AccountAdmin(self.api)
        available_balance = account_admin.get_account_settlement()['available_balance'].values[0]
        df = df.append({'name': 'cash', 'balance': available_balance}, ignore_index=True)
        return df
