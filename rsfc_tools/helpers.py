import numpy as np
import os,subprocess

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

# This requires having connectome workbench installed
# You may need to edit the path_to_wb variable with your own local path to the workbench installation
def save_nii(array, output_name, output_dir_path, wb_required_template_path, purge = True):
    
    path_to_wb = '/Applications/workbench/bin_macosx64/wb_command'
    
    '''
    Save a numpy array as a .nii file, utilizing workbench as an intermediary.
    Arguments:
        array: the numpy array to save
        output_name: the name to use for the output file
        output_dir_path: the directory path to save the output file in
        wb_required_template_path: a dtseries of the same dimension used as a template to write over
        purge: if True, delete the intermediate text file after creating the .nii file
    '''
    if not os.path.isdir(output_dir_path):
        raise Exception(f"The output folder {output_dir_path} does not exist")
    template_base = os.path.basename(wb_required_template_path)
    end = template_base.find('.')
    file_end = template_base[end:]
    out_path = os.path.join(output_dir_path, output_name)
    outnamecifti = out_path+file_end
    if os.path.isfile(outnamecifti):
        print('-WARNING: Overwriting')
    np.savetxt(out_path, array)
    wb_comm = ' '.join([path_to_wb, '-cifti-convert -from-text', out_path, wb_required_template_path, outnamecifti])
    subprocess.call(wb_comm, shell=True)
    if purge:
        os.remove(out_path)        
