import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import pickle


df=pd.read_csv('./Training.csv', sep=',')
df = df.loc[(df!=0).any(axis=1)]
df = df.fillna(0)
y = df['category']
X = df.drop(['category'],axis=1)
feature_list = list(X.columns)

# scaler = StandardScaler()
# scaler.fit(X)
# X = scaler.transform(X)
# pca= PCA(0.999)
# pca.fit(X)
# X = pca.transform(X)
# pickle.dump(pca, open("pca.pkl","wb"))

# model = RandomForestClassifier(n_estimators=100)
# model.fit(X, y)

std_pca = make_pipeline(StandardScaler(), PCA(0.99))
X_trans = std_pca.fit_transform(X)

model = RandomForestClassifier(n_estimators=150)
model.fit(X_trans,y)

# model = make_pipeline(StandardScaler(), PCA(0.99), RandomForestClassifier(n_estimators=100))
# model.fit(X, y)

fileP = "./PCA.pkl"
pickle.dump(std_pca, open(fileP, 'wb'))
fileM = "./scriptedModel.sav"
pickle.dump(model, open(fileM, 'wb'))

# file = "./scriptedModel.sav"
# pickle.dump(model, open(file, 'wb'))

#Random Forest
#
# df2 = pd.read_csv("TestData.csv",sep=",")
# df2 = df2.loc[(df != 0).any(axis=1)]
# df2 = df2.drop(['name'],axis=1)
# df2 = df2.fillna(0)
# X_t = df2
# scaler2 = StandardScaler()
# scaler2.fit(X_t)
# X_t = scaler2.transform(X_t)
#
#
# pca_reload = pickle.load(open("pca.pkl",'rb'))
# X_t = pca_reload .transform(X_t)
#
# yhat = model.predict(X_t)
# yhat