##Employee Termination Analysis
## By: Tom Rice

##Libraries to start with
################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from pycaret.classification import *
##############################

##Descriptive Analysis###
##Brining the Data in##
df = pd.read_csv('Final_ProjectDataReady.csv')
df.apply(pd.to_numeric, errors='ignore') #Applying Numeric designations to all numeric fields

##Descriptive Analysis###
##FUNCTIONS
def df_summary(df):
    print(f'This dataframe has', df.shape[0] , 'rows')
    print(f'This dataframe has', df.shape[1] , 'columns')
    print(df.index)
    print()
    print('--DF HEADERS--')
    print(df.head())
    print()
    print('--DF Summmary--')
    print(df.describe())
    print()
    print(df.info())
    print()
    print('--Unique Values Vs Nulls--')
    print(df.nunique())
    print(df.nunique(dropna=False))

def distribution(df,x,label,title):
    plt.figure()
    df[x] = pd.to_numeric(df[x], errors='coerce')
    plt.xlabel(label)
    plt.ylabel('Freq')
    plt.title(title)
    mean = int(np.mean(df[x]))
    std_dev = int(np.std(df[x]))
    size = int(df[x].shape[0])
    var= np.random.normal(mean,std_dev,size)
    plt.hist(var,mean)
    plt.axvline(var.mean(), color='k', linestyle='dashed', linewidth=1)
    plt.show()

def boxplot(df):
    df.plot(kind = 'box')
    plt.title('Box plots to Search for Outliers')
    plt.show()

def print_score(clf, X_train, y_train, X_test, y_test, train=True):
    if train:
        pred = clf.predict(X_train)
        clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
        print("Training Result:\n================================================")
        print("_______________________________________________")
        print(f"CLASSIFICATION SUMMARY:\n{clf_report}")
        print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
        print("_______________________________________________")
        cm = confusion_matrix(y_train, pred)
        print(f"Confusion Matrix: \n {confusion_matrix(y_train, pred)}\n")
        cm_matrix = pd.DataFrame(data=cm, columns=['Actual Positive:1', 'Actual Negative:0'],
                                 index=['Predict Positive:1', 'Predict Negative:0'])
        plt.title('Confusion Matrix for Training Data')
        sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
        plt.show()
    elif train==False:
        pred = clf.predict(X_test)
        clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
        print("Testing Results:\n================================================")
        print(f"CLASSIFICATION SUMMARY:\n{clf_report}")
        print("_______________________________________________")
        print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
        print("_______________________________________________")
        cm = confusion_matrix(y_test, pred)
        print(f"Confusion Matrix: \n {confusion_matrix(y_test, pred)}\n")
        cm_matrix = pd.DataFrame(data=cm, columns=['Actual Positive:1', 'Actual Negative:0'],
                                 index=['Predict Positive:1', 'Predict Negative:0'])
        plt.title('Confusion Matrix for Testing Data')
        sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
        plt.show()

df_summary(df)
terms = df.loc[df['EMPL_STATUS'] != 1]
terms.sort_values(['AGE'], inplace=True) ## Sort the column
print(terms.shape[0])

##Looking at a Certain Position
# df = df.loc[df['POS_CAT'] == 1]

#Checking the Binary Values for Balance
plt.subplot(1,2,1)
plt.title('Distribution of Employment Status')
plt.xlabel('Employment Status')
plt.ylabel('Employee Count')
df['EMPL_STATUS'].value_counts().plot(kind='bar',color ='Green')
plt.subplot(1,2,2)
plt.title('Distribution of Employment Position Type')
plt.xlabel('Position Type')
plt.ylabel('Employee Count')
df['HCS_POS_TYPE'].value_counts().plot(kind='bar', color ='blue')
plt.show()

# #Checking the Balance of Categorial Values
plt.title('HCS Employee Position Distribution')
plt.xlabel('Position Type')
plt.ylabel('Employee Count')
df['HCS_POS_POSITION'].value_counts().plot(kind='bar',color ='red')
plt.show()

