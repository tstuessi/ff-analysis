# Utilities
from sklearn.base import TransformerMixin
from sklearn.preprocessing import LabelEncoder

class MultiColumnLabelEncoder(TransformerMixin):
    def __init__(self, columns="all"):
        self.columns = columns
        self.encoder_dict = {}

    def fit(self, X, y=None):
        if self.columns == "all":
            self.columns = X.columns
        for column in self.columns:
            self.encoder_dict[column] = LabelEncoder()
            self.encoder_dict[column].fit(X[column])
        return self

    def transform(self, X):
        X_out = X.copy()
        for column in self.columns:
            X_out[column] = self.encoder_dict[column].transform(X[column])
        return X_out.values
