# SquatSpotter

SquatSpotter is a Python application designed to detect and analyze squatting domains. It helps in identifying potentially malicious domains that are similar to legitimate ones, which can be used for phishing or other cyber attacks.

## Features

- Detects domain squatting using various algorithms
- Analyzes domain similarity
- Generates a .txt file in the same directory as the program with a list of potential squatting domains
- Easy to use command-line interface

## Requirements

- Python 3.6 or higher
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/NJSP/SquatSpotter.git
    ```
2. Navigate to the project directory:
    ```sh
    cd SquatSpotter
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the SquatSpotter application, use the following command:
```sh
python SquatSpotter.py <domain>
```

## Example
```sh
python SquatSpotter.py GitHub.com
```