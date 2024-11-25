#!/usr/bin/env python3

#
# tourGEN - Tourdate Generator v0.2
# All rights reserved - (c) 2023 - suuhm
#
# ---------------------------------------
#
# Set Crontab:
#
# vi /etc/crontab
# # GET NEW TOUDATES?
# 5 6,12,16,20,23 * * * root tourgen.py -u https://... -m mail@bandsite.com >/dev/null 2>&1
#
# PIP / VIRTUALENV
# ----------------
# python -m pip install --upgrade pip
#
# apt install python-pip python3-pip python3-virtualenv
# ALT: ( pip install virualenv )
# virtualenv [--python=python3] project-XYZ
# cd project-XYZ ; source bin/activate
#
# pip list
# deactivate
# -----------------
# pip freeze [--local] > requirements.txt
# pip install -r requirements.txt
#


import argparse
import requests
from urllib.parse import urlparse
from datetime import datetime
#from bs4 import BeautifulSoup
import re

def sendmail(message, MAILADDR):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

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


    if args.mailsend:
        recipient_email = args.mailsend
    else:
        recipient_email= recipient_email

    # Create a MIMEText object
    #msg = MIMEText(message)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(message, 'plain')
    part2 = MIMEText(message, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        #server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print('\n[*] Email sent successfully.')
    except Exception as e:
        print('\n[!!] Failed to send email:', str(e))




def set_songkick(pattern, page, trRows, aTourDates=None, COUNT=0, top3=False):

    #Cleanup breakslines:
    sContent = page.text.replace('\n', '').replace('\r\t', '')
    sURL = "sURL"
    skurl = "https://www.songkick.com"
    b64img = "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"
    if args.debug:
       print("\n[*] Debug REGEXOUT: " + sContent)



    if trRows != "" and top3 == True:
        print("\n[!!] Setup Top 3 past shows:")
        print("       -----------------------")
        past_shows = r'past\".+past\-tou.+?ref..([^\"].+?)\"' #link show more
        aP = re.search(past_shows, sContent)
        if aP:
            sURL = aP.group(1)
            r = 1
        else:
            print("No match found for past shows.")
            r = 0
    elif trRows != "" and top3 == False:

        URL = args.url
        try:
            page = requests.get(URL + "/gigography")
            stat = page.raise_for_status()

            print(f"\n[*] Downloaded content from {URL} and saved it to html status: {stat}")

        except Exception as e:
            print(f"\n[!] An error occurred: {str(e)}")

        pattern = r'<li title=.+?datetime=\"([^\"]+)\".+?ref=\"(.+?)\".+?strong>(.+?)</span.*?venue-name\">(.+?)</span' # date link name room
        gigo_shows = r'id=\"event-listings.*?footer-container\">'
        aP = re.search(gigo_shows, page.text.replace('\n', '').replace('\r\t', ''))
        r = 1
    else:
        #new_shows= r'upcoming\".*?@type\":\"MusicEvent\".*?url\"\:\"([^\"].+?)\".*past\"'
        new_shows = r'upcoming\".*?past\"'
        aP = re.search(new_shows, sContent)
        r = 0

    if aP:
        aTourDates = re.finditer(pattern, aP.group(0))
        tDates = aTourDates
        # make list array
        cDates = list(tDates)
        lDates = len(cDates)
    else:
        aTourDates = None
        lDates = 0

    print("\n[*] Get and Show Results: (" + str(lDates) +")\n")
    #if args.debug:
        #print("Debug: " + str(aP))

    if lDates > 0:
        for dates in cDates:
            if r <= 0 or top3 == True:
                if args.debug:
                    print("\n[*] " + str(dates) + " -> " + str(dates.group(0)))
                link = dates.group(3)
                name = dates.group(2)
                date = dates.group(6)
                if date:
                    date = transform_date(date)
                room = re.sub(r'",".+?":"', ', ', dates.group(4))
            elif trRows != "" and top3 == False: 
                if args.debug:
                    print("\n[*] " + str(dates) + " -> " + str(dates.group(0)))
                link = skurl + dates.group(2)
                name = dates.group(3)
                date = dates.group(1)
                room = dates.group(4).replace('<a href="', '<a href="' + skurl)
                if date:
                    date = transform_date(date)
                #room = re.sub(r'",".+?":"', ', ', dates.group(4))


            COUNT+=1
            print("\n["+ str(COUNT) +".] Link " + link + " Name " + name + " Datum " + date + " Room " + room)

            #trRows += "\n"
            trRows += f"""<tr>
              <th scope="row"><a href="{link}"><img src="data:image/png;base64,{b64img}" style="height: 42px;margin-top: -6px;" alt="View on Web"></a></th>
              <td>{name}</td>
              <td>{date}</td>
              <td>{room}</td>
            </tr>
            """
    else:
        trRows += f"""<tr>
          <th scope="row"><a href="#"><img src="data:image/png;base64,{b64img}" style="height: 42px;margin-top: -6px;" alt="View on Web"></a></th>
          <td>No</td>
          <td>Shows</td>
          <td>yet...</td>
        </tr>
        """

    if r == 1 and top3 == False:
        if args.debug:
            print(f"\n\n[*] Debug trRows PAST:\n ------------------ \n\n{trRows}")
        return trRows.replace('sURL', sURL)
    elif r == 1 and top3 == True:
        if args.debug:
            print(f"\n\n[*] Debug trRows PAST:\n ------------------ \n\n{trRows}")
        trRows += f"""</tbody></table><br/></details><hr/>
        <br/>
          <h3>Past Shows - Gigography</a></h3>
        </p></br>
        <table class="table table-hover table-dark"><thead>
        <tr>
          <th scope="col">Web</th>
          <th scope="col">Name?</th>
          <th scope="col">Time?</th>
          <th scope="col">Where?</th>
        </tr>
        </thead><tbody>
        """
        return set_songkick(pattern, page, trRows.replace('sURL', sURL), False)
    else:
        if args.debug:
            print(f"\n\n[*] Debug trRows NEW:\n ------------------ \n\n{trRows}")
        trRows += f"""</tbody></table><br/><hr/>
        <br/>
        <details class="spoiler-details animated">
          <summary class="buybtn" style="color: rgb(255, 255, 255); border-style: dotted none; --darkreader-inline-color: #fffff8;" data-darkreader-inline-color="">Show last 3 Shows</summary>
          <h3>Past Shows - <a href="{skurl + sURL}">Show all past shows</a></h3>
        </p></br>
        <table class="table table-hover table-dark"><thead>
        <tr>
          <th scope="col">Web</th>
          <th scope="col">Name?</th>
          <th scope="col">Time?</th>
          <th scope="col">Where?</th>
        </tr>
        </thead><tbody>
        """
        return set_songkick(pattern, page, trRows, None, 0, True)




def set_spotify(mode, pattern, page, trRows="", aTourDates=None, COUNT=0):

    b64img = "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"

    if "spotify.com" in mode:
        #Cleanup breakslines:
        sContent = page.text.replace('\n', '').replace('\r\t', '')

        aTourDates = re.finditer(pattern, page.text)
        tDates = aTourDates
        # make list array
        cDates = list(tDates)
        lDates = len(cDates)
        print("\n[*] Get and Show Results: (" + str(lDates) +")\n")

        if args.debug:
            print("Debug: " + page.text + " - " + str(list(aTourDates)))

    if lDates > 0:
        for dates in cDates:
            if "spotify.com" in mode:
                link = dates.group(1)
                name = dates.group(2)
                date = dates.group(3)
                if date:
                    date = transform_date(date)
                room = dates.group(4)

            elif "other.com" in mode:
                link = dates.group(1)
                name = dates.group(3)
                date = dates.group(4)
                if date:
                    date = transform_date(date)
                room = dates.group(2)

            COUNT+=1
            print("["+ str(COUNT) +".] Link " + link + " Name " + name + " Datum " + date + " Room " + room)

            #trRows += "\n"
            trRows += f"""<tr>
              <th scope="row"><a href="{link}"><img src="data:image/png;base64,{b64img}" style="height: 42px;margin-top: -6px;" alt="View on Web"></a></th>
              <td>{name}</td>
              <td>{date}</td>
              <td>{room}</td>
            </tr>
            """
    else:
        trRows += f"""<tr>
          <th scope="row"><a href="#"><img src="data:image/png;base64,{b64img}" style="height: 42px;margin-top: -6px;" alt="View on Web"></a></th>
          <td>No</td>
          <td>Shows</td>
          <td>yet...</td>
        </tr>
        """

    return trRows



def write_to_tourhtml(HTMFILE, trRows):

    # Create an HTML template string with placeholders
    html_template = f"""
<link rel="stylesheet" href="/css/cwe-strap-cont.css">
<style>.table th, .table td {{padding: 0.55rem;}}</style>
<h1>TOUR/SHOWS</h1>
<br/>
<!--
<h3>No Shows at the moment</h3>
-->
<br/><br/>
<table class="table table-hover table-dark">
  <thead>
    <tr>
      <th scope="col">Web</th>
      <th scope="col">Name?</th>
      <th scope="col">Time?</th>
      <th scope="col">Where?</th>
    </tr>
  </thead>
  <tbody>
    {trRows}
  </tbody>
</table>
<p><br/><br/><br/><br/></p>
    """

    try:
        print(f"\n[*] Write html-TEXT to {HTMFILE} ...")
        #formatted_html = html_template.format(title, title, content)
        with open(HTMFILE, 'wt') as file:
            file.write(html_template + "\n")
        #DEBUG:
        #print(html_template)
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")



def transform_date(date_string):

    try:
        # Parse with timezone information if available
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        try:
            # Try without timezone information
            date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            # Fallback to date-only format
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
    
    # Format the datetime object into the desired output format
    formatted_date = date_object.strftime("%d.%m.%Y Doors: %I:%M %p")
    
    return formatted_date




def main():

    print("        ----------------------------------------- ")
    print("       |    tourGEN - Tourdate Generator v0.2    |")
    print("       |     by suuhm (C) 2023                   |")
    print("        --------------------------------------- \n")

    # VARS
    #
    URL = "https://open.spotify.com/artist/629ruWM6oJTLI5gODFYrwh/concerts"
    HTMFILE = "/var/www/tour.html"
    MAILADDR = "" # info@bandsite.local

    aTourDates = None
    trRows = ""
    # SUBPRCESS
    #
    # cmd = f"sd.py {args.filename} ..."
    # result subprocess.run(cmd, shell=True, captured_output=True, text=True)
    # lines = result.stdout.split("\n")


    # ARGS PARSER:
    parser = argparse.ArgumentParser(description='Download content from a URL and save it to a file.')

    parser.add_argument("--url", "-u", default=URL, required=False, help="URL to fetch data from")
    parser.add_argument("--export", "-f", default=HTMFILE, required=False, help="Name of the HTML file to save the data")
    parser.add_argument("--debug", "-d", default=None, action="store_true", required=False, help="Output debugging of site conntent")
    parser.add_argument("--mailsend", "-m", default=MAILADDR, required=False, help="Get a debugging mail")


    # PCHECK ARGS:
    global args
    args = parser.parse_args()

    if args.url:
        URL = args.url
    else:
        URL = URL
    if args.export:
        HTMFILE = args.export
    else:
        HTMFILE = HTMFILE

    # Perform the download and save operation
    try:
        page = requests.get(URL)
        stat = page.raise_for_status()

        print(f"\n[*] Downloaded content from {URL} and saved it to {HTMFILE} status: {stat}")

        # DEBUGGING:
        if args.debug:
            print(f"\n\n[*] Debug:\n ------------------ \n\n{stat}")
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")



    # GET CONTENT PER REGEX
    #
    # GET DOMAIN TO CHECK:
    parsed_url = urlparse(URL)
    domain = parsed_url.netloc

    if "spotify.com" in domain:
        print(f"\n[+] Using Regex scraping of '{domain}' ...")
        pattern = r'{\"@type\":\"MusicEven.*?\"\:\"([^\"]+).+?\:\"([^\"]+).+?\:\"([^\"]+).+?ad.*?ty.\:\"([^\"]+)' #link , name, date, room
        trRows = set_spotify(domain, pattern, page, trRows)

    elif "songkick.com" in domain:
        print(f"\n[+] Using Regex scraping of '{domain}' ...")
        pattern = r'mary-det.+?\>(.+?)\<.+?ail\"\>(.+?)\<.+?url\"\:\"([^\?]+).+?ad.+?ality\"\:\"([^\}].+?)\"\}.+?name\"\:\"([^\"]+).+?s.+?ate\"\:\"([^\"]+)' #room, name, link, room-adv, location, date
        trRows = set_songkick(pattern, page, trRows)

    else:
        print(f"\n[!] Cannot find domain {domain}...")
        pattern = r'{.*\"\:\"([^\"]+).+?\:\"([^\"]+).+?\:\"([^\"]+).*?ty.\:\"([^\"]+)'

    # DEBUGGING:
    if args.debug:
        print(f"\n\n[*] Debug trRows MAIN:\n ------------------ \n\n{trRows}")

    write_to_tourhtml(HTMFILE, trRows)

    if args.mailsend:
        # Get MAIL?
        sendmail(trRows, MAILADDR)


if __name__ == "__main__":
    main()
