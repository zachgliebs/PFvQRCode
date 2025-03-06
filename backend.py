# app.py
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Simulated database for storing the redirect URL
redirect_data = {"current_url": "https://www.google.com/"}

# Endpoint to generate and serve the QR code
@app.route('/qr-code')
def qr_code():
    # The QR code will point to this redirect endpoint
    qr_url = request.host_url + "redirect"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # Save QR code as an image file
    img_path = "static/qr_code.png"
    if not os.path.exists("static"):
        os.makedirs("static")
    img.save(img_path)
    return redirect(f"/{img_path}")

# Redirect endpoint for the QR code
@app.route('/redirect')
def dynamic_redirect():
    # Fetch the current URL from the simulated database
    current_url = redirect_data.get("current_url", "https://example.com")
    return redirect(current_url)

# Page to update the destination URL
@app.route('/update', methods=['GET', 'POST'])
def update_url():
    if request.method == 'POST':
        new_url = request.form.get('url')
        if new_url:
            # Update the simulated database with the new URL
            redirect_data["current_url"] = new_url
            return render_template('update.html', message="URL updated successfully!", current_url=new_url)
        else:
            return render_template('update.html', message="Invalid URL!", current_url=redirect_data["current_url"])
    
    # Render the update page with the current URL
    return render_template('update.html', current_url=redirect_data["current_url"])

# Main page to display the QR code


if __name__ == '__main__':
    app.run(debug=True)
