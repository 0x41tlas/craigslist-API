import requests
import bs4

class search:

    def __init__(self, city, fld, inq):

        self.city = city
        self.inq = inq
        self.fld = fld
        self.items = []

        self.citylist = ('https://www.craigslist.org/about/sites')

        self.proxies = {'https': 'https://83.18.150.54:3128atom text '}

        # For debugging and logs
        self.Flog = open('log.txt', 'w')
        self.Fresults = open('report.txt', 'w')
        self.Fdupe = open('dupes.txt', 'w')


    def bsoup(self, data):
        return bs4.BeautifulSoup(data.text, 'lxml')

    def request(self, req):
        res = requests.get(req, proxies=self.proxies)
        res.raise_for_status
        soup = self.bsoup(res)
        return soup

    def log(self, l):
        self.Flog.write(str(l))

    def logjobs(self, j):
        self.Fresults.write(str(j))

    def logdupes(self, d):
        self.Fdupe.write(str(d))

    def search(self, name, c):
        try:
            print('[*]          Working...')
            url = ('{}search/{}?query={}&is_paid=all'.format(c, self.fld, self.inq.replace(" ", "+")))
            soup = self.request(url)

            print('      [#]    Success: {}'.format(name))
            self.log("Request sucessful: {}".format(url))
            self.log('\n')

            for ul in soup.select('.rows li'):
                for fin in ul.select('a.result-title'):
                    href = fin['href'].split('/')
                    href = "/".join(href[:6])
                    print href
                    if (href in self.items):
                        print('************ Duplicate')
                        self.logdupes("City: {}{}".format(name.title(), '\n'))
                        self.logdupes("Title: {}{}".format(fin.text, '\n'))
                        self.logdupes("Link: {}{}".format(fin['href'], '\n'))
                        self.logdupes("\n")
                    else:
                        print('         [#] Found')
                        self.logjobs("City: {}{}".format(name.title(), '\n'))
                        self.logjobs("Title: {}{}".format(fin.text, '\n'))
                        self.logjobs("Link: {}{}".format(fin['href'], '\n'))
                        self.logjobs("\n")

                        self.items.append(href)


        except Exception as e:
            print('   [!]       Error: {}'.format(str(e)))
            self.log(e)
            self.log('\n')

    def citysearch(self):
        citylist = {}

        soup = self.request(self.citylist)

        fin = soup('div')[3]
        for a in fin.select('a'):
            citylist[a.text] = a['href']

        print("[*] Found cities...")

        for c in citylist:
            self.search(c, citylist[c])

    def main(self):
        if self.city.lower() == ('all'):
            self.citysearch()
        else:
            print("Done")

def printhelp():
    print("""

CraigsList web scraper by Atlas
GitHub @AtlasMerc

Common item expressions:

Computers:
    ela - electronics
    sya - computers by all
    syd - computers by dealer
    sys - computers by owner
    syp - parts by all
    sop - parts by owner
    sdp - parts by dealer

Gigs:
    cpg - computer gigs
    crg - creative gigs
    tlg - talent gigs

Jobs:
    sof - software jobs

Hints:
    Put <all> in for the city to scan every capital city
    """)

printhelp()
city = raw_input("city:: ")
fld = raw_input("expression:: ")
inq = raw_input("search:: ")
print

search = search(city, fld, inq)
search.main()
