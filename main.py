import argparse
import logging
import random
import pandas as pd
from faker import Faker
import chardet
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataSamplingAnonymizer:
    """
    A tool to randomly sample and anonymize data from CSV files.
    """

    def __init__(self, input_file, output_file, sample_size, columns_to_anonymize, header=True, encoding=None, delimiter=','):
        """
        Initializes the DataSamplingAnonymizer.

        Args:
            input_file (str): Path to the input CSV file.
            output_file (str): Path to the output CSV file.
            sample_size (float): The fraction of rows to sample (0.0 to 1.0).
            columns_to_anonymize (list): List of column names to anonymize.
            header (bool): Whether the CSV file has a header row.
            encoding (str): Encoding of the input CSV file (e.g., 'utf-8', 'latin-1'). If None, attempts to detect.
            delimiter (str): Delimiter used in the CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.sample_size = sample_size
        self.columns_to_anonymize = columns_to_anonymize
        self.header = header
        self.encoding = encoding
        self.delimiter = delimiter
        self.fake = Faker()

        # Input validation
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        if not 0.0 <= self.sample_size <= 1.0:
            raise ValueError("Sample size must be between 0.0 and 1.0")

        if not isinstance(self.columns_to_anonymize, list):
            raise TypeError("Columns to anonymize must be a list")

    def detect_encoding(self):
        """
        Detects the encoding of the input file.
        """
        with open(self.input_file, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']
    
    def load_data(self):
        """
        Loads the data from the CSV file into a pandas DataFrame.
        """
        try:
            if self.encoding is None:
                self.encoding = self.detect_encoding()

            self.data = pd.read_csv(self.input_file, encoding=self.encoding, header=0 if self.header else None, sep=self.delimiter, engine='python')
            
            # Handle no header case
            if not self.header:
              self.data.columns = [f'column_{i}' for i in range(self.data.shape[1])]
              
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise
        
        # Validate that columns exist
        for col in self.columns_to_anonymize:
            if col not in self.data.columns:
                raise ValueError(f"Column '{col}' not found in the input file.")

    def anonymize_data(self):
        """
        Samples the data and anonymizes the specified columns.
        """
        try:
            sampled_data = self.data.sample(frac=self.sample_size, random_state=42)  # Consistent sampling

            for column in self.columns_to_anonymize:
                if column in sampled_data.columns:
                    sampled_data[column] = sampled_data[column].apply(lambda x: self.fake.name() if isinstance(x, str) else self.fake.random_number())

            self.anonymized_data = sampled_data
        except Exception as e:
            logging.error(f"Error anonymizing data: {e}")
            raise

    def save_data(self):
        """
        Saves the anonymized data to the output CSV file.
        """
        try:
            self.anonymized_data.to_csv(self.output_file, index=False, encoding='utf-8')
        except Exception as e:
            logging.error(f"Error saving data: {e}")
            raise

def setup_argparse():
    """
    Sets up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(description="Randomly sample and anonymize data from a CSV file.")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", required=True, help="Path to the output CSV file.")
    parser.add_argument("-s", "--sample_size", type=float, required=True, help="The fraction of rows to sample (0.0 to 1.0).")
    parser.add_argument("-c", "--columns", nargs='+', required=True, help="List of column names to anonymize.")
    parser.add_argument("--no_header", action='store_false', dest='header', default=True, help="Specify if the CSV file does not have a header row.")
    parser.add_argument("-e", "--encoding", help="Encoding of the input CSV file (e.g., 'utf-8', 'latin-1'). If not specified, attempts to detect.", default=None)
    parser.add_argument("-d", "--delimiter", help="Delimiter used in the CSV file", default=',')

    return parser.parse_args()

def main():
    """
    Main function to execute the data sampling and anonymization process.
    """
    try:
        args = setup_argparse()

        anonymizer = DataSamplingAnonymizer(
            input_file=args.input_file,
            output_file=args.output_file,
            sample_size=args.sample_size,
            columns_to_anonymize=args.columns,
            header=args.header,
            encoding=args.encoding,
            delimiter=args.delimiter
        )

        anonymizer.load_data()
        anonymizer.anonymize_data()
        anonymizer.save_data()

        logging.info(f"Data sampled and anonymized successfully. Output saved to {args.output_file}")

    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)
    except TypeError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()

# Example Usage:
# python main.py -i input.csv -o output.csv -s 0.5 -c name email phone
# python main.py -i input.csv -o output.csv -s 0.2 -c column1 column2 --no_header
# python main.py -i input.csv -o output.csv -s 0.75 -c Name Surname -e latin-1 -d ";"