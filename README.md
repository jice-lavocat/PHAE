PHAE - Python HTML Authorship Extraction
========================================

Intro
-----

PHAE is a Google+ authorship extraction tool written in Python. It is extracting authorship information
from html pages based on the [Google+ authorship tag](https://support.google.com/webmasters/answer/2539557?hl=en) .

It is supposed to return similar result as the Structured Data Testing Tool 
( [SDTT](http://www.google.com/webmasters/tools/richsnippets) ) provided by Google.

The script can follow rel="author" and rel="me" links in a recursive way until it finds a link to a Google+
user page. It returns the name and link to Google+ profile of the author.


Tutorial
--------

At the moment, we do not provide an installation package. To install Phae, just git clone this repository:

    git clone git@github.com:tanzaho/PHAE.git
    
You need to install some dependencies   using ip :

    cd PHAE
    pip install -r requirements.txt
    
The script needs a public Google API token to access author information. Get one at the [Google API Console](https://console.developers.google.com/). You can then either place this token in the `settings.py` file or 
use it as a parameter when calling the script.

To get the authorship information from a given url :
    
    from PHAE import phae
    
    # Either use the token from `settings.py` or use it as an (optional) parameter
    g_token = "your_token_123456789"
    phae = Phae(google_token=g_token)
    
    # Define the url you want to analyze
    url = "http://blog.elokenz.com/features/wordpress_widget"
    
    try:
        author = phae.get_author(url)
        print author['first_name']
        print author['family_name']
        print author['google_plus_profile']
    except:
        print "No correct author found"



Todo
----
* Write custom exceptions and return the correct one when needed
* Write tests
* Write a longer documentation
* Create an installer
