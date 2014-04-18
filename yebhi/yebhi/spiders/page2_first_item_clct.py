import req_proxy
from  bs4 import BeautifulSoup
from lxml import html
import threading
import logging
import os 
import multiprocessing
import time
import ast


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

num_fetch_threads = 100
enclosure_queue = multiprocessing.JoinableQueue()


def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()



def main3(line, filename2, link):
    
    page = req_proxy.main(link)
    soup = BeautifulSoup(page, "html.parser")

    item_box_list = soup.find_all("div", attrs={"class":"price_Reviews"})
    
    f = open(filename2, "a+")

    for item_box in item_box_list:
        item_a_tag = item_box.find("a", attrs={"class":"gotopage"})
	item_title = item_a_tag.get("title")
	item_link = "http://www.yebhi.com%s" %(item_a_tag.get("href"))
	item_sku = item_a_tag.get("id")[item_a_tag.get("id").find("_")+1: ]
	item_image = item_a_tag.img.get("original")
	item_price = item_box.find("input", attrs={"id":"itemMRP_%s" %(item_sku)}).get("value")
	item_discnt = item_box.find("input", attrs={"id":"itemDiscountPrice_%s" %(item_sku)}).get("value")
        try:
	    item_size = item_box.find("p", attrs={"class":"avlsizes"}).span.get_text() 
        except:
            item_size = "None"

        f.write(str(line + map(my_strip, [item_title, item_link,  item_sku, item_image, item_price, item_discnt, item_size])) + "\n")
        logging.debug(line + map(my_strip, [item_title, item_link,  item_sku, item_image, item_price, item_discnt, item_size]))
        
    f.close()



def main2(line, filename2, link):
    try:
        main3(line, filename2, link)
    except:
        pass



def main(line, filename2):
    page = req_proxy.main(line[-1])
    soup = BeautifulSoup(page, "html.parser")
    
    all_page_list = soup.find_all("li", attrs={"class":"MyAccountPag"})

    threads = []

    t = threading.Thread(target=main2, args=(line, filename2, line[-1],))
    threads.append(t)
    t.start()

    for page_link_tag in all_page_list:
        page_link = "http://www.yebhi.com%s" %(str(page_link_tag.a.get("href")))
        t = threading.Thread(target=main2, args=(line, filename2, page_link,))
	threads.append(t)
	t.start()

    main_thread = threading.currentThread()

    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()



def main_process2(i, q):
    for line, filename2 in iter(q.get, None):
        try:
            line = ast.literal_eval(line)
            main(line, filename2)
            logging.debug(line)

        except:
            pass

        time.sleep(2)
        q.task_done()

    q.task_done()


    
def line_collect():
    f = open("yebhi_to_extract.txt")
    directory = f.read().strip()
    f.close()

    curr_dir = os.getcwd()

    filename = "%s/%s/f_cl_tr_ct_st_scl_bt_bl.txt" %(curr_dir, directory)

    filename2 = "%s/%s/f_cl_tr_ct_st_scl_bt_bl_item_info.txt" %(curr_dir, directory)
    
    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main_process2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for line in f:
        enclosure_queue.put((line.strip(), filename2))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    f.close()
    


def supermain():
    #main("http://www.yebhi.com/online-shopping/men/coats-and-jackets.html?affint=men-topmenu&lc=Category")
    line_collect()
    #line = ['http://www.yebhi.com/online-shopping/boys.html?affint=kids-topmenu', 'Kids', 'Boys-Clothing', 'casual-shoes', 'http://www.yebhi.com/online-shopping/boys/casual-shoes.html?affint=kids-topmenu&lc=Category', 'mardi-gras', 'http://www.yebhi.com/online-shopping/mardi-gras/boys/casual-shoes.html?affint=kids-topmenu&lc=Brands']

    #filename = "yebhi14042014/f_cl_tr_ct_st_scl_bt_bl_item_info.txt"

    #main(line, filename)
    



if __name__=="__main__":
    supermain()
