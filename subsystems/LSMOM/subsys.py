"""
Implement API for long biased momentum strategy
1. Function to get data and indicators SPECIFIC to strategy
2. Function to run backtest and get positions
"""

class Lsmom:

    def __init__(self, instruments_config, historical_df, simulation_start):
        self.pairs = [(15, 99), (13, 50), (10, 24), (41, 78), (10, 40), (21, 87), (13, 66), (42, 99), (83, 93), (11, 48), (31, 57), (51, 53), (90, 91), (11, 66), (36, 72), (10, 12), (64, 83), (39, 63), (20, 31), (44, 53), (30, 35)]

    def extend_dataframe(self, instruments, historical_data):
        pass

    def run_simulation(self, historical_data):
        pass

    def get_subsys_pos(self):
        pass