# Supreme Bot

Selenium script to automate Supreme purchases.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
pip install -r requirements.txt
```

Check your system's Chrome version, and download and add the [WebDriver](https://chromedriver.chromium.org/downloads) to the directory accordingly.


## Usage

Update config.py with the right information.
```python
product_type = "sweatshirts" # eg, sweatshirts, shirts, jackets
product_name = "crossover hooded sweatshirt"
product_colour = "Black"   
size = "Small"
```

Run on terminal:
```bash
python supreme.py
```

Set up [Crontab](https://crontab.guru):
```bash
crontab -e
0 8 * * 4 cd /directory/to/Supreme-Bot && DISPLAY=:0 /usr/local/bin/python3 ./supreme.py >> ./logs.txt
```