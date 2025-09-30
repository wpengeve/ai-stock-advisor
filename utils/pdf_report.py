# utils/pdf_report.py

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'AI Stock Advisor Report', 0, 1, 'C')
        self.ln(10)

def generate_pdf_report(summaries, risk_analysis, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "AI Stock Research Report", ln=True, align="C")
    pdf.ln(10)

    for ticker, stock_summary in summaries:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{ticker}", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, stock_summary)
        pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Risk Comparison", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, risk_analysis)

    pdf.output(filename)