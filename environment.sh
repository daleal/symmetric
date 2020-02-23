# Create virtual environment
python3 -m venv .venv

# Activate it
. .venv/bin/activate

# Upgrade pip and install the dependencies.
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate it
deactivate
