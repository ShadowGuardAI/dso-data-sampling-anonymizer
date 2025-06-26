# dso-data-sampling-anonymizer
Randomly samples rows or columns from a dataset and replaces sensitive information in the sampled data with dummy values, reducing the size of the dataset while preserving statistical properties for testing purposes. - Focused on Tools for sanitizing and obfuscating sensitive data within text files and structured data formats

## Install
`git clone https://github.com/ShadowGuardAI/dso-data-sampling-anonymizer`

## Usage
`./dso-data-sampling-anonymizer [params]`

## Parameters
- `-h`: Show help message and exit
- `-i`: Path to the input CSV file.
- `-o`: Path to the output CSV file.
- `-s`: No description provided
- `-c`: List of column names to anonymize.
- `--no_header`: Specify if the CSV file does not have a header row.
- `-e`: Encoding of the input CSV file (e.g., 
- `-d`: Delimiter used in the CSV file

## License
Copyright (c) ShadowGuardAI
