import pandas as pd
from dateutil.relativedelta import relativedelta

import plutuslib.data_utils as du
import plutuslib.general_utils as gu

from subsystems.LBMOM.subsys import Lbmom

# Save code
# df, instruments = du.get_ftx_df()
# df = du.extend_dataframe(traded=instruments, df=df)
# gu.save_file('./data/data.obj', (df, instruments))

# # Load code
df, instruments = gu.load_file('./data/data.obj')

VOL_TARGET = 0.20
print(df.index[-1])

# strat = Lbmom(
#     instruments_config = "./subsystems/LBMOM/config.yml"
#     historical_df = df,

# )