# Improbable CPR

Generate CPR numbers suitable for testing.

A CPR number is the national identity number of Denmark. They can be divided into two categories based on whether they satisfy a modulo 11 test. Both types are valid, but numbers that do not satisfy the test are only allocated once those that do have been exhausted. Consequently, testing IT systems using numbers that do not satisfy the test reduces the risk of testing using an already allocated number.

As of writing, only 26 days have had numbers that do not satisfy the test allocated.

For more information, see [Personnumre uden kontrolciffer (modulus 11 kontrol)](https://www.cpr.dk/cpr-systemet/personnumre-uden-kontrolciffer-modulus-11-kontrol) (only in danish).

## Install

1. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
2. Install the package:
```bash
pip install --user .
```
3. Run the program as `improbable_cpr`. See `improbable_cpr --help` for options.

## Usage

Run `improbable_cpr --help` for options. For example, to generate 100 CPR numbers, use:
```bash
improbable_cpr --count 100
```

Note running with no options will generate all CPR numbers.

## Development

To install the package in development mode use:
```bash
pip install -e .
```

Subsequently, tests can be run using:
```bash
pytest tests
```

To uninstall the package in development mode, use:
```bash
pip uninstall improbable_cpr
```