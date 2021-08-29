import sys,os,bs4,webbrowser,requests,logging,re,openpyxl,smtplib

chromeExePath='Update the full chrome executable path'
sourceExcelPath=(str(os.getcwd())+'\SourceExcel.xlsx')
AvailableURL=[]



def flipkartAvailable(url,AvailableURL):
    AvailableURL=AvailableURL
    resultBody=""
    resultBody=resultBody+('FlipKart check')
    availSelector='#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(3) > div'
    comingsoonSelector='#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(3) > div'
    # coming soon - container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(3) > div
    soldoutSelector='#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(3) > div'

    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromeExePath))
    res=requests.get(url)
    res.raise_for_status()

    #logging.basicConfig((logging.info,'Status is : '+str(res.status_code)))
    soup=bs4.BeautifulSoup(res.text,'html.parser')

    elements = soup.select(availSelector)

    element2= soup.select(comingsoonSelector)
    element3=soup.select(soldoutSelector)

    RO1=re.compile(r'Currently Unavailable')
    RO2=re.compile(r'Coming Soon')
    RO3=re.compile(r'Sold Out')
    
    MO1=RO1.findall((elements[0]).text.strip())
    MO2=RO2.findall((element2[0]).text.strip())
    MO3=RO3.findall((element3[0]).text.strip())
    
    resultBody=resultBody+"""
"""+str(MO1)
    resultBody=resultBody+"""
"""+str(MO2)
    resultBody=resultBody+"""
"""+str(MO3)

    if len(MO1)==0:
        resultBody=resultBody+"""
"""+('empty string for Currently Unavailable')
        if len(MO2)==0:
            resultBody=resultBody+"""
"""+('empty string for Coming soon')
            if len(MO3)==0:
                resultBody=resultBody+"""
"""+('empty string for Sold Out')
            else: resultBody=resultBody+"""
"""+('Product Sold Out')
        else:resultBody=resultBody+"""
"""+('Product Coming soon')
    else: resultBody=resultBody+"""
"""+('product unavailable')
    if len(MO1)==0 and len(MO2)==0 and len(MO3)==0:
        resultBody=resultBody+"""
"""+('Product Available')
        AvailableURL.append('---- FLIPKART URL ---->')
        AvailableURL.append(url)

    return(resultBody)

def AmazonAvailable(url,AvailableURL):
    AvailableURL=AvailableURL
    status=''
    headers={
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Referer": "https://www.google.com/",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9"
}
    resultBody=''
    resultBody=resultBody+"""
"""+('Amazon Check')
    instockSelector='#availability > span' 

    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromeExePath))
    res=requests.get(url,headers=headers)
    try:
        res.raise_for_status()
    except:
        status='Either Product with url : '+url+' is unavailable or url is disabled.'

    #logging.basicConfig((logging.info,'Status is : '+str(res.status_code)))
    soup=bs4.BeautifulSoup(res.text,'html.parser')

    element1 = soup.select(instockSelector)
    

    if len(element1)==0:
        
        resultBody=resultBody+"""
"""+('In Stock Option Unavailable')
    else:

        RO=re.compile(r'In stock.')
        RO2=re.compile(r'Currently unavailable.')
        
        MO=RO.findall((element1[0]).text.strip())
        MO2=RO2.findall((element1[0]).text.strip())
        
        resultBody=resultBody+"""
"""+('Amazon check : '+str(MO))


        if len(MO)==0 and len(MO2)==0:
            resultBody=resultBody+"""
"""+('Product not in stock in Amazon.')
        elif len(MO2)>0:
            #print("elif check")
            resultBody=resultBody+"""
"""+('Product not in stock in Amazon')

        else:
            #print('else check')
            resultBody=resultBody+"""
"""+('Product in stock, Check the website')
            AvailableURL.append('---- AMAZON URL ---->')
            AvailableURL.append(url)

    return(resultBody)

    
def gamesTheShopAvailable(url,AvailableURL):
    AvailableURL=AvailableURL
    resultBody=''
    resultBody=resultBody+"""
"""+('GameShop Check')
    availSelector='#ctl00_ContentPlaceHolder1_divOfferDetails > div > div.offr-mne > div:nth-child(2) > div.addToCart-nw.addToCart-nw-dv.bo.errorherebg-blu'

    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromeExePath))
    res=requests.get(url)
    res.raise_for_status()

    soup=bs4.BeautifulSoup(res.text,'html.parser')

    elements = soup.select(availSelector)
    

    if len(elements)==0:
        resultBody=resultBody+"""
"""+('Product Unavailable to add at GameShop')
    else:

        RO=re.compile(r'ADD TO CART')
        MO=RO.findall((elements[0]).text.strip())
        resultBody=resultBody+"""
"""+('gamesShop : '+str(MO))

        if len(MO)==0:
            resultBody=resultBody+"""
"""+('Product Uavailable to add at GameShop')
        else: resultBody=resultBody+"""
"""+('product available to add at GameShop')
        AvailableURL.append('---- GAMES The SHOP URL ---->')
        AvailableURL.append(url)

    return(resultBody)


