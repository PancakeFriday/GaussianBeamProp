import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.optimize import curve_fit
import numpy as np

class Beam:
    def __init__(self, wavelength, waist, waist_position=0, zmin=-np.inf, zmax=np.inf):
        self.wavelength = wavelength
        self.waist = waist
        self.rayleigh_range = np.pi*self.waist**2 / wavelength
        self.waist_position = -waist_position
        
        self.zmin = zmin
        self.zmax = zmax

    @classmethod
    def from_beam_sizes(cls, wavelength, beam_sizes, z_positions):
        def fit_func(z, w0, z0):
            zR = np.pi*w0**2 / wavelength
            return w0 * np.sqrt(1 + ((z - z0) / zR) ** 2)

        (waist, waist_position), _ = curve_fit(fit_func, z_positions, beam_sizes, p0=(2*beam_sizes[0], z_positions[0]))

        return cls(wavelength, waist, waist_position)
        
    def spot_size(self, z, do_clip=True):
        """
        Return spot size clipped between zmin and zmax
        """
        z_ = z + self.waist_position
        A = 1 + (z_ / self.rayleigh_range)**2
        if not hasattr(z_, "__len__"):
            z_ = np.array([z_])
        
        if do_clip:
            clip = np.where(z > self.zmin, 1, 0) * np.where(z <= self.zmax, 1, 0)
        else:
            clip = np.ones(len(z_))
        return self.waist * np.sqrt(A) * clip
        
class Lens:
    def __init__(self, position, f):
        self.position = position
        self.f = f
        
class Measure:
    def __init__(self, position):
        self.position = position
        
class BeamPropagation:
    def __init__(self, input_beam):
        self.beams = [input_beam]
        self.measures = []
        self.lenses = []
        
    def add_element(self, element):
        if isinstance(element, Measure):
            self.measures.append(element)
        if isinstance(element, Lens):
            self.lenses.append(element)
            
    def spot_size(self, z):
        y1 = 0
        for b in self.beams:
            y1 += b.spot_size(z)
        return y1
    
    def _create_beams(self):
        self.lenses = sorted(self.lenses, key=lambda x: x.position)
        for i, l in enumerate(self.lenses):
            beam = self.beams[i]
            
            # Calculate new waist position using the thin lens equation
            # https://en.wikipedia.org/wiki/Gaussian_beam#Lens_equation
            z0 = l.position + beam.waist_position
            if z0 == l.f:
                magnification = 1
            else:
                r = beam.rayleigh_range / (z0 - l.f)
                Mr = np.abs(l.f / (z0 - l.f))
                magnification = Mr / np.sqrt(1 + r**2)
            new_waist = magnification * beam.waist
            new_z0 = magnification**2 * (z0 - l.f) + l.f
            
            beam.zmax = l.position
            self.beams.append(Beam(beam.wavelength, new_waist, new_z0 + l.position, zmin=l.position))
        
    def plot(self, figsize=(20, 3), x0=-100e-3, x1=500e-3, ylim=None):
        self._create_beams()
        
        xfine = np.linspace(x0, x1, 1000)
        
        y1 = self.spot_size(xfine)
        y1 *= 1e3 # scale to mm
        y2 = -y1
        
        plt.figure(figsize=figsize)
        
        plt.plot(xfine, y1, c="tab:blue")
        plt.plot(xfine, y2, c="tab:blue")
        
        # for b in self.beams:
        #     plt.plot(xfine, b.spot_size(xfine, do_clip=False)*1e3)
            
        plt.fill_between(xfine, y1, y2, alpha=0.3)
        
        if ylim is not None:
            plt.ylim(-ylim, ylim)
        ylim = plt.gca().get_ylim()
        
        xlim = plt.gca().get_xlim()
        
        for l in self.lenses:
            ellipse = Ellipse(xy=(l.position, 0), width=(xlim[1]-xlim[0])*0.008, height=(ylim[1]-ylim[0])*0.75, 
                        edgecolor='tab:grey', fc='tab:grey', lw=2, alpha=0.7)
            plt.gca().add_patch(ellipse)

        
        for i, m in enumerate(self.measures):
            yval = self.spot_size(m.position)
            text = f"w({m.position}) = {yval:.1e}"
            print(f"Measure {i}: {text}")
            
            plt.axvline(m.position, c="tab:red")
            plt.text(m.position + (xlim[1]-xlim[0])*0.005, ylim[0] + (ylim[1] - ylim[0])*0.05, text)
            
        
        plt.ylabel("Spot size (mm)")
        plt.tight_layout()
