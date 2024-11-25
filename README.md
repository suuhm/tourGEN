# tourGEN
Simple python script for generating automatic tour dates for your website by scraping the web

![grafik](https://github.com/user-attachments/assets/fec1ec07-1535-4465-a387-dd6cb0de20e5)

## Features
- Fast and simple scarping data from spotify / songkick urls
- Email sending functions
- Automatic via cronjobs / sheduled tasks etc.
- Debug mode for errors
- Raw output hmtl, so you can use your own css  


## Functions and Usage:
```
        ----------------------------------------- 
       |    tourGEN - Tourdate Generator v0.2    |
       |     by suuhm (C) 2023                   |
        --------------------------------------- 

usage: tourgen.py [-h] [--url URL] [--export EXPORT] [--debug] [--mailsend MAILSEND]

Download content from a URL and save it to a file.

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     URL to fetch data from
  --export EXPORT, -f EXPORT
                        Name of the HTML file to save the data
  --debug, -d           Output debugging of site conntent
  --mailsend MAILSEND, -m MAILSEND
                        Get a debugging mail

```

## How to run the script:
Simply download the python file and run this on your serial/ssh console: 
```bash
# Example 
python tourgen.py --url https://www.songkick.com/de/artists/0123-XYZ --export /var/www/yoursite/tourdate.html
```


## How to automatic via cronjob:
Simply put these lines to `/etc/cronjob/`: 
```bash
# Example : Everyday 06:05AM and 03:05PM 
5 6,15 * * * root tourgen.py -u https://www.songkick.com/de/artists/0123-XYZ --export /var/www/yoursite/tourdate.html -m mail@bandsite.com >/dev/null 2>&1
```

## Email configuration
You have to edit the lines in the py file like this:
```bash
    #
    # Email configuration:
    # --------------------
    #
    sender_email = 'tourGEN@example.com'
    recipient_email = MAILADDR
    subject = 'Alert'
    #message = 'This is a test email alert.'

    # SMTP server configuration
    smtp_server = 'localhost'
    smtp_port = 25
    #smtp_port = 587
    #smtp_username = 'your_smtp_username'
    #smtp_password = 'your_smtp_password'
```


<br>
<hr>

## If you have some questions and feature wishes write an issue

#### Verson: 0.2
<hr>

## Attention / This is a PoC script I cannt give any warranty for some damage!

<hr>
