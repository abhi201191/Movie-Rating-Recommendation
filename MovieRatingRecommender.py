'''
Created on 26-Dec-2015

@author: Abhi

Assignment: Predict movie ratings

Name: Abhishek Singh
Roll: cs1423

Technique used: User Based collaborative filtering and Pearson's correlation similarity is used.
'''

from math import sqrt
from operator import itemgetter

moviesList = {}
movieRating = {}

def loadData():
    movieFile = open("movies.dat", "r")
    for line in movieFile:
        (movieId, movieName, genre) = line.split("::")
        moviesList[movieId] = movieName
    
    ratedFile = open("movie_ratings_incomplete.dat", "r")
    for line in ratedFile:
        (userId, movieId, rating, timestamp) = line.split("::")
        movieRating.setdefault(userId, {})
        movieRating[userId][moviesList[movieId]] = float(rating)
    
def similarity(user1, user2):
    commonRatedMovies = {}
    for movie in movieRating[user1]:
        if movie in movieRating[user2]:
            commonRatedMovies[movie] = 1
    
    noOfcommonRatedMovies = len(commonRatedMovies)
    if noOfcommonRatedMovies == 0:
        return 0
    
    count = len(movieRating[user1])
    meanOfUser1 = sum(movieRating[user1][movie] for movie in movieRating[user1]) / count
    
    count = len(movieRating[user2])
    meanOfUser2 = sum(movieRating[user2][movie] for movie in movieRating[user2]) / count
    
    numer = sum((movieRating[user1][movie] - meanOfUser1) * (movieRating[user2][movie] - meanOfUser2) for movie in commonRatedMovies)
    
    sqrtOfSumOfUser1 = sqrt(sum(pow((movieRating[user1][movie] - meanOfUser1),2) for movie in commonRatedMovies))
    sqrtOfSumOfUser2 = sqrt(sum(pow((movieRating[user2][movie] - meanOfUser2),2) for movie in commonRatedMovies))
    
    denom = sqrtOfSumOfUser1 * sqrtOfSumOfUser2
    
    if denom == 0:
        return 0
    else:
        r = numer/denom
        return r
        
def similarUser(user, noOfSimilarUser, movieId):
    similarUserList = []
    for otherUser in movieRating:
        if otherUser != user:
            if moviesList[movieId] in movieRating[otherUser]:
                similarityValue = similarity(user, otherUser)
                similarUserList.append((otherUser, similarityValue))
        
    similarUserList.sort(key = itemgetter(1))
    similarUserList.reverse()
    return similarUserList[0:noOfSimilarUser]
    
def computePrediction(user, movieId):
    count = len(movieRating[user])
    meanOfUser = sum(movieRating[user][movie] for movie in movieRating[user]) / count
    numerator = 0.0
    denomenator = 0.0
    similarUserList = similarUser(user, 5, movieId)
    
    for (otherUser, similarityValue) in similarUserList:
        count = len(movieRating[otherUser])
        meanOfOtherUser =  sum(movieRating[otherUser][movie] for movie in movieRating[otherUser]) / count
        numerator = numerator + (similarityValue * (movieRating[otherUser][moviesList[movieId]] - meanOfOtherUser))  
        denomenator = denomenator + abs(similarityValue)
        
    if denomenator == 0.0:
        return meanOfUser
    else:
        predictedRating = meanOfUser + (numerator / denomenator)
    
    return predictedRating    
        
def movieRatingPrediction():
    fRead = open("movie_ratings_blanks.dat", 'r')
    fWrite = open("movie_ratings_1423.dat", 'w')
    
    '''for userId in movieRating:
        for movie in moviesList:
            if moviesList[movie] not in movieRating[userId]:
                rating  = computePrediction(userId, movie)
                movieRating[userId][moviesList[movie]] = rating 
            fWrite.write(str(userId) + "::" + str(movie) + "::" + str(movieRating[userId][moviesList[movie]]) + "\n")
    '''
    for line in fRead:
        (userId, movieId, rating, timestamp) = line.split("::")
        rating = computePrediction(userId, movieId)
        fWrite.write(str(userId) + "::" + str(movieId) + "::" + str(rating) + "::" + str(timestamp))
        
loadData()
movieRatingPrediction()