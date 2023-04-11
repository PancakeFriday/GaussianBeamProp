GaussianBeamProp
===

Gaussian beam propagation through lenses. This script will help plan the layout of lenses.

![Example](https://github.com/PancakeFriday/GaussianBeamProp/blob/main/img/example.png?raw=true)

Example
---

A brief example is given in the following. It initiates an input with a wavelength of 813nm and a waist of 3mm at the origin. We add various lenses, as well as measurement points to get the waist at that specific position. Finally, we plot the result.

```python
import gaussianbeamprop as gp

input_beam = gp.Beam(wavelength=813e-9, waist=3e-3, waist_position=0)
prop = gp.BeamPropagation(input_beam)

prop.add_element(gp.Measure(position=0.3))
prop.add_element(gp.Measure(position=0.73))

prop.add_element(gp.Lens(position=0.2, f=0.1))
prop.add_element(gp.Lens(position=0.4, f=0.2))
prop.add_element(gp.Lens(position=0.6, f=0.1))
prop.add_element(gp.Lens(position=0.7, f=0.3))
prop.add_element(gp.Lens(position=0.8, f=0.9))

prop.plot(figsize=(10, 3), ylim=None, x0=-50e-3, x1=1)
```

Using measured values to initialize a beam
---

```python
import matplotlib.pyplot as plt
import numpy as np

beam_radii = np.array((0.0001, 0.0001126, 0.0001439, 0.00018468))
positions = (0.02, 0.04, 0.06, 0.08)

fitted_beam = gp.Beam.from_beam_sizes(813e-9, beam_radii, positions)
prop = gp.BeamPropagation(fitted_beam)

prop.plot(figsize=(10, 3), ylim=None, x0=-50e-3, x1=0.08)
plt.plot(positions, beam_radii*1e3, "rx")
```

![Fitted Beam](https://github.com/PancakeFriday/GaussianBeamProp/blob/main/img/fitted_beam.png?raw=true)
