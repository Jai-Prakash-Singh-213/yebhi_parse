import req_proxy
from  bs4 import BeautifulSoup
from lxml import html



def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()



def main(link):
    page = req_proxy.main(link)
    soup = BeautifulSoup(page, "html.parser")

    item_box_list = soup.find_all("div", attrs={"class":"price_Reviews"})

    for item_box in item_box_list:
        item_a_tag = item_box.find("a", attrs={"class":"gotopage"})
	item_title = item_a_tag.get("title")
	item_link = "http://www.yebhi.com%s" %(item_a_tag.get("href"))
	item_sku = item_a_tag.get("id")[item_a_tag.get("id").find("_")+1: ]
	item_image = item_a_tag.img.get("original")
	item_price = item_box.find("input", attrs={"id":"itemMRP_%s" %(item_sku)}).get("value")
	item_discnt = item_box.find("input", attrs={"id":"itemDiscountPrice_%s" %(item_sku)}).get("value")
	item_size = item_box.find("p", attrs={"class":"avlsizes"}).span.get_text()

        print map(my_strip, [item_title, item_link,  item_sku, item_image, item_price, item_discnt, item_size])


def supermain():
    main("http://www.yebhi.com/online-shopping/alx-new-york/men/casual-shirts.html?affint=men-topmenu&lc=Brands")



if __name__=="__main__":
    supermain()
