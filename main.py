import requests
from bs4 import BeautifulSoup 
import re
import os

url="https://dwgfree.com/category/"

categories = ['cad-accessories','2d-animals','cad-architecture','autocad-block-library-files','bedroom-cad-blocks','bathroom-cad-blocks','door-cad-block','road-dwg','furniture-cad-blocks','free-autocad-house-plans-drawings','kitchen-cad-blocks-drawings','autocad-projects','people-cad-blocks','drawing-sports','stairs-block','automobile-blocks','plan-tree-cad-blocks','autocad-title-blocks-templates','auto-cad-symbol','autocad-electric-symbols','electrical-lighting-dwg','pipe-fittings']

destinationFolder = "drawings"

def getdata(url): 
    r = requests.get(url) 
    return r.text 

def downloadFile(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

def download(downloadurl,category):
    htmldata = getdata(downloadurl) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    downloadlink = soup.find("a",class_="grid-link-container")
    print(downloadlink['href'])
    downloadlink = re.findall(r'http[s]?:\/\/dwgfree.com\/wp-content\/uploads\/.*', downloadlink['href'])
    if(len(downloadlink) > 0):
        print("will download "+downloadlink[0])
        downloadFile(downloadlink[0],destinationFolder+"/"+category)

for category in categories:
    fetchUrl = url+category
    havedoc = True
    while(havedoc):
        # get document
        print("downloading "+fetchUrl)
        htmldata = getdata(fetchUrl) 
        soup = BeautifulSoup(htmldata, 'html.parser') 
        data = '' 
        for data in soup.find_all("a",class_="db"): 
            print(data['href'])
            download(data['href'],category)

        nextPage = soup.find("a",class_="next page-numbers")
        if nextPage:
            print(nextPage['href'])
            fetchUrl=nextPage['href']
            havedoc = True
        else:
            havedoc = False
print("end of statement")
