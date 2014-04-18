import req_proxy
from lxml import html
from bs4 import BeautifulSoup
import logging 
import re 
import time
import os
from Queue import Queue
import threading

num_fetch_threads = 10
enclosure_queue = Queue()




logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )


def main(directory, catelink, target, cate):
    filename = "%s/f_cl_tr_ct_st_scl.txt" %(directory)

    f = open(filename, "a+")
   
    page = req_proxy.main(catelink)

    soup = BeautifulSoup(page, "html.parser")
    cate_tag_list = soup.find_all("span", attrs={"class":"forspan"})

    for cate_tag in cate_tag_list:
        if str(cate_tag.get_text()).strip() == "Category":
            sub_cat_box = cate_tag.find_parent("div", attrs={"class":"divli"})

    sub_cat_list = sub_cat_box.find_all("a", attrs={"class":"RefineByLink"})

    for sub_cat_tag  in sub_cat_list:
        sub_cat = str(sub_cat_tag.get("relmselect"))
	sub_cat_link = "http://www.yebhi.com%s" %(str(sub_cat_tag.get("href")))
	f.write(str([catelink, target, cate, sub_cat, sub_cat_link]) + "\n")
        logging.debug([catelink, target, cate, sub_cat, sub_cat_link])

    f.close()
    


def mainthread2(i, q):
    for line in iter(q.get, None):
        try:
            directory = line[0]
            link = line[1]
            target = line[2]
            cate = line[3]

            main(directory, link, target, cate)

        except:
            f2 = open("page1_first_sub_cat_ext_yebhi.txt", "a+")
            f2.write(str(line) + "\n")
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def supermain():
    directory = "yebhi%s" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)
    except:
       pass

    f = open("yebhi_extracted.txt", "a+")
    f.write(directory)
    f.close()

    f = open("yebhi_to_extract.txt", "w+")
    f.write(directory)
    f.close()


    #main("http://www.yebhi.com/online-shopping/men/shoes.html?affint=men-topmenu", "Men", "Shoes")
    link_list = [(directory, "http://www.yebhi.com/online-shopping/men/shoes.html?affint=men-topmenu", "Men", "Shoes"), 
                 (directory, "http://www.yebhi.com/online-shopping/men/apparels.html?affint=men-topmenu", "Men", "Clothing"),  
                 (directory, "http://www.yebhi.com/online-shopping/lifestyle/men.html?affint=men-topmenu", "Men", "Accessory"), 
                 (directory, "http://www.yebhi.com/online-shopping/men/bath-and-beauty.html?affint=men-topmenu", "Men", "Personal Care"), 
                 (directory, "http://www.yebhi.com/online-shopping/women/shoes.html?affint=women-topmenu", "Women", "Shoes"), 
                 (directory, "http://www.yebhi.com/online-shopping/women/apparels.html?affint=women-topmenu", "Women", "Clothing"), 
                 (directory, "http://www.yebhi.com/online-shopping/women/dress-materials/sarees/salwar-kameez-set/kurta-kurtis/leggings-and-jeggings.html?affint=women-topmenu", "Women", "Traditional-Ethnic"), 
                 (directory, "http://www.yebhi.com/online-shopping/lifestyle/women.html?affint=women-topmenu", "Women", "Accessories"), 
                 (directory, "http://www.yebhi.com/online-shopping/women/bath-and-beauty.html?affint=women-topmenu", "Women", "Personal-Care"), 
                 (directory, "http://www.yebhi.com/online-shopping/boys.html?affint=kids-topmenu", "Kids", "Boys-Clothing"), 
                 (directory, "http://www.yebhi.com/online-shopping/boys/shoes.html?affint=kids-topmenu", "kids", "Boys-Shoes"), 
                 (directory, "http://www.yebhi.com/online-shopping/girls.html?affint=kids-topmenu", "kids", "girls-clothing"), 
                 (directory, "http://www.yebhi.com/online-shopping/girls/shoes.html?affint=kids-topmenu", "kids", "girls-shoes"), 
                 (directory, "http://www.yebhi.com/online-shopping/toys-and-games.html?affint=kids-topmenu", "kids", "toys-n-games"), 
                 (directory, "http://www.yebhi.com/online-shopping/home-furnishing.html?affint=home-topmenu", "home and kitchen", "Home Furnishings"), 
                 (directory, "http://www.yebhi.com/online-shopping/home-decor.html?affint=home-topmenu", "home and kitchen", "Home Decor"), 
                 (directory, "http://www.yebhi.com/online-shopping/home-ware.html?affint=home-topmenu", "home and kitchen", "Home Ware"), 
                 (directory, "http://www.yebhi.com/online-shopping/appliances.html?affint=home-topmenu", "home and kitchen", "Appliances"), 
                 (directory, "http://www.yebhi.com/online-shopping/furniture.html?affint=home-topmenu", "home and kitchen", "Furniture"), 
                 ]
        
    procs = []

    for i in range(num_fetch_threads):
        procs.append(threading.Thread(target=mainthread2, args=(i, enclosure_queue,)))
        procs[-1].start()


    for line in link_list:
        enclosure_queue.put(line)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()




if __name__=="__main__":
    supermain()
