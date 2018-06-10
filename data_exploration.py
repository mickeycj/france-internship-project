import cols
import pandas as pd
import sys
import utils

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# The column names to be reduced/combined.
fname = sys.argv[2]
if fname == 'max_min':
    cols = cols.max_min()
elif fname == 'avg':
    cols = cols.avg()
else:
    print('Invalid file name!')
    exit()

# Reduce different sensors from the same location to the same columns and print the result.
transformed_df = utils.transform(df.copy(deep=True), cols, '{}.*')
# utils.print_data(transformed_df.head(10), 7)

# Find the correlation between the speed of the boat with different sensors.
utils.write_corr(utils.find_corr_of(transformed_df, 'WTP_SelBoatSpd', exclude=['date TU', 'heure TU', 'latitude', 'longitude']), '{}_corr'.format(fname))

# Plot the correlation matrix.
utils.plot_corr(transformed_df, '{}_corr'.format(fname))
