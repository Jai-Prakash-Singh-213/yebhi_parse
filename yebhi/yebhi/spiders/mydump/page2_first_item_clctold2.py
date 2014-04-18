import req_proxy
from  bs4 import BeautifulSoup
from lxml import html
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )



def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()



def main3(link):
    page = req_proxy.main(link)
    soup = BeautifulSoup(page, "html.parser")

    item_box_list = soup.find_all("div", attrs={"class":"price_Reviews"})
    
    f = open("myfile.txt", "a+")

    for item_box in item_box_list:
        item_a_tag = item_box.find("a", attrs={"class":"gotopage"})
	item_title = item_a_tag.get("title")
	item_link = "http://www.yebhi.com%s" %(item_a_tag.get("href"))
	item_sku = item_a_tag.get("id")[item_a_tag.get("id").find("_")+1: ]
	item_image = item_a_tag.img.get("original")
	item_price = item_box.find("input", attrs={"id":"itemMRP_%s" %(item_sku)}).get("value")
	item_discnt = item_box.find("input", attrs={"id":"itemDiscountPrice_%s" %(item_sku)}).get("value")
	item_size = item_box.find("p", attrs={"class":"avlsizes"}).span.get_text() 

        f.write(str(map(my_strip, [item_title, item_link,  item_sku, item_image, item_price, item_discnt, item_size])) + "\n")
        logging.debug(map(my_strip, [item_title, item_link,  item_sku, item_image, item_price, item_discnt, item_size]))
        
    f.close()



def main2(link):
    try:
        main3(link)
    except:
        pass



def main(link):
    page = req_proxy.main(link)
    soup = BeautifulSoup(page, "html.parser")
    
    all_page_list = soup.find_all("li", attrs={"class":"MyAccountPag"})

    threads = []

    t = threading.Thread(target=main2, args=(link,))
    threads.append(t)
    t.start()

    for page_link_tag in all_page_list:
        page_link = "http://www.yebhi.com%s" %(str(page_link_tag.a.get("href")))
        t = threading.Thread(target=main2, args=(page_link,))
	threads.append(t)
	t.start()

    main_thread = threading.currentThread()

    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()

    



def supermain():
    main("http://www.yebhi.com/online-shopping/men/coats-and-jackets.html?affint=men-topmenu&lc=Category")



if __name__=="__main__":
    supermain()
