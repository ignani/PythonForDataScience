"""

"""
import fancyimpute
from sklearn.model_selection import cross_val_score

mice = fancyimpute.MICE(verbose=0)
X_train_fancy_mice = mice.complete(X_train)
scores = cross_val_score(logreg, X_train_fancy_mice, y_train, cv=10)
scores.mean()