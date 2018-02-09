"""
Binds a LibXC Functional struct to a Python object
"""

import ctypes
import numpy as np

from .core import core
from . import flags
from . import util
from . import structs

### Bind required ctypes

# Build out a few common tmps
_ndptr = np.ctypeslib.ndpointer(dtype=np.double, flags=("C", "A"))
_ndptr_w = np.ctypeslib.ndpointer(dtype=np.double, flags=("W", "C", "A"))  # Writable

_xc_func_p = ctypes.POINTER(structs.xc_func_type)
_xc_func_info_p = ctypes.POINTER(structs.xc_func_info_type)

# Allocation wrappers
core.xc_func_alloc.restype = _xc_func_p

core.xc_func_init.argtypes = (_xc_func_p, ctypes.c_int, ctypes.c_int)
core.xc_func_init.restype = ctypes.c_int

core.xc_func_end.argtypes = (_xc_func_p, )

core.xc_func_free.argtypes = (_xc_func_p, )

# Info wrappers
core.xc_func_get_info.argtypes = (_xc_func_p, )
core.xc_func_get_info.restype = _xc_func_info_p

core.xc_func_info_get_kind.argtypes = (_xc_func_info_p, )

core.xc_func_info_get_name.argtypes = (_xc_func_info_p, )
core.xc_func_info_get_name.restype = ctypes.c_char_p

core.xc_func_info_get_family.argtypes = (_xc_func_info_p, )

core.xc_func_info_get_flags.argtypes = (_xc_func_info_p, )

core.xc_func_info_get_references.argtypes = (_xc_func_info_p, ctypes.c_int)
core.xc_func_info_get_references.restype = ctypes.POINTER(structs.func_reference_type)

# Setters
core.xc_func_info_get_n_ext_params.argtypes = (_xc_func_info_p, )

core.xc_func_info_get_ext_params_description.argtypes = (_xc_func_info_p, ctypes.c_int)
core.xc_func_info_get_ext_params_description.restype = ctypes.c_char_p

core.xc_func_info_get_ext_params_default_value.argtypes = (_xc_func_info_p, ctypes.c_int)
core.xc_func_info_get_ext_params_default_value.restype = ctypes.c_double

core.xc_func_set_ext_params.argtypes = (_xc_func_p, _ndptr)

core.xc_func_set_dens_threshold.argtypes = (_xc_func_p, ctypes.c_double)

# LDA computers
core.xc_lda.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w, _ndptr_w, _ndptr_w, _ndptr_w)
core.xc_lda_exc_vxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w, _ndptr_w)
core.xc_lda_exc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w)
core.xc_lda_vxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w)
core.xc_lda_fxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w)
core.xc_lda_kxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr_w)

# GGA computers
core.xc_gga.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 10))
core.xc_gga_exc_vxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 3))
core.xc_gga_exc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 1))
core.xc_gga_vxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 2))
core.xc_gga_fxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 3))
core.xc_gga_kxc.argtypes = (_xc_func_p, ctypes.c_int, _ndptr, _ndptr, *([_ndptr_w] * 4))

# MGGA computers
core.xc_mgga.argtypes = (_xc_func_p, ctypes.c_int, *([_ndptr] * 4), *([_ndptr_w] * 15))
core.xc_mgga_exc_vxc.argtypes = (_xc_func_p, ctypes.c_int, *([_ndptr] * 4), *([_ndptr_w] * 5))
core.xc_mgga_exc.argtypes = (_xc_func_p, ctypes.c_int, *([_ndptr] * 4), *([_ndptr_w] * 1))
core.xc_mgga_vxc.argtypes = (_xc_func_p, ctypes.c_int, *([_ndptr] * 4), *([_ndptr_w] * 4))
core.xc_mgga_fxc.argtypes = (_xc_func_p, ctypes.c_int, *([_ndptr] * 4), *([_ndptr_w] * 10))

### Build LibXCFunctional class


def _check_arrays(current_arrays, required, sizes, factor):
    """
    A specialized function built to construct and check the sizes of arrays given to the LibXCFunctional class.
    """

    # Nothing supplied so we build it out
    if current_arrays is None:
        current_arrays = {}
        for label in required:
            size = sizes["n_" + label]
            current_arrays[label] = np.zeros((size, factor))

    # Supplied arrays, check sizes
    else:
        missing = set(required) - set(current_arrays)
        if len(missing):
            raise KeyError("Missing the following output arrays: %s" % ", ".join(missing))

        for label in required:
            size = sizes["n_" + label] * factor
            if size != current_arrays[label].size:
                raise ValueError("Supplied output array '%s' does not have the correct shape number of points by %d" %
                                 (label, size))

    ret = [current_arrays[x] for x in required]
    return ret


