from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

# Sample financial data for top 10 companies
sample_data = {
    "Tesla": {
        "Revenue": [10000, 12000, 15000, 18000, 20000],
        "Net Income": [1000, 1200, 1500, 1800, 2000],
        "Inventory": [500, 600, 700, 800, 900],
        "Debt": [2000, 2200, 2500, 2800, 3000],
    },
    "Apple": {
        "Revenue": [50000, 55000, 60000, 65000, 70000],
        "Net Income": [10000, 11000, 12000, 13000, 14000],
        "Inventory": [1000, 1200, 1300, 1400, 1500],
        "Debt": [5000, 5500, 6000, 6500, 7000],
    },
    "Amazon": {
        "Revenue": [200000, 220000, 240000, 260000, 280000],
        "Net Income": [10000, 12000, 14000, 16000, 18000],
        "Inventory": [20000, 22000, 24000, 26000, 28000],
        "Debt": [50000, 55000, 60000, 65000, 70000],
    },
    "Google": {
        "Revenue": [150000, 160000, 170000, 180000, 190000],
        "Net Income": [30000, 32000, 34000, 36000, 38000],
        "Inventory": [5000, 5500, 6000, 6500, 7000],
        "Debt": [10000, 11000, 12000, 13000, 14000],
    },
    "Microsoft": {
        "Revenue": [120000, 130000, 140000, 150000, 160000],
        "Net Income": [40000, 42000, 44000, 46000, 48000],
        "Inventory": [3000, 3200, 3400, 3600, 3800],
        "Debt": [20000, 22000, 24000, 26000, 28000],
    },
    "Meta": {
        "Revenue": [80000, 85000, 90000, 95000, 100000],
        "Net Income": [20000, 22000, 24000, 26000, 28000],
        "Inventory": [1000, 1200, 1400, 1600, 1800],
        "Debt": [5000, 5500, 6000, 6500, 7000],
    },
    "Berkshire Hathaway": {
        "Revenue": [250000, 260000, 270000, 280000, 290000],
        "Net Income": [50000, 52000, 54000, 56000, 58000],
        "Inventory": [10000, 11000, 12000, 13000, 14000],
        "Debt": [30000, 32000, 34000, 36000, 38000],
    },
    "Johnson & Johnson": {
        "Revenue": [80000, 85000, 90000, 95000, 100000],
        "Net Income": [15000, 16000, 17000, 18000, 19000],
        "Inventory": [5000, 5500, 6000, 6500, 7000],
        "Debt": [10000, 11000, 12000, 13000, 14000],
    },
    "Visa": {
        "Revenue": [20000, 22000, 24000, 26000, 28000],
        "Net Income": [10000, 11000, 12000, 13000, 14000],
        "Inventory": [0, 0, 0, 0, 0],  # Visa has no inventory
        "Debt": [5000, 5500, 6000, 6500, 7000],
    },
    "Walmart": {
        "Revenue": [500000, 520000, 540000, 560000, 580000],
        "Net Income": [10000, 12000, 14000, 16000, 18000],
        "Inventory": [40000, 42000, 44000, 46000, 48000],
        "Debt": [20000, 22000, 24000, 26000, 28000],
    },
}

# Financial Ratios Calculation
def calculate_ratios(data):
    ratios = {}
    ratios["P/E Ratio"] = data["Revenue"][-1] / data["Net Income"][-1]
    ratios["Debt-to-Equity"] = data["Debt"][-1] / data["Revenue"][-1]
    ratios["Current Ratio"] = data["Revenue"][-1] / data["Debt"][-1]
    return ratios

# Detect Unusual Patterns
def detect_unusual_patterns(data):
    patterns = {}
    inventory_growth = (data["Inventory"][-1] - data["Inventory"][-2]) / data["Inventory"][-2]
    if inventory_growth > 0.2:
        patterns["Inventory Spike"] = f"Inventory increased by {inventory_growth*100:.2f}%"
    return patterns

# Extract Data from PDF
def extract_data_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except PyPDF2.errors.PdfReadError:
        return "Invalid PDF file. Please upload a valid PDF."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# API Endpoints
@app.route("/analyze", methods=["POST"])
def analyze():
    company = request.json.get("company")
    if company in sample_data:
        data = sample_data[company]
        ratios = calculate_ratios(data)
        patterns = detect_unusual_patterns(data)
        return jsonify({"ratios": ratios, "patterns": patterns})
    return jsonify({"error": "Company not found"}), 404

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        text = extract_data_from_pdf(file)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Welcome to FundamentaX Backend! Use /analyze or /upload endpoints."

if __name__ == "__main__":
    app.run(debug=True)
