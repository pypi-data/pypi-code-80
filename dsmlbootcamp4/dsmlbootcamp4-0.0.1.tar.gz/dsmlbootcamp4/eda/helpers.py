from mlxtend.frequent_patterns import apriori, association_rules


def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### Tail #####################")
    print(dataframe.tail(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def crm_data_prep(dataframe):
    dataframe.dropna(axis=0, inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    return dataframe


def create_invoice_product_df(dataframe):
    return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
        applymap(lambda x: 1 if x > 0 else 0)

def create_rules(dataframe, country=False, head=5):
    if country:
        dataframe = dataframe[dataframe['Country'] == country]
        dataframe = create_invoice_product_df(dataframe)
        frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True,low_memory=True)
        rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
        print(rules.sort_values("lift", ascending=False).head(head))
    else:
        dataframe = create_invoice_product_df(dataframe)
        frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True, low_memory=True)
        rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
        print(rules.sort_values("lift", ascending=False).head(head))

    return rules

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('/Users/tugcedogan/Desktop/phyton_samples/movie.csv')
    rating = pd.read_csv('/Users/tugcedogan/Desktop/phyton_samples/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    df['title'] = df.title.str.replace('(\(\d\d\d\d\))', '')
    df['title'] = df['title'].apply(lambda x: x.strip())
    a = pd.DataFrame(df["title"].value_counts())
    rare_movies = a[a["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df



def item_based_recommender(movie_name):
    # film umd'de yoksa önce ismi barındıran ilk filmi getir.
    # eger o da yoksa filmin isminin ilk iki harfini barındıran ilk filmi getir.
    if movie_name not in user_movie_df:
        # ismi barındıran ilk filmi getir.
        if [col for col in user_movie_df.columns if movie_name.capitalize() in col]:
            new_movie_name = [col for col in user_movie_df.columns if movie_name.capitalize() in col][0]
            movie = user_movie_df[new_movie_name]
            print(F"{movie_name}'i barındıran ilk  film: {new_movie_name}\n")
            print(F"{new_movie_name} için öneriler geliyor...\n")
            return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)
        # filmin ilk 2 harfini barındıran ilk filmi getir.
        else:
            new_movie_name = [col for col in user_movie_df.columns if col.startswith(movie_name.capitalize()[0:2])][0]
            movie = user_movie_df[new_movie_name]
            print(F"{movie_name}'nin ilk 2 harfini barındıran ilk film: {new_movie_name}\n")
            print(F"{new_movie_name} için öneriler geliyor...\n")
            return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)
    else:
        print(F"{movie_name} için öneriler geliyor...\n")
        movie = user_movie_df[movie_name]
        return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)






