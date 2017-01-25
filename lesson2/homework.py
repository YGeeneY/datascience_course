import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as tkr


sns.set(style="ticks", color_codes=True)

df = pd.read_csv("../lesson1/spider/4pda_dump.csv", parse_dates=True, index_col='date_published')

# looks odd actually
target = df.groupby(pd.TimeGrouper(freq='D'))['title'].count().rename('count').reset_index()
target['extra_index'] = target.index
sns.lmplot(x='extra_index', y='count', data=target)
sns.plt.savefig('cumsum.png')


# extra research
df = df.reset_index()
df['date_published'] = pd.to_datetime(df.date_published)
df['weekday'] = df.date_published.apply(lambda x: x.weekday())
df['half_hours_from_midnight'] = df.date_published.apply(lambda x: (x.hour * 60 + x.minute)//30)

# grouping data by weeks
# and half hours deltas in a day
weekly_grouped_data = df.groupby(['weekday'])
minutes_grouped_data = df.groupby(['half_hours_from_midnight'])

# weekly aggregation
weekly_post_count = weekly_grouped_data['title'].count().rename('articles_count')
weekly_comments_sum = weekly_grouped_data['comments_count'].sum()

# daily aggregation
# dtd stand for during the day
dtd_post_count = minutes_grouped_data['title'].count().rename('articles_count')
dtd_comments_sum = minutes_grouped_data['comments_count'].sum()
dtd_comment_and_articles = pd.concat([dtd_post_count, dtd_comments_sum], axis=1)

# some concerns about violating DRY
# plot showing amount of comment/articles during the day
f, (ax1, ax2) = plt.subplots(2, sharex='all')
sns.regplot(x='half_hours_from_midnight', y='articles_count', data=dtd_post_count.reset_index(), ax=ax1)
sns.regplot(x='half_hours_from_midnight', y='comments_count', data=dtd_comments_sum.reset_index(), ax=ax2)
ax2.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, y: '%02d:%02d' % divmod(x * 30, 60)))
sns.plt.title('SPREAD DURING THE DAY')
sns.plt.savefig('comment_articles_daily.png')

# plot that showing amount of comment/articles during the week
f, (ax1, ax2) = plt.subplots(2, sharex='all')
sns.regplot(x='weekday', y='articles_count', data=weekly_post_count.reset_index(), ax=ax1)
sns.regplot(x='weekday', y='comments_count', data=weekly_comments_sum.reset_index(), ax=ax2)
day_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue']
ax2.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, y: day_abbr[int(x)]))
sns.plt.title('WEEKLY SPREAD')
sns.plt.savefig('comment_articles_weekly.png')

# plot that showing correlation between articles and comments
sns.regplot(x='articles_count', y='comments_count', data=dtd_comment_and_articles, )
sns.plt.title('ARTICLE COUNT vs COMMENT COUNT')
sns.plt.savefig('article_comment_correlation.png')
