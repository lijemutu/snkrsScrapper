from bs4 import BeautifulSoup
import re
import json
from scraper_api import ScraperAPIClient
import time

class snkrs:
    def __init__(self) -> None:
        self.products = {}
    def getInfoInnvictus(self,apiKey='aba275ef5f8f713e086a1a0ab240dd5c'):
        """ Method to retrieve a dict given launching shoes on innvictus.com/lanzamientos """

        self.client = ScraperAPIClient(apiKey)
    
        result = self.client.get(url = 'https://www.innvictus.com/lanzamientos')
        assert result.status_code == 200, f"Status code {result.status_code}"
        
        soup = BeautifulSoup(result.content,'html.parser')
        links = soup.find('body').find_all("script",attrs={'type':'text/javascript'})
        s = links[3] # links[3] element gives var products 
        productVar = re.search(r'\'(.*?)\'', str(s))
        productDict = json.loads(productVar.group(0).replace("'{\"id","[{\"id").replace("\"}'","\"}]"))
        #print(productVar.group(0).replace("'{\"id","[{\"id").replace("\"}'","\"}]"))

      
        for tenis in productDict:
            tenis['url'] = "https://www.innvictus.com/p/{id}" .format(id=tenis['id'])
        self.products = productDict
    def selectSaveTargetShoes(self,save=False):
        i=0
        for shoes in self.products:
            print(f"Selelction {i}")
            print("Shoe: ",shoes['name2'])
            print("Launching date: ",shoes['realdate'])
            print("Price: ",shoes['price'],"\n")
            i+=1
        selectedShoe = [int(x) for x in input("Select shoe number to track\n").split()]
        #print(selectedShoe)
        def takeFromDict(dct, listElements):
            return [dct[element] for element in listElements]
        self.products = takeFromDict(self.products,selectedShoe)
        if save==True:
            with open('TargetShoes.txt','w') as f:
                for shoe in self.products:
                    f.write(shoe['url'])
                    f.write("\n")
    def isAvailable(self,fileName=None):
        def sendDiscordMessage(self,message='Hello world'):
            from discord import Webhook, RequestsWebhookAdapter
            webhook = Webhook.from_url("https://discord.com/api/webhooks/811294684386426890/3SY7GtmBAwyjDM6qr73eDRqrzjRJZ2u0vlShoyOvvf_cCUNvv6YJqiGPI1udVWWqipVp", adapter=RequestsWebhookAdapter())
            webhook.send(message)

        
        if fileName==None:
            for url in self.products:
                notAvailable = self.client.get(url['url'])
                assert notAvailable.status_code == 200, f"Status code {notAvailable.status_code}"
                soupNotAvailable = BeautifulSoup(notAvailable.content,'html.parser')
                try:
                    notFoundClass = soupNotAvailable.find('body').find("div",attrs={'class':'pdp-notFound'}).text.strip()
                    notFoundTitle = soupNotAvailable.find('title').text.strip()
                except:
                    notFoundClass = ''
                    notFoundTitle = ''
                if "No encontrado" in notFoundTitle or "Este producto no" in notFoundClass:
                    url['Available'] = False
                    message = url['name2'], " no disponible aun"
                    print(message)
                    return False
                    
                else:
                    message = url['name2'], " disponible",url['url']
                    print(message)
                    url['Available'] = True
                    sendDiscordMessage(self,message=message)
                    return True
        else:
            with open(fileName,'r') as targetShoes:
                urls = [url.strip() for url in targetShoes]
                for url in urls:
                    notAvailable = self.client.get(url,headers=self.headers)
                    soupNotAvailable = BeautifulSoup(notAvailable.content,'html.parser')
                    try:
                        notFoundClass = soupNotAvailable.find('body').find("div",attrs={'class':'pdp-notFound'}).text.strip()
                        notFoundTitle = soupNotAvailable.find('title').text.strip()
                    except:
                        notFoundClass = ''
                        notFoundTitle = ''
                    if "No encontrado" in notFoundTitle or "Este producto no" in notFoundClass:
                        print(url, " no disponible aun\n")
                    else:
                        print(url, " disponible \n")
                        

innvictusShoesLaunching = snkrs()



innvictusShoesLaunching.getInfoInnvictus()
innvictusShoesLaunching.selectSaveTargetShoes(save=True)
i = 0
while True:
    start_time = time.time()
    success = innvictusShoesLaunching.isAvailable()
    if (time.time() - start_time)<5:
        time.sleep(3)
    if success == True or i==930:
        break
    i+=1
    
    #print("--- %s seconds ---" % (time.time() - start_time))
