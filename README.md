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
