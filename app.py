from flask import Flask, request
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import io

app = Flask(__name__)

page_html = """
<!doctype html>
<html>
<head><title>TOPSIS</title></head>
<body>
    <h2>TOPSIS Calculator</h2>
    <form method="post" enctype="multipart/form-data">
        File: <input type="file" name="dataset" required><br><br>
        Weights: <input type="text" name="weights" required><br><br>
        Impacts: <input type="text" name="impacts" required><br><br>
        Email: <input type="email" name="user_email" required><br><br>
        <input type="submit" value="Run">
    </form>
</body>
</html>
"""

def notify_user(email_id, df_result):
    sender = "simantasaha792@gmail.com"
    pwd = "nfifzxddkqhpilmw"

    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Results'
    msg['From'] = sender
    msg['To'] = email_id
    msg.set_content('Here are your results.')

    buffer = io.StringIO()
    df_result.to_csv(buffer, index=False)
    buffer.seek(0)
    
    msg.add_attachment(buffer.getvalue().encode(), maintype='text', subtype='csv', filename='output.csv')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(sender, pwd)
        s.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            f = request.files['dataset']
            w_str = request.form['weights']
            i_str = request.form['impacts']
            email = request.form['user_email']

            df = pd.read_csv(f)
            matrix = df.iloc[:, 1:].values.astype(float)
            w = [float(x) for x in w_str.split(',')]
            imp = i_str.split(',')

            norm = matrix / np.sqrt((matrix**2).sum(axis=0))
            weighted = norm * w

            best = []
            worst = []
            for j in range(len(imp)):
                if imp[j] == '+':
                    best.append(max(weighted[:, j]))
                    worst.append(min(weighted[:, j]))
                else:
                    best.append(min(weighted[:, j]))
                    worst.append(max(weighted[:, j]))

            s_best = np.sqrt(((weighted - best)**2).sum(axis=1))
            s_worst = np.sqrt(((weighted - worst)**2).sum(axis=1))
            
            topsis_score = s_worst / (s_best + s_worst)

            df['Topsis Score'] = topsis_score
            df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

            notify_user(email, df)
            return "Done. Check email."

        except Exception as e:
            return f"Error: {e}"

    return page_html

if __name__ == '__main__':
    app.run(debug=True)