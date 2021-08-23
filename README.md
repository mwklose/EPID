# Twister Plots for Time-to-Event Studies

### Paul N Zivich, Stephen R Cole, Alexander Breskin

## Supplementary Materials

The electronic supplementary materials consists of the SAS (`twister.sas`), R (`twister.R`), and Python
(`twister.py`) files to generate the example twister plot presented in the figure. Risk differences and
associated confidence intervals estimated from the reconstructed data set are available in
`data_twister.csv`.

### Manifesto
`data_twister.csv`
- Estimated risk differences and risk ratios (vaccine minus placebo) and associated confidence 
  intervals for each unique event time from the recreated Pfizer data.

`twister.sas`
- SAS code to generate twister plots. Demonstrated with applied example

`twister.R`
- R code to generate twister plots. Consists of a generalized function and example of function in use
- Dependencies: `ggplot2`

`twister.py`
- Python 3.6+ code to generate twister plots. Consists of a generalized function and example of
  function in use
- Dependencies: `numpy`, `pandas`, `matplotlib`
