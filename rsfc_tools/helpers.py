import numpy as np

def create_corrmat(arr):
    """
    Generate a Fisher-transformed correlation matrix from a time series array.
    
    Parameters
    ----------
    arr : array_like
        2D array with shape (n_parcels, m_frames) where n_parcels is the number of parcels
        (variables) and m_frames is the number of frames (time points).
    Returns
    -------
    corrmat : ndarray
        The Fisher-transformed correlation matrix with the shape as `n x n`, where each
        element corrmat [i, j] represents the Fisher-transformed correlation coefficient
        between parcel i and parcel j. 
    """
    corrmat = np.corrcoef(arr)
    #Apply Fisher-Z Transform
    np.fill_diagonal(corrmat, 0)
    corrmat = np.arctanh(corrmat)
    np.fill_diagonal(corrmat, 1)
    return corrmat
