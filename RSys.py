import graphlab
import pandas as pd
import graphlab.aggregate as agg

# pass in column names for each CSV and read them using pandas.
# Column names available in the readme file

#Reading users file:
users = graphlab.SFrame.read_csv('user_profile_no_null.csv', sep='\t')


#Reading items file:
items = graphlab.SFrame.read_csv('item_profile_no_null.csv', sep='\t')
items['title'] = items['title'].apply(lambda x: x.split())
items['tags'] = items['tags'].apply(lambda x: x.split())

item = graphlab.SFrame.read_csv('DataSet/item_profile.csv', sep='\t',)
itemfiltered = item.filter_by(0, 'active_during_test', exclude=True)

itemfilt = itemfiltered.remove_columns(['title', 'career_level', 'discipline_id', 'industry_id', 'country', 'region',
                                        'latitude', 'longitude', 'employment', 'tags', 'created_at', 'active_during_test'])

#Reading the target file:
filtered = graphlab.SFrame.read_csv('DataSet/target_users.csv')

#Reading the interactions file:
ratings_base = pd.read_csv('DataSet/interactions.csv', sep='\t')

#Reading the interactions file for the recommendation to remove
interactionsToRemove = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')
interactionsToRemove.remove_columns(['interaction_type', 'created_at'])

#Since we be using GraphLab, lets convert these in SFrames
#We can use this data for training
ratings_base_SFrame = graphlab.SFrame.read_csv('DataSet/interactions.csv', sep='\t')

knn_sim_items_model = graphlab.item_content_recommender.create(items, item_id='item_id')
knn_sim_items_model.save(location='Models')
knn_sim_items = knn_sim_items_model.get_similar_items()

item_sim_model = graphlab.item_similarity_recommender.create(ratings_base_SFrame, item_id='item_id', user_id='user_id',
                                                             nearest_items=knn_sim_items)
recomm = item_sim_model.recommend(users=filtered, items=itemfilt, k=5, exclude=interactionsToRemove, random_seed=911)

groupedResult = recomm \
    .groupby(key_columns='user_id', operations={'recommended_items': agg.CONCAT('item_id')}) \
    .sort('user_id')

def split_string(x):
    x = map(str, x)
    return ' '.join(x)

groupedResult['recommended_items'] = groupedResult['recommended_items'].apply(split_string)

groupedResult.export_csv('Results/SimilarityWithKNNSimilarItems.csv')