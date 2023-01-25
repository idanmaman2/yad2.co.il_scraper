LinkTemplate = """https://gw.yad2.co.il/feed-search-legacy/products/%s?category=%d&item=%d&page=%d&forceLdLoad=true"""
import requests 
import csv
import json
def fetchJson(section : str  , catgeory : int, item : int , printIt= False , page : int =0):
    '''generator to get all yad2 item and category pages and results '''
    jsonRes = requests.get(LinkTemplate%( section , catgeory , item , page )).json()
    for itemJson in jsonRes["data"]["feed"]["feed_items"]: 
        yield itemJson
        if printIt :
            print(json.dumps(itemJson,ensure_ascii=False))
    if(jsonRes["data"]["pagination"]["current_page"] < jsonRes["data"]["pagination"]["last_page"]  ): 
        yield from fetchJson(section , catgeory , item  , printIt, page+1)

def items(section , catgeory : int , searchTerm):
    cats = requests.get(f"https://gw.yad2.co.il/search-options/products/{section}?fields={searchTerm}&category={catgeory}").json()
    yield from cats["data"][searchTerm] 

    
def to_csv(name, jsonList : list ):
    with open(name, 'w', newline='',encoding="utf-16") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        for index,item in enumerate(jsonList) : 
            if not(index):
                  spamwriter.writerow(item.keys())
            spamwriter.writerow(list(map(lambda val : str(val).replace("\t","     "),item.values())))
to_csv("items_in_section.csv" ,items("cellular" , 5,"item") )     
to_csv("areas_codes.csv" ,items("cellular" , 5,"area") )    
to_csv("fetched_data.csv" ,fetchJson("cellular" , 5,29,True) )