class LibXCFunctional(object):
    def __init__(self, func_name, spin):
        """
        The primary LibXCFunctional class used to build and compute DFT exchange-correlation quantities.

        Parameters
        ----------
        func_name : int or str
            Either the functional name or ID used to create the LibXCFunctional.
        spin : int or str
            The spin of the requested functional either "unpolarized" (1) or polarized" (2).

        Returns
        -------
        func : LibXCFunctional
            A constructed LibXCFunctional.

        Examples
        --------
        >>> pylibxc.util.xc_family_from_id(72)
        (4, 3)

        """
        self.xc_func = None
        self._xc_func_init = False

        # Handle func_name
        if isinstance(func_name, str):
            func_id = util.xc_functional_get_number(func_name)
            if func_id == -1:
                raise KeyError("LibXC Functional name '%s' not found." % func_name)
        elif isinstance(func_name, int):
            func_id = func_name
            if util.xc_functional_get_name(func_name) is None:
                raise KeyError("LibXC Functional ID '%d' not found." % func_name)
        else:
            raise TypeError("func_name must either be a string or int.")

        # Handle spin
        if isinstance(spin, str):
            spin = spin.lower()
            if spin == "polarized":
                self._spin = 2
            elif spin == "unpolarized":
                self._spin = 1
            else:
                raise KeyError("Spin must either be 'polarized' or 'unpolarized' if represented by a string.")
        else:
            self._spin = spin

        if self._spin not in [1, 2]:
            raise KeyError("Spin must either be 1 or 2 if represented by a integer.")

        # Build the LibXC functional
        self.xc_func = core.xc_func_alloc()
        self.xc_func_size_names = [x for x in dir(self.xc_func.contents) if "n_" in x]

        # Set all int attributes to zero (not all set to zero in libxc)
        for attr in self.xc_func_size_names:
            setattr(self.xc_func.contents, attr, 0)

        ret = core.xc_func_init(self.xc_func, func_id, self._spin)
        if ret != 0:
            raise ValueError("LibXC Functional construction did not complete. Error code %d" % ret)
        self._xc_func_init = True

        # Pull out all sizes after init
        self.xc_func_sizes = {}
        for attr in self.xc_func_size_names:
            self.xc_func_sizes[attr] = getattr(self.xc_func.contents, attr)

        # Unpack functional info
        self.xc_func_info = core.xc_func_get_info(self.xc_func)
        self._number = core.xc_func_info_get_number(self.xc_func_info)
        self._kind = core.xc_func_info_get_kind(self.xc_func_info)
        self._name = core.xc_func_info_get_name(self.xc_func_info).decode("UTF-8")
        self._family = core.xc_func_info_get_family(self.xc_func_info)
        self._flags = core.xc_func_info_get_flags(self.xc_func_info)

        # Set derivatives
        self._have_exc = self._flags & flags.XC_FLAGS_HAVE_EXC
        self._have_vxc = self._flags & flags.XC_FLAGS_HAVE_VXC
        self._have_fxc = self._flags & flags.XC_FLAGS_HAVE_FXC
        self._have_kxc = self._flags & flags.XC_FLAGS_HAVE_KXC
        self._have_lxc = self._flags & flags.XC_FLAGS_HAVE_LXC

        # Set omega
        self._have_cam = self._flags & flags.XC_FLAGS_HYB_CAM
        self._have_cam |= self._flags & flags.XC_FLAGS_HYB_CAMY
        self._have_cam |= self._flags & flags.XC_FLAGS_HYB_LC
        self._have_cam |= self._flags & flags.XC_FLAGS_HYB_LCY
        self._cam_omega = self._cam_alpha = self._cam_beta = False
        if self._have_cam:
            self._cam_omega = self.xc_func.contents.cam_omega
            self._cam_alpha = self.xc_func.contents.cam_alpha
            self._cam_beta = self.xc_func.contents.cam_beta

        elif self._family in [flags.XC_FAMILY_HYB_GGA, flags.XC_FAMILY_HYB_MGGA]:
            self._cam_alpha = self.xc_func.contents.cam_alpha

        # VV10
        self._have_vv10 = self._flags & flags.XC_FLAGS_VV10
        self._nlc_b = self._nlc_C = False
        if self._have_vv10:
            self._nlc_b = self.xc_func.contents.nlc_b
            self._nlc_C = self.xc_func.contents.nlc_C

        # Stable
        self._stable = self._flags & flags.XC_FLAGS_STABLE
        self._dev = self._flags & flags.XC_FLAGS_DEVELOPMENT

        # Laplacian
        self._dev = self._flags & flags.XC_FLAGS_NEEDS_LAPLACIAN

        # Pull out references
        self._refs = []
        self._bibtexs = []
        self._dois = []

        for pos in range(flags.XC_MAX_REFERENCES):
            ref = core.xc_func_info_get_references(self.xc_func_info, pos)
            if not ref: break

            self._refs.append(ref.contents.ref.decode("UTF-8"))
            self._bibtexs.append(ref.contents.bibtex.decode("UTF-8"))
            self._dois.append(ref.contents.doi.decode("UTF-8"))

    def __del__(self):
        """
        Cleans up the LibXC C struct on deletion
        """
        if self.xc_func is None:
            return

        if self._xc_func_init:
            core.xc_func_end(self.xc_func)

        core.xc_func_free(self.xc_func)

    ### Getters

    def get_number(self):
        """
        Returns the LibXCFunctional ID.
        """

        return self._number

    def get_kind(self):
        """
        Returns the LibXCFunctional kind.
        """

        return self._kind

    def get_name(self):
        """
        Returns the LibXCFunctional name.
        """

        return self._name

    def get_family(self):
        """
        Returns the LibXCFunctional family.
        """

        return self._family

    def get_flags(self):
        """
        Returns the LibXCFunctional flags.
        """

        return self._flags

    def get_references(self):
        """
        Returns the LibXCFunctional references.
        """

        return self._refs

    def get_bibtex(self):
        """
        Returns the LibXCFunctional bibtex references.
        """

        return self._bibtexs

    def get_doi(self):
        """
        Returns the LibXCFunctional reference DOIs.
        """

        return self._dois

    def get_hyb_exx_coef(self):
        """
        Returns the amount of global exchange to include.
        """

        if self._cam_alpha is False:
            raise ValueError("Can only be called on Hybrid functionals.")

        return self._cam_alpha

    def get_cam_coef(self):
        """
        Returns the (omega, alpha, beta) quantites
        """

        if self._cam_omega is False:
            raise ValueError("Can only be called on CAM functionals.")

        return (self._cam_omega, self._cam_alpha, self._cam_beta)

    def get_vv10_coef(self):
        """
        Returns the VV10 (b, C) coefficients
        """

        if self._nlc_b is False:
            raise ValueError("Can only be called on -V functionals.")

        return (self._nlc_b, self._nlc_C)

    ### Setters

    def get_ext_param_descriptions(self):
        """
        Gets the description of all external parameters
        """
        num_param = core.xc_func_info_get_n_ext_params(self.xc_func_info)

        ret = []
        for p in range(num_param):
            tmp = core.xc_func_info_get_ext_params_description(self.xc_func_info, p)
            ret.append(tmp.decode("UTF-8"))

        return ret

    def get_ext_param_default_values(self):
        """
        Gets the default value of all external parameters.
        """
        num_param = core.xc_func_info_get_n_ext_params(self.xc_func_info)

        ret = []
        for p in range(num_param):
            tmp = core.xc_func_info_get_ext_params_default_value(self.xc_func_info, p)
            ret.append(tmp)

        return ret

    def set_ext_params(self, ext_params):
        """
        Sets all external parameters.
        """
        num_param = core.xc_func_info_get_n_ext_params(self.xc_func_info)
        if num_param == 0:
            raise ValueError("The LibXCFunctional '%s' has no extermal parameters to set." % self.get_name())

        if len(ext_params) != num_param:
            raise ValueError(
                "The length of the input external parameters (%d) does not match the length of the Functionals external parameters (%d)."
                % (len(ext_params), num_param))

        core.xc_func_set_ext_params(self.xc_func, np.asarray(ext_params, dtype=np.double))

    def set_dens_threshold(self, dens_threshold):
        """
        Sets the density threshold in which densities will not longer be computer.
        """

        if dens_threshold < 0:
            raise ValueError("The density threshold cannot be smaller than 0.")

        core.xc_func_set_dens_threshold(self.xc_func, ctypes.c_double(dens_threshold))

    def compute(self, inp, output=None, do_exc=True, do_vxc=True, do_fxc=False, do_kxc=False):
        """
        Evaluates the functional and its derivatives on a grid.

        Parameters
        ----------
        inp : np.ndarray or dict of np.ndarray
            A input dictionary of NumPy array-like structures that provide the density on a grid and its derivaties. These are labled:
                rho - the density on a grid
                sigma - the contracted density gradients
                lapl - the laplacian of the density
                tau - the kinetic energy density

            Each family of functionals requires different derivates:
                LDA: rho
                GGA: rho, sigma
                MGGA: rho, sigma, lapl (optional), tau

        output : dict of np.ndarray (optional, None)
            Contains a dictionary of NumPy array-like structures to use as output data. If none are supplied this
            function will build an output space for you. The output dictionary depends on the derivates requested.
            A comprehensive list is provided below for each functional family.
                LDA:
                    EXC: zk
                    VCX: vrho
                    FXC: v2rho2
                    KXC: v3rho3
                GGA:
                    EXC: zk
                    VCX: vrho, vsigma
                    FXC: v2rho2, v2rhosigma, v2sigma2
                    KXC: v3rho3, v3rho2sigma, v3rhosigma2, v3sigma3
                MGGA:
                    EXC: zk
                    VCX: vrho, vsigma, vlapl (optional), vtau

            For unpolarized functional the spin pieces are summed together. However, for polarized functionals the following order will be used for output quantities:

                VXC:
                    vrho         = (u, d)
                    vsigma       = (uu, ud, dd)
                    vlapl        = (u, d)
                    vtau         = (u, d)

                FXC:
                    v2rho2       = (u_u, u_d, d_d)
                    v2gamma2     = (uu_uu, uu_ud, uu_dd, ud_ud, ud_dd, dd_dd)
                    v2rhogamma   = (u_uu, u_ud, u_dd, d_uu, d_ud, d_dd)

                KXC:
                    v3rho2sigma  = (u_u_uu, u_u_ud, u_u_dd, u_d_uu, u_d_ud, u_d_dd, d_d_uu, d_d_ud, d_d_dd)
                    v3rhosigma2  = (u_uu_uu, u_uu_ud, u_uu_dd, u_ud_ud, u_ud_dd, u_dd_dd, d_uu_uu, d_uu_ud, d_uu_dd,
                                    d_ud_ud, d_ud_dd, d_dd_dd)
                    v3sigma      = (uu_uu_uu, uu_uu_ud, uu_uu_dd, uu_ud_ud, uu_ud_dd, uu_dd_dd, ud_ud_ud, ud_ud_dd,
                                    ud_dd_dd, dd_dd_dd)

        do_exc : bool (optional, True)
            Do evaluate the the functional?
        do_vxc : bool (optional, True)
            Do evaluate the derivative of the functional?
        do_fxc : bool (optional, False)
            Do evaluate the 2nd derivative of the functional?
        do_kxc : bool (optional, False)
            Do evaluate the 3rd derivative of the functional?

        Returns
        -------
        output : dict of np.ndarray
            A dictionary of NumPy array-like structures. See the output section above for the expected returns.

        Examples
        --------

        # Build functional
        >>> func = pylibxc.LibXCFunctional("gga_c_pbe", "unpolarized")

        # Create input
        >>> inp = {}
        >>> inp["rho"] = np.random.random((3))
        >>> inp["sigma"] = np.random.random((3))

        # Compute
        >>> ret = func.compute(inp)
        >>> for k, v in ret.items():
        >>>     print(k, v)

        zk [[-0.06782171 -0.05452743 -0.04663709]]
        vrho [[-0.08349967 -0.0824188  -0.08054892]]
        vsigma [[ 0.00381277  0.00899967  0.01460601]]

        """

        # Check flags
        if not self._have_exc and do_exc:
            raise ValueError("Functional '%s' does not have EXC capabilities." % self.get_name())
        if not self._have_vxc and do_vxc:
            raise ValueError("Functional '%s' does not have VXC capabilities." % self.get_name())
        if not self._have_fxc and do_fxc:
            raise ValueError("Functional '%s' does not have FXC capabilities." % self.get_name())
        if not self._have_kxc and do_kxc:
            raise ValueError("Functional '%s' does not have KXC capabilities." % self.get_name())

        # Parse input arrays
        if isinstance(inp, np.ndarray):
            inp = {"rho": np.asarray(inp, dtype=np.double)}
        elif isinstance(inp, dict):
            inp = {k: np.asarray(v, dtype=np.double) for k, v in inp.items()}
        else:
            raise KeyError("Input must have a 'rho' variable or a single array.")

        # How long are we?
        npoints = int(inp["rho"].size / self._spin)
        if (inp["rho"].size % self._spin):
            raise ValueError("Rho input has an invalid shape, must be divisible by %d" % self._spin)

        # Find the right compute function
        args = [self.xc_func, ctypes.c_int(npoints)]
        if self.get_family() == flags.XC_FAMILY_LDA:

            # Build input args
            required_input = ["rho"]
            args.extend(_check_arrays(inp, required_input, self.xc_func_sizes, npoints))
            input_num_args = len(args)

            # Hybrid computers
            if do_exc and do_vxc and do_fxc and do_kxc:
                required_fields = ["zk", "vrho", "v2rho2", "v3rho3"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda(*args)
                do_exc = do_vxc = do_fxc = do_kxc = False

            if do_exc and do_vxc:
                required_fields = ["zk", "vrho"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda_exc_vxc(*args)
                do_exc = do_vxc = False

            # Individual computers
            if do_exc:
                required_fields = ["zk"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda_exc(*args)
            if do_vxc:
                required_fields = ["vrho"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda_vxc(*args)
            if do_fxc:
                required_fields = ["v2rho2"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda_fxc(*args)
            if do_kxc:
                required_fields = ["v3rho3"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_lda_kxc(*args)

        elif self.get_family() in [flags.XC_FAMILY_GGA, flags.XC_FAMILY_HYB_GGA]:

            # Build input args
            required_input = ["rho", "sigma"]
            args.extend(_check_arrays(inp, required_input, self.xc_func_sizes, npoints))
            input_num_args = len(args)

            # Hybrid computers
            if do_exc and do_vxc and do_fxc and do_kxc:
                required_fields = [
                    "zk", "vrho", "vsigma", "v2rho2", "v2rhosigma", "v2sigma2", "v3rho3", "v3rho2sigma", "v3rhosigma2",
                    "v3sigma3"
                ]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga(*args)
                do_exc = do_vxc = do_fxc = do_kxc = False

            if do_exc and do_vxc:
                required_fields = ["zk", "vrho", "vsigma"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga_exc_vxc(*args)
                do_exc = do_vxc = False

            # Individual computers
            if do_exc:
                required_fields = ["zk"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga_exc(*args)
            if do_vxc:
                required_fields = ["vrho", "vsigma"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga_vxc(*args)
            if do_fxc:
                required_fields = ["v2rho2", "v2rhosigma", "v2sigma2"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga_fxc(*args)
            if do_kxc:
                required_fields = ["v3rho3", "v3rho2sigma", "v3rhosigma2", "v3sigma3"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_gga_kxc(*args)

        elif self.get_family() in [flags.XC_FAMILY_MGGA, flags.XC_FAMILY_HYB_MGGA]:
            # Build input args
            required_input = ["rho", "sigma", "lapl", "tau"]
            args.extend(_check_arrays(inp, required_input, self.xc_func_sizes, npoints))
            input_num_args = len(args)

            # Hybrid computers

            # Wait until FXC and KXC are available
            # if do_exc and do_vxc and do_fxc and do_kxc:
            #     required_fields = [
            #         "zk", "vrho", "vsigma", "vlapl", "vtau", "v2rho2", "v2sigma2", "v2lapl2", "v2tau2", "v2rhosigma",
            #         "v2rholapl", "v2rhotau", "v2sigmalapl", "v2sigmatau", "v2lapltau"
            #     ]
            #     args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
            #     core.xc_mgga(*args)
            #     do_exc = do_vxc = do_fxc = do_kxc = False

            if do_exc and do_vxc:
                required_fields = ["zk", "vrho", "vsigma", "vlapl", "vtau"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_mgga_exc_vxc(*args)
                do_exc = do_vxc = False

            # Individual computers
            if do_exc:
                required_fields = ["zk"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_mgga_exc(*args)
            if do_vxc:
                required_fields = ["vrho", "vsigma", "vlapl", "vtau"]
                args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                core.xc_mgga_vxc(*args)
            if do_fxc:
                raise KeyError("FXC quantities (2rd derivitives) are not defined for MGGA's! (%d)")
                # required_fields = [
                #     "v2rho2", "v2sigma2", "v2lapl2", "v2tau2", "v2rhosigma", "v2rholapl", "v2rhotau", "v2sigmalapl",
                #     "v2sigmatau", "v2lapltau"
                # ]
                # args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                # core.xc_mgga_fxc(*args)
            if do_kxc:
                raise KeyError("KXC quantities (3rd derivitives) are not defined for MGGA's! (%d)")
                # required_fields = ["v3rho3", "v3rho2sigma", "v3rhosigma2", "v3sigma3"]
                # args.extend(_check_arrays(output, required_fields, self.xc_func_sizes, npoints))
                # core.xc_gga_kxc(*args)
        else:
            raise KeyError("Functional kind not recognized! (%d)" % self.get_kind())

        # Return a dictionary
        return {k: v for k, v in zip(required_fields, args[input_num_args:])}
