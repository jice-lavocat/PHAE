import settings
import requests
import json
#from urlparse import urlparse
import urlparse 
import lxml.html

class Phae(object):
    """
    Phae() will retrieve and/or analyze html pages to extract relevant author information
    """
    def __init__(self, google_token=None):
        self.google_token = google_token or settings['GOOGLE_API_TOKEN']
        
        
    def import_urls_from_google(self,user_id):
        """
        Imports the urls from a given user_id profile
        """
        params = {"key" : self.google_token}
        url_google = "https://www.googleapis.com/plus/v1/people/" + str(user_id)
        r = requests.get(url_google, params = params)
        # Json to dict
        user_json = json.loads(r.text)
        # User exists for Google ?
        if (user_json.get("error")):
            user_exists = False
            raise ValueError("User %s does not represent a valid Google+ account" % user_id)
        # Does the user have some urls in his/her profile
        try:
            urls = user_json["urls"]
            return urls
        except:
            raise ValueError("User has no URLs")
            
            
    def google_urls_to_domains(self, urls):
        """
        Transform the G+ urls dict into a set of domain
        """
        domain_list = []
        for url_info in urls:
            url = url_info["value"]
            parsed_uri = urlparse.urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            domain_list.append(domain)
        return set(domain_list)
        
    def extract_schema_author(self, html_tree):
        """
        Returns author url contained in itemprop author
         <span itemprop=author><a title="Jean-Christophe Lavocat" href="/news/contributeurs/jice-lavocat" rel = "author">Jean-Christophe Lavocat</a></span>
        """
        return True
        
        
    def extract_relauthor_url(self, url_requested_page, raw_html = None):
        """
        Extract the rel=author url from a given page or from raw_html
        """
        if raw_html:
            raw_html_tree =  lxml.html.fromstring(raw_html)
        else :
            r = requests.get(url_requested_page)
            raw_html_tree =  lxml.html.fromstring(r.text)
            
        # Now that we have the html tree, we look for variations of author tag
        # In order rel="author" then rel="me"
        list_author_urls = raw_html_tree.xpath('//a[@rel="author"]/@href')
        list_author_urls += raw_html_tree.xpath("//a[@rel='me']/@href")
        # We then select only the first link found
        if len(list_author_urls)>0:
            first_author_url_rel = list_author_urls[0]
            first_author_url_absolute = urlparse.urljoin(url_requested_page,first_author_url_rel)
            return first_author_url_absolute
        else:
            raise BaseException("No author tag was found")
        
    def find_google_profile(self, visited_urls):
        """
        Returns the final google profile if it exists
        """
        last_url = visited_urls[-1]
        if (("plus.google.com" in last_url) or ("profiles.google.com" in last_url)) :
            return last_url
        else:
            # visit the last page and check for author profile
            new_url = self.extract_relauthor_url(last_url)
            if new_url in visited_urls:
                # if the new url was already visited, then stop the recursion
                raise BaseException("There is a link to an author profile, but none goes to Google+")
            else:
                visited_urls += [new_url]
                return self.find_google_profile(visited_urls)
