from os import path
import pandas as pd
import matplotlib.pyplot as plt


from spider.spider import run

# start crawling n pages
run(100)

base_dir = path.dirname(path.abspath(__file__))
target_file_path = path.join(base_dir, 'spider', '4pda_dump.csv')

df = pd.read_csv(target_file_path, parse_dates=True, index_col='date_published')
max_time_delta = df.index.max() - df.index.min()

try:
    daily_post_frequency = len(df.index) // max_time_delta.days
except ZeroDivisionError:
    daily_post_frequency = len(df.index)

print 'Daily post frequency: ', daily_post_frequency
# plotting

# grouped data
month_grouped_data = df['title'].groupby(pd.TimeGrouper(freq='M'))
date_grouped_data = df['title'].groupby(pd.TimeGrouper(freq='D'))

# x//30 is wrong if we need precise data but as approximately value it's ok
month_grouped_data.count().apply(lambda x: x//30).plot(color='g', label='approx average based on month')
date_grouped_data.count().plot(color='r', alpha=0.5, label='daily posts')

plt.show()
