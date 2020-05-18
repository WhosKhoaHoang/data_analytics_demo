import pandas as pd
import seaborn as sns


# ==================== Basic functions ==================== #

# How to load data
listings_df = pd.read_csv("AB_NYC_2019.csv")

# Clean data a little bit
columns_to_drop = ["id", "host_name", "last_review"]
listings_df.drop(columns_to_drop, axis="columns", inplace=True)
listings_df.fillna({'reviews_per_month': 0}, inplace=True)

# How to select particular columns and rows
listings_df[['name', 'neighbourhood_group', 'price']] # => DataFrame
listings_df[5:10]

# SQL-filtering-like action
listings_df[listings_df['price'] < 100]



# ==================== Data analysis examples ==================== #

# What are the 10 most reviewed listings?
listings_df.nlargest(10, "number_of_reviews")

# What are the NY neighborhood groups with listings?
listings_df["neighbourhood_group"].unique()

# How many listings per neighborhood group?
# - E.g., How many rows are there for a neighbourhood_group
#   with the value of "Brooklyn", "Manhattan", "Queens"...
# - Use value_counts()!
listings_df["neighbourhood_group"].value_counts()
listings_df["neighbourhood_group"].value_counts().head(10)  # Top 10

# Plotting
# -- With pandas itself --
listings_df["neighbourhood_group"].value_counts().head(10).plot(kind="bar")
# -- With seaborn (sns) --
# - Note that we don't need to say value_counts. sns has methods that
#   wraps all of those preferences/method calls up.
sns.countplot(data=listings_df, x="neighbourhood_group")

# Adjust column order
columns_order = listings_df["neighbourhood_group"].value_counts().index
sns.countplot(data=listings_df, x="neighbourhood_group", order=columns_order)

# Partition bars by room_type
sns.countplot(data=listings_df, x="neighbourhood_group",
              order=columns_order, hue="room_type")

# Distribution plot
sns.distplot(listings_df["price"])

# Let's make the graph more granular by filtering out high prices
affordable_df = listings_df[listings_df["price"] <= 500]
sns.distplot(affordable_df["price"])

# Some heatmap action
affordable_df.plot(
    kind='scatter',
    x='longitude',
    y='latitude',
    c='price',
    cmap='inferno',
    colorbar=True,
    alpha=0.8,
    figsize=(12,8))

# How to add NYC map underneath our heatmap
import urllib
from matplotlib import pyplot as plt
i = urllib.request.urlopen('https://upload.wikimedia.org/wikipedia/commons/e/ec/Neighbourhoods_New_York_City_Map.PNG')
plt.imshow(plt.imread(i), zorder=0, extent=[-74.258, -73.7, 40.49, 40.92])
ax = plt.gca()
affordable_df.plot(
    ax=ax,
    zorder=1,
    kind='scatter',
    x='longitude',
    y='latitude',
    c='price',
    cmap='inferno',
    colorbar=True,
    alpha=0.8,
    figsize=(12,8))
