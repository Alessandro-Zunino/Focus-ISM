import numpy as np
from scipy.ndimage import fourier_shift, shift
from skimage.registration import phase_cross_correlation

def sigmoid(R, T, S):
    """
    Radially sigmoidal filter
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    R           radial axis
    T           cut-off frequency
    S           sigmoid slope
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    sig         sigmoid, with the same shape of R
    ======
    """
    
    return  1 / (1 + np.exp( (R-T)/S ) )

def Low_pass(img, T, S, pxsize = 1, data = 'real'):
    """
    Low-pass sigmoidal filter
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    img         input image, np.array (Nx x Ny)
    T           cut-off frequency
    S           sigmoid slope
    pxsize      XY pixel size
    data        put 'real' if the image is in the real space, or 'fourier' if
                    img is already the fft of the original image
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    img_filt    filtered image, np.array (Nx x Ny)
    ======
    """
    
    if data == 'real':
        img_fft = np.fft.fftn(img, axes = (0,1) )
        img_fft = np.fft.fftshift(img_fft, axes = (0,1) )
    elif data == 'fourier':
        img_fft = img
    else:
        raise ValueError('data has to be \'real\' or \'fourier\'')
            
    Nx = np.shape(img_fft)[0]
    Ny = np.shape(img_fft)[1]
    cx = int ( ( Nx + np.mod(Nx,2) ) / 2)
    cy = int ( ( Ny + np.mod(Ny,2) ) / 2)
    
    x = ( np.arange(Nx) - cx ) / Nx
    y = ( np.arange(Ny) - cy ) / Ny
    
    X, Y = np.meshgrid(x, y)
    R = np.sqrt( X**2 + Y**2 )
    
    sig = sigmoid(R, T, S)
    
    img_filt = np.einsum( 'ij..., ij -> ij...', img_fft, sig )
    
    if data == 'real':
        img_filt = np.fft.ifftshift(img_filt, axes = (0,1) )
        img_filt = np.fft.ifftn(img_filt, axes = (0,1) )
        img_filt = np.abs(img_filt)
    
    return img_filt

def hann2d( shape ):
    """
    Hann window for a 2D array
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    shape       list containing the shape of the image to be windowed (Nx, Ny)
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    W           window function np.array(Nx x Ny)
    ======
    """
    
    Nx, Ny = shape[0], shape[1]
    
    x = np.arange(Nx)
    y = np.arange(Ny)
    X, Y = np.meshgrid(x,y)
    W = 0.5 * ( 1 - np.cos( (2*np.pi*X)/(Nx-1) ) )
    W *= 0.5 * ( 1 - np.cos( (2*np.pi*Y)/(Ny-1) ) )
    
    return W

def rotate(array, degree):
    radians = degree*(np.pi/180)  
    x = array[:,0]
    y = array[:,1]    
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, ( [x, y] ) )
    return m

def APR(dset, usf, ref, pxsize = 1, cutoff = None, apodize = True, degree = None, mode = 'fourier'):
    """
    Adaptive pixel reassignment
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    dset        ism dataset, np.array (Nx x Ny x Nch)
    usf         up-sampling factor
    ref         reference channel (typically Nch//2)
    pxsize      XY pixel size
    cutoff      if it is not None, the dset is low-pass filtered at the cutoff frequency
    apodize     if it is not None, the dset is apodized with a Hann window
    degree      if it is not None, the returned shift vector are rotated bt degree [deg]
    mode        registration method: 'fourier' or 'interp'
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    shift_vec       shift vectors (Nch x 2)
    result_ism_pc   reassigned dataset (Nx x Ny x Nch)
    ======
    """
    
    # Low-pass filter dataset
    
    if cutoff is not None:
        if cutoff == 'frc':
            ... #TO BE IMPLEMENTED
        else:
            s = 0.01
            t = cutoff * pxsize
            dset = Low_pass(dset, t, s)
            
    # Apodize dataset
    
    if apodize == True:
        W = hann2d( dset.shape )
        dsetW = np.einsum('ijk, ij -> ijk', dset, W)
    else:
        dsetW = dset
    
    # Calculate shifts
    
    shift_vec, error = ShiftVectors(dsetW, usf, ref)

    # Compensate shifts
    
    result_ism_pc = Reassignment(shift_vec, dset, mode = mode)

    shift_vec *= pxsize

    if degree is not None:
        shift_vec = np.transpose(rotate(shift_vec, degree))

    return shift_vec, result_ism_pc


def ShiftVectors(dset, usf, ref):
    sz = dset.shape
    
    shift_vec = np.empty( (sz[-1], 2) )
    error = np.empty( (sz[-1], 2) )
    
    for i in range( sz[-1] ):
        shift_vec[i,:], error[i,:], diffphase = phase_cross_correlation(dset[:,:, ref], dset[:,:,i], upsample_factor=usf, normalization=None)
    
    return shift_vec, error
    

def Reassignment(shift_vec, dset, mode = 'fourier'):
    
    sz = dset.shape    
    result_ism_pc = np.empty( sz )
    
    if mode == 'fourier':
    
        for i in range( sz[-1] ):
            offset  = fourier_shift(np.fft.fftn(dset[:,:,i]), (shift_vec[i,:]))
            result_ism_pc[:,:,i]  = np.real( np.fft.ifftn(offset) )
        return result_ism_pc
        
    elif mode == 'interp':
        
        for i in range( sz[-1] ):
            result_ism_pc[:,:,i]  = shift( dset[:,:,i], shift_vec[i,:] )
        return result_ism_pc