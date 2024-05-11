from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import re
import numpy as np

app = Flask(__name__)
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

@app.route("/calculate_credit", methods=["POST"])
def calculate_credit():
    # Get PDF file from request
    pdf_file = request.files["pdf_file"]
    pdf_file_path = "./uploaded.pdf"
    pdf_file.save(pdf_file_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_file_path)

    # Define patterns for extraction
    patterns = {
        "Current Assets": r"Current Assets[\s\S]*?Total Current Assets (\d+(?:,\d+)*)",
        "Current Liabilities": r"Current Liabilities[\s\S]*?Total Current Liabilities (\d+(?:,\d+)*)",
        "Inventory": r"Inventory (\d+(?:,\d+)*)",
        "Total Debt": r"Total Debt (\d+(?:,\d+)*)",
        "Total Equity": r"Total Equity (\d+(?:,\d+)*)",
        "Earnings Before Interest and Taxes \(EBIT\)": r"Earnings Before Interest and Taxes \(EBIT\) (\d+(?:,\d+)*)",
        "Interest Expense": r"Interest Expense (\d+(?:,\d+)*)",
        "Net Profit": r"Net Profit (\d+(?:,\d+)*)",
        "Revenue": r"Revenue (\d+(?:,\d+)*)",
        "Total Assets": r"Total Assets (\d+(?:,\d+)*)",
        "Cost of Goods Sold \(COGS\)": r"Cost of Goods Sold \(COGS\) (\d+(?:,\d+)*)",
        "Average Inventory": r"Average Inventory (\d+(?:,\d+)*)",
        "Net Credit Sales": r"Net Credit Sales (\d+(?:,\d+)*)",
        "Average Accounts Receivable": r"Average Accounts Receivable (\d+(?:,\d+)*)",
        "Average Accounts Payable": r"Average Accounts Payable (\d+(?:,\d+)*)"
    }

    # Extract values from text
    extracted_values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text)
        if match:
            extracted_values[key] = int("".join(match.group(1).split(",")))

    # Calculate ratios
    ratios = {
    "Current Ratio": extracted_values["Current Assets"] / extracted_values["Current Liabilities"],
    "Quick Ratio": (extracted_values["Current Assets"] - extracted_values["Inventory"]) / extracted_values["Current Liabilities"],
    "Debt-to-Equity Ratio": extracted_values["Total Debt"] / extracted_values["Total Equity"],
    "Interest Coverage Ratio": extracted_values["Earnings Before Interest and Taxes \(EBIT\)"] / extracted_values["Interest Expense"],
    "Net Profit Margin": extracted_values["Net Profit"] / extracted_values["Revenue"]*100,
    "Return on Assets (ROA)": extracted_values["Net Profit"] / extracted_values["Total Assets"]*100,
    "Return on Equity (ROE)": extracted_values["Net Profit"] / extracted_values["Total Equity"]*100,
    "Asset Turnover Ratio": extracted_values["Revenue"] / extracted_values["Total Assets"],
    "Inventory Turnover Ratio": extracted_values["Cost of Goods Sold \(COGS\)"] / extracted_values["Average Inventory"],
    "Accounts Receivable Turnover Ratio": extracted_values["Net Credit Sales"] / extracted_values["Average Accounts Receivable"],
    "Yearly Turnover Score": 800000/extracted_values["Revenue"]*100
}
    for i in ratios:
        if i.endswith("Ratio") and ratios[i]:
            ratios[i] = ratios[i]/(ratios[i]+1)*100


    # Calculate credit risk
    weights = np.array([0.09, 0.11, 0.14, 0.09, 0.11, 0.10, 0.09, 0.05, 0.04, 0.06, 0.12])
    bias = 0
    credit_risk_score = np.dot(np.array(list(ratios.values())), weights) + bias

    # Calculate credit score
    weights = np.array([0.1, 0.1, 0.2, 0.15, 0.15, 0.15, 0.15])
    credit_score = (550/100) * np.dot(np.array(list(ratios.values())[:7]), weights) + 300

    # Return results
    return jsonify({
        "credit_risk_score": round(credit_risk_score,2),
        "credit_score": round(credit_score,2)
    })

@app.route("/sanction", methods=["POST"])
def sanctioned():
    pdf_files = request.files.getlist("pdf_files")
    results = []
    for pdf_file in pdf_files:
        pdf_file_path = "./uploaded.pdf"
        pdf_file.save(pdf_file_path)
        # Extract text from the PDF file
        extracted_text = extract_text_from_pdf(pdf_file_path)
        result = {
            "sanctioned_amount": int("".join(re.findall("Sanction amount Rs. (\d*(?:(\d*,?)*))", extracted_text)[0][0].split(","))),
            "PAN": re.findall("PAN: (.*)", extracted_text)[0]
        }
        results.append(result)
    return jsonify(results)


# @app.route("/sanction", methods=["POST"])
# def sanctioned():
#     pdf_file = request.files["pdf_file"]
#     pdf_file_path = "./uploaded.pdf"
#     pdf_file.save(pdf_file_path)
#     # Extract text from the PDF file
#     extracted_text = extract_text_from_pdf(pdf_file_path)

#     return { "sanctioned":int("".join(re.findall("Sanction amount Rs. (\d*(?:(\d*,?)*))",extracted_text)[0][0].split(","))),
#          "PAN":re.findall("PAN: (.*)",extracted_text)[0] }


if __name__ == "__main__":
    app.run(debug=True)
