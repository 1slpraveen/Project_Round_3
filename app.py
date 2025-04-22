from flask import Flask, render_template, request, send_file, url_for, redirect, make_response
from art import generate_pdf_bank_statement
from datetime import datetime
import os
import io

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
        
        # Create a BytesIO object instead of saving to file
        pdf_buffer = io.BytesIO()
        
        # Generate PDF directly to memory
        generate_pdf_bank_statement(
            account_number=account_number,
            output_file=pdf_buffer
        )
        
        # Seek to the beginning of the buffer
        pdf_buffer.seek(0)
        
        # Create the response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=bank_statement.pdf'
        
        return response
    
    return render_template('generate.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Add this for Vercel
app = app.wsgi_app

if __name__ == '__main__':
    app.run(debug=True)