plt.subplot(1,2,1)
plt.title('HCS Active Employee Position Distribution')
plt.xlabel('Position Type Category')
plt.ylabel('Employee Count')
active = df.loc[df['EMPL_STATUS'] == 1]
active['POS_CAT_DESCR'].value_counts().plot(kind='bar',color ='orange',label = 'Active Employees')

plt.subplot(1,2,2)
plt.title('HCS Terminated Employee Position Distribution')
plt.xlabel('Position Type Category')
plt.ylabel('Employee Count')
terms['POS_CAT_DESCR'].value_counts().plot(kind='bar',color ='red',label = 'Terminated Employees')
plt.show()

plt.title('HCS Employee Reason for Leaving')
plt.xlabel('Reason for Leaving')
plt.ylabel('Employee Count')
remove_active = df.loc[df['ACTION_REASON'] != 1]
remove_active['REASON_LEAVE'].value_counts().plot(kind='bar',color ='orange')
plt.show()

##Looking to See how the Data is distirubted
distribution(df,'AGE','Employee Age','Distribution of Employee Age')
distribution(df,'YOS','Years of Service','Distribution of Employee Years of Service')
distribution(df,'STEP','STEP','Distribution of Employee STEP')
distribution(df,'DAILY_RT','Daily Salary','Distribution of Employee Daily Salary')

boxplot(df['ANNUAL_RT'])
boxplot(df['AGE'])

##Pair plot to Look for Patterns for Trends##
# df_pair = df.reindex(columns=['POS_CAT','LOCATION','YOS','AGE','GRADE','STEP','ANNUAL_RT','DAILY_RT','EMPL_STATUS'])
# sns.pairplot(df_pair, hue='EMPL_STATUS')
# plt.plot()

##Looking for Trends From Terminated Employees
plt.title('Distribution of Terminated Employees by Age')
ax = sns.histplot(data=terms['AGE'], bins=20, stat='density', alpha= 1, kde=True,
                  edgecolor='white', linewidth=0.5,
                  line_kws=dict(color='red', alpha=0.5, linewidth=1.5, label='KDE'))
ax.get_lines()[0].set_color('red')
plt.show()


plt.title('Distribution of Terminated Employees by Years of Service')
ax = sns.histplot(data=terms['YOS'], bins=20, stat='density', alpha= 1, kde=True,
                  edgecolor='white', linewidth=0.5,
                  line_kws=dict(color='red', alpha=0.5, linewidth=1.5, label='KDE'))
ax.get_lines()[0].set_color('red')
plt.show()

plt.title('Distribution of Terminated Employees by Annual Salary')
ax = sns.histplot(data=terms['ANNUAL_RT'], bins=20, stat='density', alpha= 1, kde=True,
                  edgecolor='white', linewidth=0.5,
                  line_kws=dict(color='red', alpha=0.5, linewidth=1.5, label='KDE'))
ax.get_lines()[0].set_color('red')
plt.show()

##########Diagnostic Analyiss####################
df_corr = df.reindex(columns=['POS_CAT','LOCATION','YOS','AGE','GRADE','STEP','ANNUAL_RT','DAILY_RT','EMPL_STATUS'])
plt.figure(figsize=(10, 7))
plt.title('Feature Correlations')
plt.ylabel('Loss')
sns.heatmap(df_corr.corr(), annot=True)
plt.show()

# ######FEATURE SIGNIFICANCE
Features = df.drop(['TERMINATION_DT','REASON_LEAVE','ACTION_REASON'],axis = 1)
pycaret_setup = setup(data = Features, target = 'EMPL_STATUS', session_id=123)
logistic_model = create_model('lr')
rf_model = create_model('rf')
plot_model(logistic_model, plot='feature')
plot_model(rf_model, plot='feature')

