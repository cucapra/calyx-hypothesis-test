# Calyx Hypothesis Test

Hypothesis is a Python library for creating unit tests which are simpler to write and more powerful when run, finding edge cases in your code you wouldn’t have thought to look for. It is stable, powerful and easy to add to any existing test suite.
Operations are generated using Calyx, and then compared with the standard calculations made in Python to verify the Calyx operator accuracy.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Hypothesis.

```bash
pip install hypothesis
```

## Organization

This repository contains the source code for the following:

1. [`calyx`][] (`calyx/`): The intermediate representation used for hardware

   accelerator generation.

2. [`futil`][] (`src/`): The compiler infrastructure for compiling Calyx programs.

   If `calyx` is like LLVM, then `futil` is Clang.

3. Calyx debugger (`interp/`): An interpreter and debugger for Calyx.

4. `fud`, The Calyx driver: Utility tool that wraps various hardware toolchains.

[site]: https://calyxir.org