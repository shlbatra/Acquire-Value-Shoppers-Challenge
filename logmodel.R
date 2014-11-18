
#install.packages('caret')
#install.packages('e1071')
rm(list = ls())
library(ROCR)
library(glmnet)
library(caret)
library('AUC')

#Setting the work directory
setwd('G:\\Marketing_project\\Repear_Buyers\\Datasets\\Sampled Data\\Model')

# Reading test and train data
train = read.csv('train.csv', header = T, sep = ",")
test = read.csv('test.csv', header = T, sep = ",")

Xtrain = as.matrix(train[,-c(1,17,37)]) 
Ytrain = as.matrix(train[,c(17)])
Xtest = as.matrix(test[,-c(1,17,37)]) 
Ytest = as.matrix(test[,c(17)])

#Number of repeat buyers in train and test set
sum(Ytrain)/length(Ytrain)
sum(Ytest)/length(Ytest)

#Creating model data sets
train.data = train[,-c(1,37)]
test.data = test[,-c(1,37)]

#Building the logit model
fit = glm(label~., data = train.data, family = 'binomial')
summary(fit)
head(train.data)
train.data$label[1:10]

#Predicting on train set 
pred.train = predict(fit, type = 'response')
pred.train[1:10]

#Calculating quantiles of predicted probabilities
quantile(pred.train, c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))

#Creating binary predicions using the probabilities
pred = ifelse(pred.train>=0.24,1,0)

#Calculating accuracies
acc = ifelse(pred == Ytrain,1,0)
sum(acc)/length(Ytrain)

#Confusion matrix
confusionMatrix(pred, Ytrain)

#ROC of train data
X = c(0, 1)
Y = c(0, 1)
pred.pred.train = prediction(pred.train, Ytrain)
perf.train.ROC <- performance(pred.pred.train, "tpr", "fpr")
plot(perf.train.ROC, xlab = '1 - Specificity', ylab = 'Sensitivity', main = 'ROC Curve - Train set', lwd = 2)
lines(X, Y, lty = 2, col='blue', lwd = 2)

#AUC for train data
auc.train <- performance(pred.pred.train, 'auc')
auc.value <- as.numeric(auc.train@y.values)

#Lift chart for train data
perf.train.lift <- performance(pred.pred.train,"lift","rpp")
plot(perf.train.lift, main="Lift curve - Train set", colorize=T)

#Prediction on test set
pred.test = predict(fit, newdata = test.data[,-16], type = 'response')

#Calculating quantiles of the test values 
quantile(pred.test, c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))

#Creating binary values of test predictions
pred.test.values = ifelse(pred.test>=0.25,1,0)

#Number of predicted repeat buyers in test set
sum(pred.test.values)

#Calculating accuracies
acc = ifelse(pred.test.values == Ytest,1,0)
sum(acc)/length(Ytest)

#Confusion matrix of test set
confusionMatrix(Ytest, pred.test.values, positive = NULL)

#Calculating AUC
pred.test.auc = prediction(pred.test, test.data[,16])
auc.test <- performance(pred.test.auc, 'auc')
auc.value <- as.numeric(auc.test@y.values)

#Using fewer variables
#Creating train and test sets
train.data = train[,c('label','offer_value', 'has_bought_category_q', 'has_bought_category_a','has_bought_category','total_spend', 'has_bought_category_180')]
test.data = test[,c('label','offer_value', 'has_bought_category_q', 'has_bought_category_a','has_bought_category','total_spend', 'has_bought_category_180')]

#Building the model
fit = glm(label~., data = train.data, family = 'binomial')
summary(fit)

#Predicting using the model
pred.test = predict(fit, newdata = test.data[,-1], type = 'response')

#Calculating quantiles of the test values 
quantile(pred.test, c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))

#Creating binary values of test predictions
pred.test.values = ifelse(pred.test>=0.25,1,0)

#Number of predicted repeat buyers in test set
sum(pred.test.values)

#Calculating accuracies
acc = ifelse(pred.test.values == test.data[,1],1,0)
sum(acc)/length(acc)

#Confusion matrix
confusionMatrix(pred.test.values, test.data[,1])  
  