def cromaAvailable(url):
    print('Croma Check')
    availSelector='#add_to_cart_footer_container > div > div > div.p-full.floating_btn_panel > div'

    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromeExePath))
    res=requests.get(url)
    res.raise_for_status()

    soup=bs4.BeautifulSoup(res.text,'html.parser')

    elements = soup.select(availSelector)
    print(elements)
    if len(elements)==0:
        print('some issue with add to cart selector')
    else:

        RO=re.compile(r'disable-btn-in-pdp')
        MO=RO.findall((elements[0]).text.strip())
        print('gamesShop : '+str(MO))

        if len(MO)==0:
            print('Product Uavailable to add at Croma')
        else: print('product available to add at Croma')


def RelianceDigitalAvailable(url,AvailableURL):
    AvailableURL=AvailableURL
    resultBody=''
    resultBody=resultBody+"""
"""+('Reliance Digital Check')
    addToCartSelector='#add_to_cart_main_btn > span'

    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromeExePath))
    res=requests.get(url)
    res.raise_for_status()

    soup=bs4.BeautifulSoup(res.text,'html.parser')

    element1 = soup.select(addToCartSelector)
    

    if len(element1)==0:
        resultBody=resultBody+"""
"""+('Add To Cart Option Unavailable')
    else:

        RO=re.compile(r'ADD TO CART')
        MO=RO.findall((element1[0]).text.strip())
        resultBody=resultBody+"""
"""+('Reliance Digital : '+str(MO))

        if len(MO)==0:
            resultBody=resultBody+"""
"""+('Product Uavailable to add at Reliance Digital')
        else: resultBody=resultBody+"""
"""+('Add To Cart Option Available, Check the website')
        AvailableURL.append('---- RELIANCE DIGITAL URL ---->')
        AvailableURL.append(url)

    return(resultBody)

def MailResult(mailBody):
    fromID='yourOutlookMailID@outlook.com'
    receiversID=['ReceiversID@gmail.com']
    smtpObj=smtplib.SMTP('smtp-mail.outlook.com',587)
    smtpObj.ehlo()
    smtpObj.starttls() 
    smtpObj.login('yourOutlookMailID@outlook.com','PasswordText')
    finalbody="""Subject: Product Availability check.

"""+mailBody
    for eid in receiversID:
        toID=eid
        smtpObj.sendmail(fromID,toID,finalbody)
    smtpObj.quit()





def getDataFromExcelSource(sourceExcelPath,AvailableURL):
    
    workbookObj=openpyxl.load_workbook(sourceExcelPath)
    sheetObj=workbookObj['Sheet1']
    list2=sheetObj.iter_rows()
    fkBody=""

    for i,row_cells in enumerate(list2):
        if i == 0:
            continue
        for cell in row_cells:
            fkBody=fkBody+("""

"""+'URL under check : '+str(cell.value))
            
            FKRO=re.compile(r'flipkart.com')
            GSRO=re.compile(r'gamestheshop.com')
            RDRO=re.compile(r'reliancedigital.in')
            AMRO=re.compile(r'www.amazon')

            FKMO=FKRO.findall(str(cell.value))
            GSMO=GSRO.findall(str(cell.value))
            RDMO=RDRO.findall(str(cell.value))
            AMMO=AMRO.findall(str(cell.value))

            if len(FKMO)>0:
                fkBody=fkBody+"""
"""+str(flipkartAvailable(str(cell.value),AvailableURL))
                #print('----------------------')
                
            elif len(AMMO)>0:
                fkBody=fkBody+"""
"""+AmazonAvailable(str(cell.value),AvailableURL)
                #print('----------------------')

            elif len(GSMO)>0:
                fkBody=fkBody+"""
"""+gamesTheShopAvailable(str(cell.value),AvailableURL)
                #print('----------------------')

            elif len(RDMO)>0:
                fkBody=fkBody+"""
"""+RelianceDigitalAvailable(str(cell.value),AvailableURL)
                #print('----------------------')

            else:
                fkBody=fkBody+"""
"""+('This product URL does not go with flipkart, games shop or reliance digital')
    mailBody="""Dear User,

This is the status mail to check the availability of the products.
Please find below the list of URLs of available products.

"""+str(AvailableURL)+"""


Regards,
AUP
"""
    #print(mailBody) #Can be enabled for debugging

    MailResult(mailBody)

getDataFromExcelSource(sourceExcelPath,AvailableURL)
#print(AvailableURL) #Can be enabled for debugging


