import random
from fpdf import FPDF
from datetime import datetime, timedelta
from decimal import Decimal

# --- Configuration ---
BANK_NAME = "Standard Chartered Bank"
STATEMENT_DATE = datetime.now().strftime('%d/%m/%Y')
CUSTOMER_NAME = "John Doe"
ACCOUNT_NUMBER = "1234567890"

# List of random transaction descriptions
DESCRIPTIONS = [
    "Coffee Shop", "Grocery Store", "ATM Withdrawal", "Salary", "Online Shopping",
    "Restaurant", "Electric Bill", "Transfer", "Mobile Recharge", "Fuel", "Gym Membership"
]

# --- Generate Random Transactions ---
def generate_random_transactions(count=15):
    transactions = []
    base_date = datetime.now()
    for _ in range(count):
        date = base_date - timedelta(days=random.randint(1, 90))
        description = random.choice(DESCRIPTIONS)
        amount = round(random.uniform(-1500, 1500), 2)
        transactions.append({
            'transaction_date': date.strftime('%d-%m-%Y'),
            'description': description,
            'amount': Decimal(amount)
        })
    return transactions

# --- Generate PDF Bank Statement ---
def generate_pdf_bank_statement(
    output_file="bank_statement.pdf",
    bank_name=BANK_NAME,
    customer_name=CUSTOMER_NAME,
    account_number=ACCOUNT_NUMBER
):
    # Create a PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title - Header Section
    pdf.set_font('Arial', 'B', 16)
    pdf.set_fill_color(0, 114, 206)  # Bank Blue Color
    pdf.cell(200, 10, f"{bank_name} - Account Statement", ln=True, align='C', border=0, fill=True)
    
    # Draw a clean blue line beneath the title
    pdf.set_fill_color(0, 114, 206)
    pdf.cell(200, 1, '', ln=True, align='C', border=0, fill=True)  # Blue line
    pdf.ln(5)  # Add some space after the line

    # Customer Information Section
    pdf.set_font('Arial', '', 12)
    pdf.cell(100, 10, f"Customer Name: {customer_name}", ln=True)
    pdf.cell(100, 10, f"Account Number: {account_number}", ln=True)
    pdf.cell(100, 10, f"Statement Date: {STATEMENT_DATE}", ln=True)
    pdf.ln(10)

    # Table Header with Styling
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(230, 242, 255)  # Light Blue for header
    pdf.cell(40, 10, "Date", border=1, align='C', fill=True)
    pdf.cell(100, 10, "Description", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Amount", border=1, align='C', fill=True)
    pdf.ln()

    # Table Content with Alternating Row Colors
    pdf.set_font('Arial', '', 12)
    transactions = generate_random_transactions()
    row_color = [255, 255, 255]  # White for the first row
    for idx, txn in enumerate(transactions):
        if idx % 2 == 0:
            row_color = [230, 242, 255]  # Light Blue for even rows
        else:
            row_color = [255, 255, 255]  # White for odd rows
        pdf.set_fill_color(*row_color)
        pdf.cell(40, 10, txn['transaction_date'], border=1, align='C', fill=True)
        pdf.cell(100, 10, txn['description'], border=1, align='L', fill=True)
        pdf.cell(40, 10, f"${txn['amount']:.2f}", border=1, align='R', fill=True)
        pdf.ln()

    # Footer - Statement Date
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(200, 10, f"Statement generated on {STATEMENT_DATE}", 0, 1, 'C')

    # Bank Footer (e.g., copyright)
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(200, 10, f"{BANK_NAME} &copy; {datetime.now().year}. All rights reserved.", 0, 1, 'C')

    # Output the PDF to a file
    # Handle both file path and BytesIO
    if isinstance(output_file, str):
        pdf.output(output_file)
        print(f"✅ PDF successfully generated: {output_file}")
    else:
        # For BytesIO object
        pdf.output(output_file, 'F')

# --- Main Program ---
if __name__ == "__main__":
    generate_pdf_bank_statement("professional_bank_statement.pdf")
