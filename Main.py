import json, os, jinja2, random, urllib2, webapp2

# https://hcde-310-final-project-223101.appspot.com/

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
    choose = random.sample(range(0, 36), 3)
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

def getZodiac(birthday):
    zodiac = ""
    if (birthday >= 321 and  birthday <= 419):
        zodiac='Aries'
    elif (birthday >= 420 and birthday <= 520):
        zodiac='Taurus'
    elif (birthday >= 521 and birthday <= 620):
        zodiac='Gemini'
    elif (birthday >= 621 and birthday <= 722):
        zodiac='Cancer'
    elif (birthday >= 723 and birthday <= 822):
        zodiac='Leo'
    elif (birthday >= 823 and birthday <= 922):
        zodiac='Virgo'
    elif (birthday >= 923 and birthday <= 1022):
        zodiac='Libra'
    elif (birthday >= 1023 and birthday <= 1121):
        zodiac= 'Scorpio'
    elif (birthday >= 1122 and birthday <= 1221):
        zodiac='Sagittarius'
    elif (birthday >= 1222 and birthday <= 119):
        zodiac='Capricorn'
    elif (birthday >= 120 and birthday <= 218):
        zodiac='Aquarius'
    else:
        zodiac = 'Pisces'
    return zodiac

# TESTING ==>
# print('testing getYoga...')
# print(getYoga())

print('testing horoREST...')
print(pretty(horoREST('libra')))
print(getZodiac(1012))

# print('testing quoteREST...')
# print(quoteREST())

# maindict = {}
# maindict['yogadata'] = getYoga()
# maindict['quotedata'] = quoteREST()

# sends to choose-vibe.html
class MainHandler(webapp2.RequestHandler):
    def get(self):
        maindict = {}
        # template = JINJA_ENVIRONMENT.get_template('choose-vibe.html')
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



        maindict = {}
        maindict['yogadata'] = getYoga()
        maindict['quotedata'] = quoteREST()

        if vibe_choice == 'peachy keen':
            template = JINJA_ENVIRONMENT.get_template('home-template1.html')
            self.response.write(template.render(maindict))
        elif vibe_choice == 'bright sky':
            template = JINJA_ENVIRONMENT.get_template('home-template2.html')
            self.response.write(template.render(maindict))
        elif vibe_choice == 'spring green':
            template = JINJA_ENVIRONMENT.get_template('home-template3.html')
            self.response.write(template.render(maindict))
        else:
            template = JINJA_ENVIRONMENT.get_template('home-template4.html')
            self.response.write(template.render(maindict))


class horoResponseHandler(webapp2.RequestHandler):
    def get(self):
        maindict={}
        month = self.request.get('month')
        day =  self.request.get('day')
        if len(day) == 1:
            day = '0' + day
        sign = getZodiac(int(month + day))
        maindict['sign']=sign
        result= horoREST(sign)
        maindict['horoscope']=result['horoscope']

        template = JINJA_ENVIRONMENT.get_template('horoscope.html')
        self.response.write(template.render(maindict))

        # sunsign = getZodiac(DOB)


    # signs = {'aries': '../api-project/images/aries.svg','taurus':'/..api-project/images/taurus.svg','gemini':'/..api-project/images/gemini.svg','cancer':'/..api-project/images/cancer.svg',
            #  'leo':'/..api-project/images/leo.svg','virgo':'/..api-project/images/virgo.svg','libra':'/..api-project/images/libra.svg','scorpio':'/..api-project/images/scorpio.svg',
            #  'sagittarius':'/..api-project/images/sagittarius.svg','capricorn':'/..api-project/images/capricorn.svg','aquarius':'/..api-project/images/aquarius.svg','pisces': '/..api-project/images/pisces.svg'}
    # print(signs)

    # Determines the zodiac sign based on the user input 
    # from the horoscope birthday request


application = webapp2.WSGIApplication([\
                                      ('/vibehome', VibeResponseHandler),
                                      ('/result', horoResponseHandler),
                                      ('/.*', MainHandler),
                                      ],
                                      debug=True)

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