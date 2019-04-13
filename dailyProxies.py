from MongoProxies import MongoProxies
import time,sys


sites = [
    'https://www.zapimoveis.com.br/',
]

proxies = MongoProxies(sites=sites,headers={
    'authority': 'https://www.zapimoveis.com.br/',
    'method': 'GET',
    'scheme': 'https',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,la;q=0.8',
    'upgrade-insecure-requests': '1'
})

threads = int(input()) if len(sys.argv)<=1 else int(sys.argv[1])
proxies.scrappingProxies()
proxies.testProxies(threads)