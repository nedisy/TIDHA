# {py:mod}`source.hydrodynamic_forces`

```{py:module} source.hydrodynamic_forces
```

```{autodoc2-docstring} source.hydrodynamic_forces
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`rdtn_force <source.hydrodynamic_forces.rdtn_force>`
  - ```{autodoc2-docstring} source.hydrodynamic_forces.rdtn_force
    :summary:
    ```
* - {py:obj}`exct_force <source.hydrodynamic_forces.exct_force>`
  - ```{autodoc2-docstring} source.hydrodynamic_forces.exct_force
    :summary:
    ```
````

### API

````{py:function} rdtn_force(t: float, dT: float, Trdtn: numpy.typing.NDArray[numpy.float64], IRF: numpy.typing.NDArray[numpy.float64], t_vel_history: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]
:canonical: source.hydrodynamic_forces.rdtn_force

```{autodoc2-docstring} source.hydrodynamic_forces.rdtn_force
```
````

````{py:function} exct_force(WvHeadingIdx: int, omega_i: numpy.typing.NDArray[numpy.float64], omega: numpy.typing.NDArray[numpy.float64], phase_rand: numpy.typing.NDArray[numpy.float64], spectrum: numpy.typing.NDArray[numpy.float64], Fex: numpy.typing.NDArray[numpy.complex128], exctnTime: numpy.typing.NDArray[numpy.complex128]) -> numpy.typing.NDArray[numpy.float64]
:canonical: source.hydrodynamic_forces.exct_force

```{autodoc2-docstring} source.hydrodynamic_forces.exct_force
```
````
