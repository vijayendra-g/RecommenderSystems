import numpy as np
import pandas as pd

#inizialization of the dictionaries and the counters for the mapping process
dict_u = {}
dict_i = {}
count_1 = 0
count_2 = 0

header = ['user_id', 'item_id', 'interaction_type', 'created_at']
ratings_base = pd.read_csv('DataSet/interactionsClean.csv', sep='\t', names=header)
n_users = ratings_base.user_id.unique().shape[0]
n_items = ratings_base.item_id.unique().shape[0]
print 'Number of users = ' + str(n_users) + ' | Number of jobs = ' + str(n_items)

from sklearn import cross_validation as cv
train_data, test_data = cv.train_test_split(ratings_base, test_size=0.25)

#Create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_items), dtype=np.int8)
for line in train_data.itertuples():

#Mapping for the users
    if not dict_u.has_key(line[1]):
        dict_u[line[1]] = count_1
        count_1 = count_1 + 1
#Mapping for the items
    if not dict_i.has_key(line[2]):
        dict_i[line[2]] = count_2
        count_2 = count_2 + 1

    train_data_matrix[dict_u[line[1]], dict_i[line[2]]] = line[3]

test_data_matrix = np.zeros((n_users, n_items), dtype=np.int8)
for line in test_data.itertuples():

    if not dict_u.has_key(line[1]):
        dict_u[line[1]] = count_1
        count_1 = count_1 + 1

    if not dict_i.has_key(line[2]):
        dict_i[line[2]] = count_2
        count_2 = count_2 + 1

    test_data_matrix[dict_u[line[1]], dict_i[line[2]]] = line[3]

from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        #You use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred

item_prediction = predict(train_data_matrix, item_similarity, type='item')
user_prediction = predict(train_data_matrix, user_similarity, type='user')

#-----EVALUATION-----#
from sklearn.metrics import mean_squared_error
from math import sqrt
def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))

print 'User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))
print 'Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix))


#-----SVD Algorithm-----#
import scipy.sparse as sp
from scipy.sparse.linalg import svds

#get SVD components from train matrix. Choose k.
u, s, vt = svds(train_data_matrix, k = 20)
s_diag_matrix=np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
print 'User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix))