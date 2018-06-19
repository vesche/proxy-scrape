# proxy-scrape

*The TorVPN proxy list is no longer populating as of July 2018, therefore this tool is defunct. If you're looking for a decent free proxy list, check out [a2u/free-proxy-list](https://github.com/a2u/free-proxy-list).*

This is a command-line tool to scrape the [TorVPN proxy list](https://www.torvpn.com/en/proxy-list) for use with [proxychains](https://github.com/haad/proxychains). TorVPN's proxy list uses images to list IP addresses (likely to avoid scrapers), this tool uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via the [pytesseract](https://github.com/madmaze/pytesseract) wrapper for [optical character recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) and [ImageMagick](https://www.imagemagick.org/script/index.php) for image manipulation.

## Install

```
$ sudo apt-get install proxychains tesseract-ocr imagemagick
$ git clone https://github.com/vesche/proxy-scrape
```

## Usage

Run proxy-scrape like so, be patient it will take about 30 seconds to process:

```
$ ./proxy-scrape.py
http 33.169.33.46    3128  # Germany
http 158.69.204.32   3128  # United States
http 139.59.117.11   3128  # Australia
http 128.199.66.186  443   # United Kingdom
http 139.59.125.12   8080  # Australia
http 128.199.190.243 443   # United Kingdom
http 139.59.125.12   80    # Australia
http 128.199.75.57   8080  # United Kingdom
http 14.141.73.11    8080  # India
http 138.197.137.90  3128  # United States
http 35.185.80.76    3128  # United States
http 143.107.228.57  3128  # Brazil
http 188.166.82.80   3000  # Russian Federation
...
```

You can easily append the results of proxy-scrape to proxychains. Some proxies may by denied or timeout, just remove these manually. Here I do a simple curl, and use my tool [scanless](https://github.com/vesche/scanless) using many proxies:

```
$ ./proxy-scrape.py > results.txt
$ head -n 20 results.txt | sudo tee -a /etc/proxychains.conf > /dev/null
$ proxychains curl https://ipinfo.io/8.8.8.8
ProxyChains-3.1 (http://proxychains.sf.net)
|D-chain|-<>-158.69.204.32:3128-<>-139.59.117.11:3128-<>-128.199.66.186:443-<>-139.59.125.53:443-<>-139.59.125.12:8080-<>-128.199.75.57:80-<>-128.199.190.243:443-<>-139.59.125.12:80-<>-128.199.75.57:8080-<>-138.197.137.90:3128-<>-35.185.80.76:3128-<>-143.107.228.57:3128-<><>-216.239.36.21:443-<><>-OK
{
  "ip": "8.8.8.8",
  "hostname": "google-public-dns-a.google.com",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.3860,-122.0840",
  "org": "AS15169 Google Inc.",
  "postal": "94035",
  "phone": "650"
}
$ proxychains scanless -t scanme.nmap.org -s hackertarget
ProxyChains-3.1 (http://proxychains.sf.net)
Running scanless...
|D-chain|-<>-158.69.204.32:3128-<>-139.59.117.11:3128-<>-128.199.66.186:443-<>-139.59.125.53:443-<>-139.59.125.12:8080-<>-128.199.75.57:80-<>-128.199.190.243:443-<>-139.59.125.12:80-<>-128.199.75.57:8080-<>-138.197.137.90:3128-<>-35.185.80.76:3128-<>-143.107.228.57:3128-<><>-35.186.165.146:443-<><>-OK

------- hackertarget -------
Starting Nmap 7.01 ( https://nmap.org ) at 2017-09-25 14:42 UTC
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.063s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
PORT     STATE  SERVICE       VERSION
21/tcp   closed ftp
22/tcp   open   ssh           OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8 (Ubuntu Linux; protocol 2.0)
23/tcp   closed telnet
25/tcp   closed smtp
80/tcp   open   http          Apache httpd 2.4.7 ((Ubuntu))
110/tcp  closed pop3
143/tcp  closed imap
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.18 seconds
----------------------------
```

## Notes
If you're having DNS issues remove `proxy_dns` from your `/etc/proxychains.conf` to do DNS resolution locally. I'd recommend using a DNS server from [OpenNIC](https://servers.opennic.org/) in your `/etc/resolv.conf`.


