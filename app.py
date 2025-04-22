from flask import Flask, render_template, request, send_file, url_for, redirect
from art import generate_pdf_bank_statement
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Add this line for Vercel
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"statement_{timestamp}.pdf"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        generate_pdf_bank_statement(
            account_number=account_number,
            output_file=filepath
        )
        
        return send_file(filepath, as_attachment=True)
    
    return render_template('generate.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)