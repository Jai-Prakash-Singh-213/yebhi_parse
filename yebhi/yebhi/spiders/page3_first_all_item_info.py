import req_proxy
from  bs4 import BeautifulSoup
from lxml import html
import threading
import logging
import os 
import multiprocessing
import time
import ast
import os 
from Queue import Queue

#num_fetch_threads = 50
#enclosure_queue = Queue()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

num_fetch_threads = 150
enclosure_queue = multiprocessing.JoinableQueue()



def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()



def main(line, directory):
    direc = "%s/%s/%s/%s" %(directory, line[2], line[3], line[5])

    try:
        os.makedirs(direc)
    except:
        pass

    filename = "%s/%s.csv" %(direc, line[5])
    f = open(filename, "a+")
    
    page = req_proxy.main(line[-6])
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("title").get_text()
    meta_disc = soup.find("meta", attrs={"name":"description"}).get("content")
    seller = "yebhi.com"
    item_desc = soup.find("div", attrs={"itemprop":"description"})
    dte = time.strftime("%d:%m:%Y")
    status  = " "

    f.write(",".join(map(my_strip, [line[9], line[7], line[0], line[12], line[2],
                                    line[3], line[5], line[10],  line[11], '',  
                                    line[1], line[8], seller, title, 
                                    meta_disc, line[13], item_desc, '', dte, status] )) + "\n")
    f.close()

    logging.debug("inserted  ............")



def main_process2(i, q):
    for line, directory in iter(q.get, None):
        try:
            line = ast.literal_eval(line)
            main(line, directory)

        except:
            f = open("page3_first_all_item_info_error_yebhy.py", "a+")
            f.write(str(line))
            f.close()   

        time.sleep(5)
        q.task_done()

    q.task_done()


    
def line_collect():
    f = open("yebhi_to_extract.txt")
    directory = f.read().strip()
    f.close()

    curr_dir = os.getcwd()

    filename = "%s/%s/f_cl_tr_ct_st_scl_bt_bl_item_info.txt" %(curr_dir, directory)

    f = open(filename)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main_process2, args=(i, enclosure_queue,)))
        #procs.append(threading.Thread(target=main_process2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for line in f:
        enclosure_queue.put((line.strip(), directory))

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

    #line = ['http://www.yebhi.com/online-shopping/boys.html?affint=kids-topmenu', 'Kids', 'Boys-Clothing', 'casual-shoes', 'http://www.yebhi.com/online-shopping/boys/casual-shoes.html?affint=kids-topmenu&lc=Category', 'footfun', 'http://www.yebhi.com/online-shopping/footfun/boys/casual-shoes.html?affint=kids-topmenu&lc=Brands', 'footfun pink boys casual shoes', 'http://www.yebhi.com/486408/PD/footfun-pink-boys-casual-shoes.htm', '486408', 'http://im6.ybndc.com/upload/486408/ProductRear635300635893122000.jpg', '299', '299', 'EU 23']

    #filename = "yebhi14042014"

    #main(line, filename)
    



if __name__=="__main__":
    supermain()
