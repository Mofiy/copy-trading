import threading
import time

from binance import Binance
import dearpygui.dearpygui as dpg

orders = []
COIN = 'USDT'
PAIR = 'BTCUSDT'
ORDER_HEADER = ['orderId',
                'symbol',
                'status',
                'avgPrice',
                'cumQuote',
                'side',
                'time']

client = Binance('binance_keys.txt')

dpg.create_context()
dpg.create_viewport(title='Copy trading')
dpg.setup_dearpygui()

user_data = client.GetAccountData()
for assets in user_data["assets"]:
    if assets['asset'] == COIN:
        with dpg.window(label=assets['asset'], no_close=True):
            for item in assets:
                if item == 'asset':
                    dpg.add_checkbox(default_value=True, tag="checkbox_" + assets[item])
                else:
                    if item == 'marginAvailable':
                        break
                    dpg.add_text(item)
                    dpg.add_input_text(source=assets[item], tag=assets['asset'] + '_' + item)


with dpg.window(label='table orders', no_close=True) as orders:
    orders = client.GetAllOrderInfo(symbol=PAIR)
    with dpg.table():
        for _ in ORDER_HEADER:
            dpg.add_table_column(width_stretch=True)
        for order in orders:
            dpg.add_table_row()
            with dpg.table_row():
                for item in order:
                    if item in ORDER_HEADER:
                        dpg.add_text(f"{order[item]}")


def background_theme():
    account_info_updater_thread = threading.Thread(name="account_info_updater", target=account_info_updater, args=(),
                                                   daemon=True)
    account_info_updater_thread.start()


def account_info_updater():
    # Function loops the background theme
    while True:
        user_data = client.GetAccountData()
        for assets in user_data["assets"]:
            if assets['asset'] == COIN:
                if dpg.get_value(item="checkbox_" + assets['asset']) == True:
                    for item in assets:
                        if item == 'marginAvailable': break
                        if item != 'asset':
                            dpg.set_value(item=assets['asset'] + '_' + item, value=assets[item])
        time.sleep(1)


background_theme()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
