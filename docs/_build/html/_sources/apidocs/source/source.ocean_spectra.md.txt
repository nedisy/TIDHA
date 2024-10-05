# {py:mod}`source.ocean_spectra`

```{py:module} source.ocean_spectra
```

```{autodoc2-docstring} source.ocean_spectra
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`pierson_moskowitz_spectrum <source.ocean_spectra.pierson_moskowitz_spectrum>`
  - ```{autodoc2-docstring} source.ocean_spectra.pierson_moskowitz_spectrum
    :summary:
    ```
* - {py:obj}`WvHeight <source.ocean_spectra.WvHeight>`
  - ```{autodoc2-docstring} source.ocean_spectra.WvHeight
    :summary:
    ```
````

### API

````{py:function} pierson_moskowitz_spectrum(omega: numpy.typing.NDArray[numpy.float64], Hs: float, Tp: float) -> numpy.typing.NDArray[numpy.float64]
:canonical: source.ocean_spectra.pierson_moskowitz_spectrum

```{autodoc2-docstring} source.ocean_spectra.pierson_moskowitz_spectrum
```
````

````{py:function} WvHeight(omega: numpy.typing.NDArray[numpy.float64], spectrum: numpy.typing.NDArray[numpy.float64], evalTime: numpy.typing.NDArray[numpy.float64], phase_rand: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.complex128]
:canonical: source.ocean_spectra.WvHeight

```{autodoc2-docstring} source.ocean_spectra.WvHeight
```
````
