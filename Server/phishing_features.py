from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import whois
import requests
from datetime import datetime
import ipaddress

# Listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                       r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                       r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                       r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                       r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                       r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                       r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                       r"tr\.im|link\.zip\.net"

# Revised `web_traffic` function:
def web_traffic(url):
    """
    Retrieves Alexa website traffic rank for a given URL.

    Args:
        url (str): The URL to get the traffic rank for.

    Returns:
        int: The Alexa website traffic rank, or 1 if unable to retrieve.

    Raises:
        requests.exceptions.RequestException: If HTTP request fails.
    """

    try:
        url = urlparse(url).netloc  # Extract only the domain part
        # Construct a more consistent and relevant Alexa URL
        response = requests.get(f"https://data.alexa.com/data?cli=10&dat=s&url={url}")
        response.raise_for_status()  # Raise an exception for non-200 status codes
        rank = BeautifulSoup(response.content, "xml").find("REACH")["RANK"]
        return int(rank)
    except (requests.exceptions.RequestException, TypeError):
        return 1  # Return 1 as a neutral value if unable to retrieve rank

# Function to check if URL is an IP address
def isIPAddress(url):
    try:
        ipaddress.ip_address(url)
        return True
    except ValueError:
        return False

# IFrame Redirection function
def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1

# Mouse Over function
def mouseOver(response): 
    if response == "" :
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0

# Right Click function
def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1

# Forwarding function
def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

# Feature extraction function:
def featureExtraction(url):

    features = []

    # Address bar based features (10)
    features.append(int(isIPAddress(url)))  # Handle IP addresses gracefully
    features.append(1 if "@" in url else 0)
    features.append(1 if len(url) < 54 else 0)
    features.append(len(urlparse(url).path.split('/')) - 1)  # Correct depth calculation
    features.append(1 if url.rfind('//') > 6 else 0)
    features.append(1 if 'https' in urlparse(url).netloc else 0)
    features.append(1 if re.search(shortening_services, url) else 0)  # Use shortening_services variable
    features.append(1 if '-' in urlparse(url).netloc else 0)

    # Domain based features (4)
    dns = 0
    try:
        domain_name = whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainEnd(domain_name))
  
    # HTML & Javascript based features (4)
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
  
    return features