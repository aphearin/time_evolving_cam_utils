"""
"""
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier


def get_cross_val_score(histories, scale_factor_array,
        z_cut, sm_low, sm_high, training_set_size=2000, random_state=43):
    """
    """
    sm_mask = (histories['stellar_mass'] >= sm_low) & ((histories['stellar_mass'] < sm_high))
    sample = histories[sm_mask]

    df = pd.DataFrame()
    idx_last = np.searchsorted(scale_factor_array, 1./(1 + z_cut))

    for isnap in range(idx_last):
        new_key = 'sfr_' + str(isnap)
        df[new_key] = sample['sfr_mp'][:, isnap]

        new_key = 'sm_mp_' + str(isnap)
        df[new_key] = sample['sm_mp'][:, isnap]

    y = sample['is_quenched'].data

    X_train, X_test, y_train, y_test = train_test_split(df, y,
            test_size=len(y)-training_set_size, random_state=random_state)

    clf = RandomForestClassifier(class_weight='balanced',
            criterion='entropy', n_estimators=50)

    return np.median(cross_val_score(clf, X_train, y_train, cv=3))
