import socket
import ftplib
import yagmail
import time
import pandas as pd
from attack_prediction import predict
from datetime import datetime
from io import BytesIO

HOSTNAME = "ftp.drivehq.com"
USERNAME = "harshith2002har"
PASSWORD = "Boli@123"
FTP_PORT = '21'

print("-------------------------------------")

ip_address = socket.gethostbyname(socket.gethostname())
port = 5003

print("[STARTED]  > Server running at : ", ip_address, " ", port)

print()

s = socket.socket()
s.bind((ip_address, port))
s.listen(5)

print("[LISTENING] > Waiting for connection ..")


def file_download(file_new, res):
    if res == "Benign":
        file_n = "HoneyPot/original/" + file_new
    else:
        file_n = "HoneyPot/duplicate/" + file_new

    ou_file = "files/" + file_new
    with open(ou_file, "wb") as file:
        try:
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            ftp_server.encoding = "utf-8"
            ftp_server.retrbinary(f"RETR {file_n}", file.write)
            file.close()
            print('[SUCCESS]  > File downloaded successfully...')
            return "success"
        except Exception as e:
            print('[FAILED]    >', e)
            return "failed"


def insert_into_excel(file, address, res):
    date = datetime.today()
    r2 = pd.read_excel(file)
    new_row = [date, address, res]
    r2.loc[-1] = new_row
    r2 = r2.reset_index(drop=True)
    r2.to_excel(file, index=False)


def sendmail(user_mail, s_file):
    try:
        yag = yagmail.SMTP(user='ganeshgtganeshgt@gmail.com',
                           password='bvdsvznmosesxonq')
        yag.send(to=user_mail, subject='Sending Attachment',
                 contents='Please find the image attached', attachments='files/' + s_file)
        print('[SUCCESS]  > Email sent successfully...')
        return "success"
    except Exception as e:
        print('[FAILED]    >', e)
        return "failed"


def sendMailToHR(hr_email, client_ip, result, file_name, email_id):
    try:
        yag = yagmail.SMTP(user='ganeshgtganeshgt@gmail.com',
                           password='bvdsvznmosesxonq')
        subject = 'File Sent - IP: ' + client_ip + ', Result: ' + result
        body = 'The file ' + file_name + ' has been sent successfully ' + email_id + '.\n\nIP: ' + \
            client_ip + '\nResult: ' + result
        yag.send(to=hr_email, subject=subject, contents=body)
        # print('[SUCCESS]  > Email sent to HR successfully...')
        return "success"
    except Exception as e:
        print('[FAILED]    >', e)
        return "failed"


while True:
    c, addr = s.accept()
    client_ip = addr[0]
    print()
    print('[CONNECTED]  > Connection got from ' + str(client_ip))
    print()

    msg = "Hello... send the packet"
    c.send(msg.encode("utf-8"))
    print("[MESSAGE SENT] > ", msg)
    print('')

    msg = c.recv(20480)
    df = pd.read_csv(BytesIO(msg))
    df.to_csv('in_folder/Test_Sample.csv', index=False)
    print("[MESSAGE RECEIVED] >  file writing")
    print(" ")
    time.sleep(20)

    print("[MODEL PREDICTION] > Predicting...")
    result = predict()
    insert_into_excel('ip_log.xlsx', client_ip, result)
    print("[MODEL PREDICTED RESULT] > ", result)

    msg = "which file you want ?"
    c.send(msg.encode("utf-8"))
    print('')
    print('[MESSAGE SENT]   > ', msg)

    f_name = c.recv(1024)
    file_name = f_name.decode("utf-8")
    print('')
    print('[MESSAGE RECEIVED] > ', file_name)

    msg = "share your email id !!"
    c.send(msg.encode("utf-8"))
    print('')
    print('[MESSAGE SENT]   >', msg)

    email = c.recv(1024)
    email_id = email.decode("utf-8")
    print('')
    print('[MESSAGE RECEIVED]', email_id)
    print('')
    print('[DOWNLOADING] > File downloading...')
    d = file_download(file_name, result)
    if d == 'success':
        print('')
        print('[SENDING]  >  File Sending to', email_id)
        mail = sendmail(email_id, file_name)
        msg = ''
        if mail == "success":
            msg = "File sent to " + email_id
        else:
            msg = "Opps!! File sending failed to " + email_id

        # c.send(msg.encode("utf-8"))

        hr_email = "h2002harshith@gmail.com"

        mailToHR = sendMailToHR(hr_email, client_ip,
                                result, file_name, email_id)
        print('[SENDING]  >  File Sending to', email_id)
        msg1 = ''
        if mailToHR == "success":
            msg1 = "File sent to " + hr_email
        else:
            msg1 = "Opps!! File sending failed to HR " + hr_email

        c.send(msg.encode("utf-8"))

        print('-----------------------------------------')
        print("[LISTENING] Waiting for new connection ..")
    else:
        msg = "Opps!! Something went wrong"
        c.send(msg.encode("utf-8"))
        c.close()
        print('-----------------------------------------')
        print("[LISTENING] Waiting for new connection ..")
