import req_proxy
from lxml import html
from bs4 import BeautifulSoup
import logging 
import re 
import time
import os
from Queue import Queue
import threading
import ast

num_fetch_threads = 10
enclosure_queue = Queue()




logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


def main(line, directory):
    filename = "%s/f_cl_tr_ct_st_scl_bt_bl.txt" %(directory)
    
    f = open(filename, "a+")
   
    page = req_proxy.main(line[-1])

    soup = BeautifulSoup(page, "html.parser")
    brand_tag_list = soup.find_all("span", attrs={"class":"forspan"})

    
    for brand_tag in brand_tag_list:
        if str(brand_tag.get_text()).strip() == "Brands":
            brand_box = brand_tag.find_parent("div", attrs={"class":"divli"})

    brand_list = brand_box.find_all("a", attrs={"class":"RefineByLink"})

    for brand_tag  in brand_list:
        brand = str(brand_tag.get("relmselect"))
	brand_link = "http://www.yebhi.com%s" %(str(brand_tag.get("href")))
	#f.write(str([catelink, target, cate, sub_cat, sub_cat_link]) + "\n")
        f.write(str([line[0], line[1], line[2], line[3], line[4], brand, brand_link]) + "\n")
        
        logging.debug([line[0], line[1], line[2], line[3], line[4], brand, brand_link])

    f.close()
    


def mainthread2(i, q):
    for line, directory in iter(q.get, None):
        try:
            line = ast.literal_eval(line.strip())
            main(line, directory)

        except:
            f2 = open("page1_second_brand_ext_yebhi.txt", "a+")
            f2.write(str(line) + "\n")
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain():
    f = open("yebhi_to_extract.txt")
    directory = f.read().strip()
    f.close()

    filename = "%s/f_cl_tr_ct_st_scl.txt" %(directory)

    f = open(filename)
        
    procs = []

    for i in range(num_fetch_threads):
        procs.append(threading.Thread(target=mainthread2, args=(i, enclosure_queue,)))
        procs[-1].start()


    for line in f:
        enclosure_queue.put((line, directory))

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()
    
    f.close()



if __name__=="__main__":
    supermain()

    #line = ['http://www.yebhi.com/online-shopping/boys.html?affint=kids-topmenu', 'Kids', 'Boys-Clothing', 'casual-shoes', 'http://www.yebhi.com/online-shopping/boys/casual-shoes.html?affint=kids-topmenu&lc=Category']
    
    
    #directory = "yebhi14042014"
    #main(line, directory)
