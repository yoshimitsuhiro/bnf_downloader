from io import BytesIO
import requests, time, regex

def main():
	print(u"Enter the ARK identifant of the book you wish to download:")
	print(u"(Url should look similar to this: \"https://gallica.bnf.fr/ark:/12148/btv1b8454684f\")")
	while True:
		ark_url = input("") #get URL of book
		if ark_url[:28] == "https://gallica.bnf.fr/ark:/": break
		else: print(u"Invalid input! Be sure to enter the full URL including https://.")
	ark_id = ark_url.split("/")[-2]
	book_id = ark_url.split("/")[-1]
	#ark_url = "https://gallica.bnf.fr/ark:/xxxxx/xxxxxxxxxxxxx" #manually set ark_url
	#ark_id = xxxxx #manually set ark_id
	#book_id = "xxxxxxxxxxxxx" #manually set book_id
	source = get_source(ark_url)
	print_title(source)
	page, lastpage = calculate_pages(source)
	download_images(ark_id, book_id, page, lastpage)

def print_title(source):
	match = regex.search(r"<title>.+?</title>", source.text)
	title = match.group(0)[7:-8]
	print("\n{0}\n".format(title))

def calculate_pages(source):
	print(u"From what page do you wish to start the download? (Input \"1\" to start from the beginning)")
	while True:
		page = input("") #get first page number
		if page.isdigit(): break
		else: print(u"Invalid input! Be sure to input an integer value.")
	page = int(page)
	print(u"Calculate last page automatically (for downloading entire book) (y/n)?")
	while True:
		choice = input()
		if choice == "y" or choice == "Y" or choice == "yes" or choice == "YES":
			print("Calculating total number of pages...")
			match = regex.search(r"nbTotalVues\\\":.+?,", source.text)
			lastpage = int(match.group(0)[14:-1])
			print("Total number of pages = {0}.\n".format(lastpage))
			break
		elif choice == "n" or choice == "N" or choice == "no" or choice == "NO":
			print(u"Input last page number: ")
			while True:
				lastpage = input("") #get final page number
				if lastpage.isdigit(): break
				else: print(u"Invalid input! Be input an integer value.")
			lastpage = int(lastpage)
			break
		else: print(u"Invalid input! Input yes or no.")
	return(page, lastpage)

def calculate_image_size(ark_id, book_id, page):
	zoom_url = "https://gallica.bnf.fr/services/ajax/mode/SINGLE/ark:/{0}/{1}/f{2}.image.zoom".format(ark_id, book_id, page)
	source = get_source(zoom_url)
	searchstring = regex.compile("\\\"ark:/" + str(ark_id) + "/" + str(book_id) + "/f" + str(page) + "\\\",\\\"_width\":.{0,5},\\\"_height\\\":.{0,5},")
	match = searchstring.search(source.text)
	x = int(regex.search("\\\"_width\\\":.{0,5},", match.group(0)).group(0)[9:-1])
	y = int(regex.search("\\\"_height\\\":.{0,5},", match.group(0)).group(0)[10:-1])
	#x = 0 #set x manually (size doesn't matter, as long as x is larger than the x value of the largest page)
	#y = 0 #set y manually (should be set to the exact value of y or warping will occur)
	return(x, y)

def download_images(ark_id, book_id, page, lastpage):
	#page = 1 #manually set first page
	#lastpage = 246 #manually set last page
	while page <= lastpage:
		filename = "%04d.jpg" % (page,)
		x, y = calculate_image_size(ark_id, book_id, page)
		print("Now downloading page {0} of {1} (x = {2}, y = {3}).".format(page, lastpage, x, y))
		image_url = "https://gallica.bnf.fr/iiif/ark:/{0}/{1}/f{2}/0,0,{3},{4}/{3},{4}/0/native.jpg".format(ark_id, book_id, page, x, y)
		source = get_source(image_url)
		with open(filename, "wb") as f:
			f.write(source.content)
		page += 1

def get_source(url):
	waittime = 5 #number of seconds to wait between downloads (don't set too low or you will burden the server and get your IP blocked)
	while True:
		try:
			source = requests.get(url)
			source.raise_for_status()
			time.sleep(waittime)
			break
		except requests.exceptions.HTTPError:
			print("Download error. Trying again...")
			time.sleep(waittime)
	return(source)

if __name__ == "__main__":
	main()