######################Predictive Analytics########################
#SETTING UP THE ANALYSIS
X = df_corr.drop(['EMPL_STATUS'],axis = 1)  #Features chosen from our Descirptive Analysis
y = df['EMPL_STATUS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=15)

num_columns = ['POS_CAT','LOCATION','YOS','AGE','GRADE','STEP','ANNUAL_RT','DAILY_RT']

scale = make_column_transformer(
    (MinMaxScaler(), num_columns),
    (StandardScaler(), num_columns),
    remainder='passthrough'
)
# X_train = scale.fit_transform(X_train)
# X_test = scale.transform(X_test)

##LOGISTIC REGRESSION##
print('Running Logistic Regression')
lr_clf = LogisticRegression(solver='liblinear')
lr_clf.fit(X_train, y_train)


lr_output = pd.concat([X_test.reset_index(drop='True'),y_test.reset_index(drop='True')],axis=1)
lr_y_pred = lr_clf.predict(X_test)
lr_output['y_pred'] = lr_y_pred.tolist()
lr_output.to_csv('lr_test_output.csv')
# lr_x = X_test.copy()
# lr_y = y_test.copy()
# lr_y_pred = lr_clf.predict(X_test)
# lr_output['x_variables'] = lr_x.tolist()
# lr_output['y_true'] = lr_y.tolist()
# lr_output['y_pred'] = lr_y_pred.tolist()
# lr_output.to_csv('lr_test_output.csv')

print('-----------------------------')
print('Results Logistic Regression With Training Data')
print_score(lr_clf, X_train, y_train, X_test, y_test, train=True)
print('-----------------------------')
print('Results Logistic Regression With Testing Data')
print_score(lr_clf, X_train, y_train, X_test, y_test, train=False)

##Random Forest Classification##
print('Running Random Forest Classifer')
print('-----------------------------')
rf_clf = RandomForestClassifier(n_estimators=1000)
rf_clf.fit(X_train, y_train)
rf_output = pd.concat([X_test.reset_index(drop='True'),y_test.reset_index(drop='True')],axis=1)
rf_y_pred = rf_clf.predict(X_test)
rf_output['y_pred'] = rf_y_pred.tolist()
rf_output.to_csv('rf_test_output.csv')  #To Review the Predictions

# rf_x = X_test.copy()
# rf_y = y_test.copy()
# rf_y_pred = rf_clf.predict(X_test)
# rf_output['x_variables'] = rf_x.tolist()
# rf_output['y_true'] = rf_y.tolist()
# rf_output['y_pred'] = rf_y_pred.tolist()
# rf_output.to_csv('rf_test_output.csv')

print('-----------------------------')
print('Results Random Forest Classifer with Training Data')
print_score(rf_clf, X_train, y_train, X_test, y_test, train=True)
print('-----------------------------')
print('Results Random Forest Classifer with Testing Data')
print_score(rf_clf, X_train, y_train, X_test, y_test, train=False)


### Predictive Analytics####
### Building a Neural Network##

##From our X features in the Diagnostic Analyticis
X1_train, X1_test, y1_train, y1_test = train_test_split(X,y,stratify=y, test_size=0.1, random_state=15)
X1_train = scale.fit_transform(X1_train)
X1_test = scale.transform(X1_test)

input_shape = [X1_train.shape[1]]

model = keras.Sequential([
    layers.BatchNormalization(input_shape=input_shape),
    layers.Dense(32,activation='relu'),
    layers.Dense(32,activation='relu'),
    layers.Dense(1,activation='sigmoid')])

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['binary_accuracy'])

early_stopping = keras.callbacks.EarlyStopping(
    patience=5,
    min_delta=0.001,
    restore_best_weights=True,
)
history = model.fit(
    X1_train, y1_train,
    batch_size=30,
    epochs=50,
    validation_split=0.1,
    callbacks=[early_stopping],
)

history_df = pd.DataFrame(history.history)

# You can change this to get a different view depending on when you see desired learning loss at an epoch.
plt.plot(history_df['loss'], label = 'Training Loss')
plt.plot(history_df['val_loss'], label = 'Validation Loss')
plt.title('Cross-entropy Training and Validation Loss')
plt.legend(loc="upper right")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.xticks(range(0, 40, 5))
plt.show()
#
plt.plot(history_df['binary_accuracy'], label = 'Training Accuracy')
plt.plot(history_df['val_binary_accuracy'], label = 'Validation Accuracy')
plt.title('Cross-entropy Training and Validation Accuracy')
plt.xlabel('Number of Epochs')
plt.legend(loc="upper left")
plt.ylabel('Accuracy')
plt.xticks(range(0, 35, 5))
plt.show()




