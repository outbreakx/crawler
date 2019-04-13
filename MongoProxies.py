from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool
from UserAgents import UserAgents
import datetime,requests, re,sys, random, copy

from config import IP

class MongoProxies:
    def __init__(self,sites=None,headers=None):
        self.db = pymongo.MongoClient(IP).Main
        self.my_collection = self.db.Proxies
        self.proxyCount = 0
        self.proxyProgress = 0
        self.now = datetime.datetime.utcnow()
        self.sites = sites
        self.headers = headers
        self.user_agents = UserAgents()

    def scrappingProxies(self,onlyHttps=False):
        main_html = requests.get('https://free-proxy-list.net/')
        main_page = BeautifulSoup(main_html.content,'html.parser')
        table = main_page.table
        rows = table.tbody('tr')
        print(len(rows))
        for row in rows:
            tds = row('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            country = tds[3].text.strip()
            https = tds[6].text.strip()  
            if(https=='yes' or not onlyHttps):
                item_insert = {
                    'ip':ip,
                    'port':port,
                    'country':country,
                    'date':self.now,
                    'https':https,
                    'threadId':'none',
                }
                self.my_collection.find_one_and_update(
                    {'ip':ip},
                    {'$set':item_insert},
                    upsert=True
                )

    def getProxies(self,checked=True,onlyHttps=False):     
        https = 'yes' if onlyHttps else {'$regex':'^'}
        proxies = self.my_collection.find({'media':{'$exists':checked},'https':https})
        ips = []
        for proxy in proxies:
            ips.append('{}:{}'.format(proxy['ip'],proxy['port']))
        return ips

    
    def testProxies(self,threads):
        if self.sites == None:
            print('Adicione ao menos um site em dailyProxies.py')
            return
        self.my_collection.update({},{'$unset':{'speed':1}},multi=True)
        proxies = self.getProxies(checked=False)
        self.proxyCount = len(proxies)
        pool = ThreadPool(threads)
        pool.map(self.__testProxies,proxies)
        pool.close()
        pool.join()
        self.__delete_bad_proxy()


    def __testProxies(self,proxy):
        self.proxyProgress+=1
        self.__update_progress(self.proxyProgress/self.proxyCount,'Testando proxies...')
        make = []
        for site in self.sites:
            make.append([site,proxy])
        pool = ThreadPool(len(make))
        pool.map(self.__asyncRequests,make)
        pool.close()
        pool.join()
        

    def __asyncRequests(self,args):
        try:
            ip = args[1].split(':')[0]
            headers = copy.copy(self.headers)
            user_agent = self.user_agents.getRandomUserAgent()
            headers['user-agent'] = user_agent
            request = requests.get(args[0],proxies={'https':args[1]},timeout=15,headers=headers)
            speed = request.elapsed.total_seconds()*1000
            # print('Deu certo.')
            self.my_collection.find_one_and_update(
                {'ip':ip},
                {'$push':{'speed':speed}},
                upsert=False
            )
        except Exception as e:
            # print(e)
            self.my_collection.delete_one({'ip':ip})

    def __delete_bad_proxy(self):
        print('--- Delete Bad Proxy ---')
        proxies = self.my_collection.find({'media':{'$exists':False},'speed.0':{'$exists':True}})
        for proxy in proxies:
            media = float(sum(proxy['speed']))/len(proxy['speed'])
            if(media>5000):
                result = self.my_collection.delete_one({'_id':proxy['_id']})
                #print(f"Deleted {proxy['ip']} - {'https' if proxy['https']=='yes' else 'http'}")
                print("Deleted {} - {}".format(proxy['ip'], 'https' if proxy['https']=='yes' else 'http'))
            else:
                self.my_collection.find_one_and_update(
                    {'ip':proxy['ip']},
                    {'$set':{'media':media}},
                    upsert=False
                )

    def getProxy(self,url):
        proxies = self.getProxies(onlyHttps=url.startswith('https',end=5))
        for proxy in proxies:
            try:
                requests.get(url,proxies={'https':proxy},timeout=10)
                print('good proxy: {}'.format(proxy))
                #print(f'good proxy: {proxy}')
                return proxy
            except:
                print('bad proxy: {}'.format(proxy))               
                continue

    def getRandomProxy(self):
        document_cursor = self.my_collection.aggregate([
            { '$match' : 
                {
                    'https':'no',
                    'country': 'Brazil',
                }
            },
            {'$sample' :
                {'size' : 1}
            }
        ])
        document = document_cursor.next()
        ip = document['ip']
        port = document['port']       
        return '{}:{}'.format(ip,port)

    def deleteProxy(self,full_ip):
        ip = full_ip.split(':')[0]
        self.my_collection.delete_one({'ip':ip})

    def __update_progress(self,progress,message):
        length = 30
        block = int(round(length*progress))
        msg = "\r{0}: [{1}] {2}%".format(message, "#"*block + "-"*(length-block), round(progress*100, 2))
        if progress >= 1: 
            msg += " FINISH\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()