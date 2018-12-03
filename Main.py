import json, os, jinja2, random, urllib2, webapp2


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib2.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def getYoga():
    #choose a random yoga pose and store it's names and image
    choose = random.sample(range(0, 34), 3)
    yoga = json.load(open('yogaJSON.txt', 'r'))
    posedata = {}
    for p in choose:
        posedata[p] = {}
        posedata[p]['s_name'] = yoga[p]['sanskrit_name']
        posedata[p]['e_name'] = yoga[p]['english_name']
        posedata[p]['image'] = yoga[p]['img_url']
    return posedata

    # get birthday info from user input on html page and translate to a sunsign and pass it in as a parameter
def horoREST(sunsign):
    #get the horoscope for today
    baseURL = 'http://horoscope-api.herokuapp.com/horoscope/today/'
    horodata = safeGet(baseURL +sunsign)
    return json.load(horodata)

def quoteREST():
    url = 'http://quotes.rest/qod.json?category=inspire&api_key=d9jh_OCJD0Z0zWNnOVhIpAeF'
    quotedata = safeGet(url).read()
    quotejson = json.loads(quotedata)
    # quote = {}
    # quote['quote'] = quotejson['contents']['quotes'][0]['quote']
    # quote['author'] = quotejson['contents']['quotes'][0].get('author','anonymous')
    quote =[]
    quote.append('"' + quotejson['contents']['quotes'][0]['quote'] + '"')
    quote.append('-' + quotejson['contents']['quotes'][0].get('author','anonymous'))
    return quote

# TESTING ==>
# print('testing getYoga...')
# print(getYoga())
#
# print('testing horoREST...')
# print(pretty(horoREST('aquarius')))
#
# print('testing quoteREST...')
# print(quoteREST())

maindict = {}
maindict['yogadata'] = getYoga()
maindict['quotedata'] = quoteREST()

# sends to choose-vibe.html
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('choose-vibe.html')
        self.response.write(template.render(maindict))

# sends to home-template.html with choosen vibe
class VibeResponseHandler(webapp2.RequestHandler):
    # vibe names:
    # peachy
    # bright_sky
    # spring_green
    # purple_rain
    def post(self):
        vibe_choice = self.request.get('vibe_choice')

        if vibe_choice == 'peachy':
            template = JINJA_ENVIRONMENT.get_template('home-template.html')
            self.response.write(template.render(maindict))
        elif vibe_choice == 'bright_sky':
            template = JINJA_ENVIRONMENT.get_template('home-template.html')
            self.response.write(template.render(maindict))
        elif vibe_choice == 'spring_green':
            template = JINJA_ENVIRONMENT.get_template('home-template.html')
            self.response.write(template.render(maindict))
        else:
            template = JINJA_ENVIRONMENT.get_template('home-template.html')
            self.response.write(template.render(maindict))


application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)

# Determines the zodiac sign based on the user input 
# from the horoscope birthday request
def getZodiac(birthday):
    zodiac = ""
    if (birthday >= '3-21' and  birthday <= '4-19'):
        zodiac='aries'
    elif (birthday >= '4-20' and birthday <= '5-20'):
        zodiac='taurus'
    elif (birthday >= '5-21' and birthday <= '6-20'):
        zodiac='gemini'
    elif (birthday >= '6-21' and birthday <= '7-22'):
        zodiac='cancer'
    elif (birthday >= '7-23' and birthday <= '8-22'):
        zodiac='leo'
    elif (birthday >= '8-23' and birthday <= '9-22'):
        zodiac='virgo'
    elif (birthday >= '9-23' and birthday <= '10-22'):
        zodiac='libra'
    elif (birthday >= '10-23' and birthday <= '11-21'):
        zodiac='scorpio'
    elif (birthday >= '11-22' and birthday <= '12-21'):
        zodiac='sagittarius'
    elif (birthday >= '12-22' and birthday <= '1-19'):
        zodiac='capricorn'
    elif (birthday >= '1-20' and birthday <= '2-18'):
        zodiac='aquarius'
    else:
        zodiac = 'pisces'
    return zodiac


# <!-- 
#     Aries (March 21- April 19)
#     Taurus (April 20 - May 20)
#     Gemini (May 21 - June 20)
#     Cancer (June 21 - July 22)
#     Leo (July 23 - August 22)
#     Virgo (August 23 - September 22)
#     Libra (September 23 - October 22)
#     Scorpio (October 23 - November 21)
#     Sagittarius (November 22 - December 21)
#     Capricorn (December 22 - January 19)
#     Aquarius (January 20 - February 18)
#     Pisces (February 19 - March 20)
#  -->