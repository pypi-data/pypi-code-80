from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from shioaji_order_executor.strategy_admin import StrategyAdmin
from shioaji_order_executor.account_admin import AccountAdmin


def stock_asset_dashboard(api):
    # create data
    data = {'date': pd.date_range(end='1/1/2018', periods=81),
            'profit_loss': [10, 5, -3, 2, -5, -4, 7, 6, 8] * 9
            }

    profit_loss_df = pd.DataFrame(data)
    profit_loss_df['cumsum_pl'] = profit_loss_df['profit_loss']
    profit_loss_df['cumsum_rr'] = round(profit_loss_df['cumsum_pl'].cumsum() / 150 * 100, 2)

    data = {'date': pd.date_range(end='1/1/2018', periods=9),
            'strategy_1_return': [1.01, 0.98, 1, 0.96, 1.01, 1.01, 1.025, 1.05, 1.03],
            'strategy_2_return': [0.99, 0.97, 0.98, 1.02, 1.01, 1.03, 1.01, 1.04, 1.07],
            'strategy_3_return': [1.02, 1.05, 1.06, 1.05, 1.07, 1.09, 1.07, 1.08, 1.1],
            'strategy_1_position': [1.01, 0.98, 1, 0.96, 1.01, 1.01, 1.025, 1.05, 1.03],
            'strategy_2_position': [1.2 * i for i in [0.99, 0.97, 0.98, 1.02, 1.01, 1.03, 1.01, 1.04, 1.07]],
            'strategy_3_position': [1.3 * i for i in [1.02, 1.05, 1.06, 1.05, 1.07, 1.09, 1.07, 1.08, 1.1]],
            'cash': [1] * 9
            }

    strategy_df = pd.DataFrame(data)

    account_admin = AccountAdmin(api)
    strategy_admin = StrategyAdmin(api)
    account_settlement = account_admin.get_account_settlement()
    account_transfer = account_admin.get_account_transfer()
    account_positions_cost = account_admin.get_positions_cost()
    realized_profit_loss = account_admin.get_realized_profit_loss('2021-01-03', '2021-03-28')
    all_strategy_balance = strategy_admin.get_all_strategy_balance()

    # plot

    fig = make_subplots(
        rows=9, cols=2,
        specs=[[{"rowspan": 2, "type": "table"}, {"rowspan": 2, "type": "domain"}],
               [None, None],
               [{"type": "table"}, {"rowspan": 2, "type": "domain"}],
               [{"type": "table"}, None],
               [{"rowspan": 2, "colspan": 2, "type": "xy", "secondary_y": True}, None],
               [None, None],
               [{}, {}],
               [{}, {"rowspan": 2, "type": "domain"}],
               [{}, None], ],
        print_grid=True, horizontal_spacing=0.1, vertical_spacing=0.05,
        subplot_titles=('Account Positions:total pnl is ' + str(account_positions_cost['pnl'].sum()),
                        'Asset Net Value:total value is ' + str(account_positions_cost['net_value'].sum()),
                        'Account Settlement',
                        'Asset Cost Value',
                        'Account Transfer',
                        'Stock Account Profit Loss Return Cumsum',
                        'Drawdown',
                        'Realized Profit Loss',
                        'Strayegy Profit Loss Return Cumsum',
                        'Strategy Cost Value',
                        'Strayegy Asset Stack'))

    fig.add_trace(go.Table(
        header=dict(values=account_positions_cost.columns,
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[account_positions_cost[i] for i in account_positions_cost.columns],
                   fill_color='lightcyan',
                   align='left')), row=1, col=1)

    fig.add_trace(
        go.Pie(values=account_positions_cost['net_value'], labels=account_positions_cost['code'], name="asset_ratio",
               textinfo='label+percent'),
        row=1, col=2)

    fig.add_trace(go.Table(
        header=dict(values=account_settlement.columns,
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[account_settlement[i] for i in account_settlement.columns],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left')), row=3, col=1)

    fig.add_trace(
        go.Pie(values=account_positions_cost['cost'], labels=account_positions_cost['code'], name="asset_ratio",
               textinfo='label+percent'),
        row=3, col=2)

    fig.add_trace(go.Table(
        header=dict(values=account_transfer.columns,
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[account_transfer[i] for i in account_transfer.columns],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left')), row=4, col=1)

    fig.add_trace(go.Bar(x=profit_loss_df['date'], y=profit_loss_df['cumsum_pl'].cumsum(), name="cumsum_pl",
                         marker_color="#636EFA"),
                  secondary_y=True, row=5, col=1)

    fig.add_trace(go.Scatter(
        x=profit_loss_df['date'],
        y=profit_loss_df['cumsum_rr'],
        name="cumsum_rr", marker_color="#FFA15A"
    ), secondary_y=False, row=5, col=1)

    fig.add_trace(go.Scatter(
        x=profit_loss_df['date'],
        y=(profit_loss_df['cumsum_rr'] / profit_loss_df['cumsum_rr'].cummax() - 1),
        name="drawdown", marker_color="#FFA15A"
    ), row=7, col=1)

    fig.add_trace(go.Bar(x=realized_profit_loss['date'], y=realized_profit_loss['pnl'], name="realized_pnl",
                         marker_color="#636EFA"),
                  row=7, col=2)

    fig.add_trace(
        go.Scatter(x=realized_profit_loss['date'], y=realized_profit_loss['pnl'].cumsum(), name="cumsum_realized_pnl",
                   marker_color="#FFA15A"),
        row=7, col=2)

    for i in strategy_df.columns:
        if i is not 'date' and 'return' in i:
            fig.add_trace(go.Scatter(x=strategy_df['date'], y=strategy_df[i], name=i), row=8, col=1)

    fig.add_trace(
        go.Pie(values=all_strategy_balance['balance'], labels=all_strategy_balance['name'], name="strategy_balance",
               textinfo='label+percent'),
        row=8, col=2)

    for i in strategy_df.columns:
        if i is not 'date' and 'return' not in i:
            fig.add_trace(go.Bar(x=strategy_df['date'], y=strategy_df[i], name=i), row=9, col=1)

    fig['layout']['yaxis']['title'] = '%'
    fig['layout']['yaxis2']['title'] = '$NTD'
    fig['layout']['yaxis3']['title'] = '%'
    fig['layout']['yaxis4']['title'] = '$NTD'
    fig['layout']['yaxis5']['title'] = '%'
    fig['layout']['yaxis6']['title'] = '$NTD'

    fig.update_layout(width=1600, height=1500, showlegend=True, barmode="relative", title={
        'text': "Shioaji Stock Asset Dashboard",
        'x': 0.5,
        'y': 0.99,
        'xanchor': 'center',
        'yanchor': 'top'}, title_font_size=24, title_font_color="#F58518")
    fig.show()
