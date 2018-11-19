import numpy as np
import matplotlib.pyplot as plt


def hanningtaper(nmask, ntap):
    r"""1D Hanning taper

    Create unitary mask of length ``nmask`` with Hanning tapering
    at edges of size ``ntap``

    Parameters
    ----------
    nmask : :obj:`int`
        Number of samples of mask
    ntap : :obj:`int`
        Number of samples of hanning tapering at edges

    Returns
    -------
    taper : :obj:`numpy.ndarray`
        taper

    """
    if ntap > 0:
        if(nmask // ntap) < 2:
            ntap_min = nmask/2 if nmask % 2 == 0 else (nmask-1)/2
            raise ValueError('ntap=%d must be smaller or '
                             'equal than %d' %(ntap, ntap_min))
    han_win = np.hanning(ntap*2-1)
    st_tpr = han_win[:ntap,]
    mid_tpr = np.ones([nmask-(2*ntap),])
    end_tpr = np.flipud(st_tpr)
    tpr_1d = np.concatenate([st_tpr, mid_tpr, end_tpr])
    return tpr_1d


def cosinetaper(nmask, square=False):
    r"""1D Cosine or Cosine square taper

    Create unitary mask of length ``nmask`` with Hanning tapering
    at edges of size ``ntap``

    Parameters
    ----------
    nmask : :obj:`int`
        Number of samples of mask
    square : :obj:`bool`
        Cosine square taper (``True``)or Cosine taper (``False``)

    Returns
    -------
    taper : :obj:`numpy.ndarray`
        taper

    """
    exponent = 1 if not square else 2
    tpr_1d = (0.5*(np.cos((np.arange(nmask)-
                           (nmask-1)/2)*np.pi/((nmask-1)/2)) + 1.))**exponent
    return tpr_1d


def taper2d(nt, nmask, ntap, tapertype='hanning', plotflag=False):
    r"""2D taper

    Create 2d mask of size :math:`[n_{mask} \times n_t]`
    with tapering of size ``ntap`` along the first dimension

    Parameters
    ----------
    nt : :obj:`int`
        Number of time samples of mask along second dimension
    nmask : :obj:`int`
        Number of space samples of mask along first dimension
    ntap : :obj:`int`
        Number of samples of tapering at edges of first dimension
    tapertype : :obj:`int`
        Type of taper (``hanning``, ``cosine``, ``cosinesquare`` or ``None``)
    plotflag : :obj:`bool`
        Quickplot

    Returns
    -------
    taper : :obj:`numpy.ndarray`
        2d mask with tapering along first dimension
        of size :math:`[n_{mask} \times n_t]`

    """
    # create 1d window
    if tapertype == 'hanning':
        tpr_1d = hanningtaper(nmask, ntap)
    elif tapertype == 'cosine':
        tpr_1d = cosinetaper(nmask, False)
    elif tapertype == 'cosinesquare':
        tpr_1d = cosinetaper(nmask, True)
    else:
        tpr_1d = np.ones(nmask)

    # replicate taper to second dimension
    tpr_2d = np.tile(tpr_1d[:, np.newaxis], (1, nt))

    if plotflag:
        plt.figure(figsize=(7, 3))
        plt.plot(tpr_1d, 'k', lw=2)
        plt.title('Taper')

    return tpr_2d


def taper3d(nt, nmask, ntap, tapertype='hanning', plotflag=False):
    r"""2D taper

    Create 2d mask of size :math:`[n_{mask}[0] \times n_{mask}[1] \times n_t]`
    with tapering of size ``ntap`` along the first and second dimension

    Parameters
    ----------
    nt : :obj:`int`
        Number of time samples of mask along third dimension
    nmask : :obj:`tuple`
        Number of space samples of mask along first dimension
    ntap : :obj:`tuple`
        Number of samples of tapering at edges of first dimension
    tapertype : :obj:`int`
        Type of taper (``hanning``, ``cosine``,
        ``cosinesquare`` or ``None``)
    plotflag : :obj:`bool`
        Quickplot

    Returns
    -------
    taper : :obj:`numpy.ndarray`
        2d mask with tapering along first dimension
        of size :math:`[n_{mask,0} \times n_{mask,1} \times n_t]`

    """
    nmasky, nmaskx = nmask[0], nmask[1]
    ntapy, ntapx = ntap[0], ntap[1]

    # create 1d window
    if tapertype == 'hanning':
        tpr_y = hanningtaper(nmasky, ntapy)
        tpr_x = hanningtaper(nmaskx, ntapx)
    elif tapertype == 'cosine':
        tpr_y = cosinetaper(nmasky, False)
        tpr_x = cosinetaper(nmaskx, False)
    elif tapertype == 'cosinesquare':
        tpr_y = cosinetaper(nmasky, True)
        tpr_x = cosinetaper(nmaskx, True)
    else:
        tpr_y = np.ones(nmasky)
        tpr_x = np.ones(nmaskx)

    tpr_yx = np.outer(tpr_y, tpr_x)

    # replicate taper to third dimension
    tpr_3d = np.tile(tpr_yx[:, :, np.newaxis], (1, nt))

    if plotflag:
        plt.figure(figsize=(7, 3))
        plt.imshow(tpr_3d[:, :, int(nt/2)], 'jet')
        plt.title('Taper in y-x slice')
        plt.xlabel('x')
        plt.ylabel('y')

    return tpr_3d