#Calculating AUC
pred.test.auc = prediction(pred.train, test.data[,1])
auc.test <- performance(pred.test.auc, 'auc')
auc.value <- as.numeric(auc.test@y.values)

#Segmenting customers based on total spend
train.data.low = train.data[which(train.data$total_spend<=120),c(16, 6, 15, 20, 21, 38, 36)]
train.data.med = train.data[which(train.data$total_spend>120 & train.data$total_spend<= 250),c(16, 6, 15, 20, 21, 38, 36)]
train.data.high = train.data[which(train.data$total_spend>250),c(16, 6, 15, 20, 21, 38, 36)]

test.data.low = test.data[which(test.data$total_spend<=120),c(16, 6, 15, 20, 21, 38, 36)]
test.data.med = test.data[which(test.data$total_spend>120 & test.data$total_spend<= 250),c(16, 6, 15, 20, 21, 38, 36)]
test.data.high = test.data[which(test.data$total_spend>250),c(16, 6, 15, 20, 21, 38, 36)]

#Number of repeat buyers in each segment
sum(test.data.low$label)/length(test.data.low$label)
sum(test.data.med$label)/length(test.data.med$label)
sum(test.data.high$label)/length(test.data.high$label)

#Printing number of rows
nrow(train.data.low)
nrow(train.data.med)
nrow(train.data.high)

nrow(test.data.low)
nrow(test.data.med)
nrow(test.data.high)

#Building model on each of the above segments
glm.fit.low = glm(label~., data = train.data.low, family = 'binomial')
glm.fit.med = glm(label~., data = train.data.med, family = 'binomial')
glm.fit.high = glm(label~., data = train.data.high, family = 'binomial')

#Printing the coeff
summary(glm.fit.low)
summary(glm.fit.med)
summary(glm.fit.high)

#Predicting on test set
pred.test.low = predict(glm.fit.low, newdata = test.data.low, type = 'response')
pred.test.med = predict(glm.fit.med, newdata = test.data.med, type = 'response')
pred.test.high = predict(glm.fit.high, newdata = test.data.high, type = 'response')

#Getting quantiles of predictions
quantile(pred.test.low,c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))
quantile(pred.test.med,c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))
quantile(pred.test.high,c(0.25, 0.5, 0.75, 0.8, 0.85, 0.9,1))

#Creating binary values
pred.test.low.values = ifelse(pred.test.low>=0.24,1,0)
pred.test.med.values = ifelse(pred.test.med>=0.28,1,0)
pred.test.high.values = ifelse(pred.test.high>=0.29,1,0)

#Number of predicted repeat buyers in test set
sum(pred.test.low.values)
sum(pred.test.med.values)
sum(pred.test.high.values)

#Calculating accuracies
acc.low = ifelse(pred.test.low.values == test.data.low[,1],1,0)
sum(acc.low)/length(acc.low)

acc.med = ifelse(pred.test.med.values == test.data.med[,1],1,0)
sum(acc.med)/length(acc.med)

acc.high = ifelse(pred.test.high.values == test.data.high[,1],1,0)
sum(acc.high)/length(acc.high)

#Confusion matrix
confusionMatrix(pred.test.low.values, test.data.low[,1])  
length(pred.test.low.values)

confusionMatrix(pred.test.med.values, test.data.med[,1])  
length(pred.test.med.values)

confusionMatrix(pred.test.high.values, test.data.high[,1])  
length(pred.test.low.values)

#Calculating AUC
pred.test.auc.low = prediction(pred.test.low, test.data.low[,1])
auc.test.low <- performance(pred.test.auc.low, 'auc')
auc.value.low <- as.numeric(auc.test.low@y.values)

pred.test.auc.med = prediction(pred.test.med, test.data.med[,1])
auc.test.med <- performance(pred.test.auc.med, 'auc')
auc.value.med <- as.numeric(auc.test.med@y.values)

pred.test.auc.high = prediction(pred.test.high, test.data.high[,1])
auc.test.high <- performance(pred.test.auc.high, 'auc')
auc.value.high <- as.numeric(auc.test.high@y.values)

