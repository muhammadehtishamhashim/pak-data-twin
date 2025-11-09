# Installation & Setup Guide

## 🖥️ System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.10 or higher
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Internet**: Required for initial setup

### Recommended Requirements

- **Operating System**: Latest stable version
- **Python**: 3.11
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **Internet**: Broadband connection

---

## 📦 Prerequisites

### 1. Python Installation

#### Windows
```bash
# Download from python.org
# Or use winget
winget install Python.Python.3.11
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Git Installation

#### Windows
```bash
winget install Git.Git
```

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt install git
```

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/pak-data-twin.git

# Navigate to project directory
cd pak-data-twin
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify Streamlit
streamlit --version
```

---

## 📋 Requirements.txt

```txt
# Core Framework
streamlit==1.50.0

# Data Processing
pandas==2.3.3
numpy==2.2.6

# Visualization
plotly==6.3.1
matplotlib==3.10.7
seaborn==0.13.2

# Machine Learning
tensorflow==2.20.0
scikit-learn==1.7.2
joblib==1.5.2

# Additional Libraries
openpyxl==3.1.5
python-dateutil==2.9.0.post0
```

---

## ⚙️ Configuration

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0f4c3a"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f7fa"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableXsrfProtection = true
```

### Environment Variables (Optional)

Create `.env` file:

```env
# Data paths
DATA_PATH=./datasets_cleaned
MODEL_PATH=./models
PLOTS_PATH=./saved_plots

# API Keys (if needed)
# API_KEY=your_api_key_here
```

---

## 🏃 Running the Application

### Method 1: Standard Run

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run the application
streamlit run app.py
```

### Method 2: With Custom Port

```bash
streamlit run app.py --server.port 8080
```

### Method 3: With Custom Address

```bash
streamlit run app.py --server.address 0.0.0.0
```

### Method 4: Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

---

## 🌐 Accessing the Dashboard

### Local Access

After running the application, open your browser and navigate to:

```
http://localhost:8501
```

### Network Access

To access from other devices on the same network:

```
http://YOUR_IP_ADDRESS:8501
```

Find your IP address:
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

---

## 📁 Project Structure

```
pak-data-twin/
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── dashboard_pages/               # Dashboard modules
│   ├── __init__.py
│   ├── economy.py
│   ├── education.py
│   ├── energy.py
│   └── health.py
├── datasets_cleaned/              # Processed datasets
│   ├── Economy/
│   ├── Education/
│   ├── Energy/
│   └── Health/
├── datasets_raw/                  # Original datasets
├── notebooks/                     # Jupyter notebooks
│   ├── LSTM_GDP_Forecaster.ipynb
│   ├── Debt_and_Liabilities.ipynb
│   └── data_cleaner.ipynb
├── models/                        # Trained ML models
│   ├── lstm_gdp_model.keras
│   ├── lstm_gdp_scaler.joblib
│   └── lstm_gdp_info.joblib
├── saved_plots/                   # Pre-generated forecasts
│   ├── gdp_lstm_forecast_plot.json
│   ├── debt_forecast_plot.json
│   ├── service_exports_forecast_plot.json
│   └── commodities_export.json
├── utils/                         # Utility functions
│   └── plot_loader.py
├── docs/                          # Documentation
└── README.md                      # Project readme
```

---

## 🔧 Troubleshooting Installation

### Issue 1: Python Version Mismatch

**Problem**: `Python 3.10+ required`

**Solution**:
```bash
# Check Python version
python --version

# Install correct version
# See Prerequisites section
```

### Issue 2: pip Install Fails

**Problem**: `ERROR: Could not install packages`

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try installing with --no-cache-dir
pip install --no-cache-dir -r requirements.txt
```

### Issue 3: TensorFlow Installation Issues

**Problem**: TensorFlow fails to install

**Solution**:
```bash
# For Windows/Linux
pip install tensorflow-cpu

# For macOS (M1/M2)
pip install tensorflow-macos
pip install tensorflow-metal
```

### Issue 4: Port Already in Use

**Problem**: `Port 8501 is already in use`

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8501 | xargs kill -9
```

### Issue 5: Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt

# Install specific module
pip install module_name
```

---

## 🐳 Docker Installation (Optional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t pak-data-twin .

# Run container
docker run -p 8501:8501 pak-data-twin
```

---

## 📊 Data Setup

### Download Datasets

If datasets are not included:

```bash
# Create directories
mkdir -p datasets_cleaned/Economy
mkdir -p datasets_cleaned/Education
mkdir -p datasets_cleaned/Energy
mkdir -p datasets_cleaned/Health

# Download from source
# (Add download scripts or instructions)
```

### Run Data Cleaning

```bash
# Open Jupyter notebook
jupyter notebook notebooks/data_cleaner.ipynb

# Run all cells to clean data
```

---

## 🤖 Model Setup

### Download Pre-trained Models

If models are not included:

```bash
# Create models directory
mkdir -p models

# Download models
# (Add download links or scripts)
```

### Train Models from Scratch

```bash
# Open LSTM notebook
jupyter notebook notebooks/LSTM_GDP_Forecaster.ipynb

# Run training cells
# Models will be saved to models/ directory
```

---

## 🔄 Updating the Application

### Pull Latest Changes

```bash
# Pull from repository
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart application
streamlit run app.py
```

### Update Datasets

```bash
# Download new data
# Run data cleaning notebooks
# Restart application
```

---

## 🧪 Testing Installation

### Run Test Script

```python
# test_installation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import tensorflow as tf

print("✅ All imports successful!")
print(f"Streamlit version: {st.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"TensorFlow version: {tf.__version__}")
```

```bash
python test_installation.py
```

---

## 📱 Mobile Access

### Local Network

1. Find your computer's IP address
2. Ensure firewall allows port 8501
3. Access from mobile: `http://YOUR_IP:8501`

### Public Access (Advanced)

Use services like:
- **ngrok**: `ngrok http 8501`
- **Streamlit Cloud**: Deploy to cloud
- **Heroku**: Deploy as web app

---

## 🔐 Security Considerations

### Production Deployment

1. **Use HTTPS**: Enable SSL/TLS
2. **Authentication**: Add user authentication
3. **Environment Variables**: Secure sensitive data
4. **Firewall**: Configure properly
5. **Updates**: Keep dependencies updated

### Best Practices

```bash
# Don't commit sensitive files
echo ".env" >> .gitignore
echo "*.key" >> .gitignore

# Use environment variables
export API_KEY=your_key_here

# Regular updates
pip list --outdated
pip install --upgrade package_name
```

---

## 📞 Support

### Getting Help

1. **Documentation**: Read all docs
2. **Issues**: Check GitHub issues
3. **Community**: Streamlit forum
4. **Email**: Contact maintainers

### Reporting Bugs

Include:
- Python version
- Operating system
- Error messages
- Steps to reproduce

---

**Next**: [API Reference](06_API_REFERENCE.md)
