import praw
from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

cache_populated = True

sns.set(style='darkgrid', context='talk', palette='Dark2')
headlines = set()

if not cache_populated:
    reddit = praw.Reddit(
        client_id='-tGqarw41cNT3Q',
        client_secret='36xNHqo6F5MWDpfT52IVBmNd1Yg',
        user_agent='tincompafriend'
    )


    for submission in reddit.subreddit('politics').new(limit=None):
        headlines.add(submission.title)
        display.clear_output()
        print(len(headlines))

    with open("headlines.set.cache", "w+") as f:
        for headline in headlines:
            print(headline, file=f)
else:
    with open("headlines.set.cache") as f:
        for line in f:
            headlines.add(line)


sia = SIA()
results = []

for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

pprint(results[:3], width=100)

df = pd.DataFrame.from_records(results)
df.head()

df['label'] = 0
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] > 0.2, 'label'] = -1

df2 = df[['headline', 'label']]
df2.to_csv('reddit_headlines_labels.csv', mode='a', encoding='utf-8', index=False)

print("Positive headlines:\n")
pprint(list(df[df['label'] == 1].headline)[:5], width=200)

print("\nNegative headlines:\n")
pprint(list(df[df['label'] == -1].headline)[:5], width=200)

print(df.label.value_counts())

print(df.label.value_counts(normalize=True) * 100)

fig, ax = plt.subplots(figsize=(8, 8))

counts = df.label.value_counts(normalize=True) * 100

print(counts)
sns.barplot(x=counts.index, y=counts, ax=ax)

ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")

plt.show()