import requests
import smtplib
import configparser
import time
import sys

def get_stock_price(symbol):
    url = f"https://brapi.dev/quote/{symbol}"
    response = requests.get(url)
    data = response.json()
    return data['price']

def send_alert(email_config, subject, message):
    recipient_email = email_config['recipient_email']
    sender_email = email_config['sender_email']
    smtp_server = email_config['smtp_server']
    smtp_port = int(email_config['smtp_port'])
    smtp_username = email_config['smtp_username']
    smtp_password = email_config['smtp_password']

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        email_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, email_body)

        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def main():
    if len(sys.argv) != 4:
        print("Uso: python stock_quote_alert.py <ativo> <preço_venda> <preço_compra>")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read('config.ini')

    symbol = sys.argv[1]
    sell_price = float(sys.argv[2])
    buy_price = float(sys.argv[3])

    email_config = dict(config['Email'])

    while True:
        current_price = get_stock_price(symbol)
        if current_price <= buy_price:
            send_alert(email_config, f"{symbol} - Comprar", f"Preço atual: {current_price}")
        elif current_price >= sell_price:
            send_alert(email_config, f"{symbol} - Vender", f"Preço atual: {current_price}")

        time.sleep(60)  

if __name__ == "__main__":
    main()