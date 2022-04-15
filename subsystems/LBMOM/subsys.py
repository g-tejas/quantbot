"""
Implement API for long biased momentum strategy
1. Function to get data and indicators SPECIFIC to strategy
2. Function to run backtest and get positions
"""
import yaml
from yaml import Loader
import pandas as pd
import plutuslib.indicators_cal as indicators_cal

class Lbmom:

    def __init__(self, instruments_config, historical_df, simulation_start, vol_target):
        self.pairs = [(15, 99), (13, 50), (10, 24), (41, 78), (10, 40), (21, 87), (13, 66), (42, 99), (83, 93), (11, 48), (31, 57), (51, 53), (90, 91), (11, 66), (36, 72), (10, 12), (64, 83), (39, 63), (20, 31), (44, 53), (30, 35)]
        self.historical_df = historical_df
        self.simulation_start = simulation_start
        self.vol_target = vol_target # we adopt the volatility targetting risk framework

        with open(instruments_config, 'r') as file:
            self.instruments_config = yaml.load(file, Loader=Loader)

        self.sysname = "LBMOM "

    def extend_historicals(self, instruments, historical_data):
        """Generate technical indicators specific to the strategy. Specifically, we will generate moving averages based
        on the pairs generated, an univariate statistical factor as a indicator of regime, and ADX as a proxy for momentum regime
        indicator.
        :param instruments: list containing symbols being traded
        :type instruments: list
        :param historical_data: dataframe containing OHLCV and returns of the instruments
        :type historical_data: pd.Dataframe
        :returns: 
        """
        for inst in instruments:
            historical_data[f"{inst} adx"] = indicators_cal.adx_series(
                high = historical_data[f"{inst} high"],
                low = historical_data[f"{inst} low"],
                close = historical_data[f"{inst} close"],
                n=14
            )
            # iterate through the pairs, calculate the difference between fast and slow MA
            for pair in self.pairs:
                historical_data[f"{inst} ema{str(pair)}"] = indicators_cal.ema_series(historical_data[f"{inst} close"], n=pair[0]) - \
                    indicators_cal.ema_series(historical_data[f"{inst} close"], n=pair[1])
        
        # the historical data has all the information required for backtesting/NOT LIVE
        return historical_data

    def run_simulation(self, historical_data):
        """Runs the strategy-specific backtest on the newly generated indicators
        :param historical_data: dataframe containing OHLCV and returns of the instruments
        :type historical_data: pd.Dataframe
        :returns: dunno yet
        """
        # Init params
        instruments = self.instruments_config['instruments']
        
        # Pre-processing
        historical_data = self.extend_historicals(instruments=instruments, historical_data=historical_data)
        print(historical_data)
        portfolio_df = pd.DataFrame(index=self.historical_df[self.simulation_start:].index).reset_index()
        portfolio_df.loc[0, "capital"] = 10000
        print(portfolio_df)
        # Run simulation

    def get_subsys_pos(self):
        pass