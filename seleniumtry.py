import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Academic:
    def __init__(self, name=None, academicBackground=None, education=None, books=None, publications=None, proceedings=None):
        self.name = name
        self.academicBackground = academicBackground
        self.education = education
        self.books = books
        self.publications = publications
        self.proceedings = proceedings


keys = ['Isim', 'AkademikGorevler', 'OgrenimBilgisi','Kitaplar', 'Makaleler', 'Bildiriler']


comOutfile = "outputs/iletisim.csv" 
comOutputFile = open(comOutfile, 'w', newline='', encoding='utf-8')
com_dict_writer = csv.DictWriter(comOutputFile, keys)
com_dict_writer.writeheader()

psychOutfile = "outputs/psikoloji.csv" 
psychOutputFile = open(psychOutfile, 'w', newline='', encoding='utf-8')
psych_dict_writer = csv.DictWriter(psychOutputFile, keys)
psych_dict_writer.writeheader()


chrome_options = Options()  
chrome_options.add_argument("--headless")  

driver = webdriver.Chrome(chrome_options=chrome_options)  # Optional argument, if not specified will search path.

def fetchAuthorLinks(link, fileToWriteIn):
    driver.get(link)
    authors = driver.find_elements_by_css_selector('[id^=authorInfo]')
    for author in authors:
        actualAuthors = driver.find_elements_by_css_selector('[id^=authorInfo')
        link_element = actualAuthors[authors.index(author)].find_element_by_tag_name('h4').find_element_by_tag_name('a')
        extractAuthorInformation(link_element.get_attribute('href'), fileToWriteIn)
        driver.back()
        print("Successful")
    
    nextPageLink = fetchNextPage(driver)
    if nextPageLink != None:
        fetchAuthorLinks(nextPageLink, fileToWriteIn)
    


def fetchNextPage(element):
    nextPaginationElement = element.find_elements_by_xpath("//ul[@class='pagination']//li[@class='active']/following-sibling::li")
    if not nextPaginationElement:
        return None 
    else:
        return nextPaginationElement[0].find_element_by_tag_name('a').get_attribute('href')


def extractAuthorInformation(author, fileToWriteIn):
    driver.get(author)

    academic = Academic()
    academic.name = driver.find_element_by_id('authorlistTb').find_element_by_tag_name('h4').text

    'Academic Background'
    academicBackgroundListItems = driver.find_element_by_xpath('(//ul[@class="timeline"])[1]').find_elements_by_tag_name('li')
    academicBackgrounds = []
    for i in range(1, len(academicBackgroundListItems) - 1, 2):
        academicBackground = {
            "year": None,
            "position": None,
            "university": None,
            "department": None
        }
        academicBackground["year"] = academicBackgroundListItems[i].find_element_by_tag_name('span').text
        academicBackground["position"] = academicBackgroundListItems[i+1].find_element_by_class_name('timeline-footer').find_element_by_tag_name('a').text
        academicBackground["university"] = academicBackgroundListItems[i+1].find_element_by_class_name('timeline-item').find_element_by_tag_name('h4').text
        academicBackground["department"] = academicBackgroundListItems[i+1].find_element_by_class_name('timeline-item').find_element_by_class_name('timeline-body').find_element_by_tag_name('h5').text
        academicBackgrounds.append(academicBackground)

    academic.academicBackground = json.dumps(academicBackgrounds, ensure_ascii=False)

    'Education'
    educationListItems = driver.find_element_by_xpath('(//ul[@class="timeline"])[2]').find_elements_by_tag_name('li')
    educationHistory = []
    for i in range(1, len(educationListItems) - 1, 2):
        education = {
            "year": None,
            "degree": None,
            "university": None,
            "department": None
        }
        education["year"] = educationListItems[i].find_element_by_tag_name('span').text
        education["degree"] = educationListItems[i+1].find_element_by_class_name('timeline-footer').find_element_by_tag_name('a').text
        education["university"] = educationListItems[i+1].find_element_by_class_name('timeline-item').find_element_by_tag_name('h4').text
        education["department"] = educationListItems[i+1].find_element_by_class_name('timeline-item').find_element_by_class_name('timeline-body').find_element_by_tag_name('h5').text
        educationHistory.append(education)
    
    academic.education = json.dumps(educationHistory, ensure_ascii=False)

    'Publications'
    driver.get(driver.find_element_by_id("articleMenu").find_element_by_tag_name("a").get_attribute("href"))
    publicationElements = driver.find_element_by_class_name("searchable").find_elements_by_tag_name("tr")
    publications = []
    for publicationElement in publicationElements:
        publication = {
            "title": None,
            "journal": None
        }
        publication["title"] = publicationElement.find_element_by_xpath("//span[@class='baslika']").find_element_by_tag_name("a").text
        splitPublication = publicationElement.text.split("\n")
        if len(splitPublication) > 1:
            publication["journal"] = splitPublication[1]
        
        publications.append(publication)
    
    academic.publications = json.dumps(publications, ensure_ascii=False)
    driver.back()

    'Proceedings'
    driver.get(driver.find_element_by_id("proceedingMenu").find_element_by_tag_name("a").get_attribute("href"))
    proceedingElements = driver.find_element_by_class_name("searchable").find_elements_by_tag_name("tr")
    proceedings = []
    for proceedingElement in proceedingElements:
        proceeding = {
            "title": None,
            "actor(s)": None,
            "event": None
        }
        proceeding["title"] = proceedingElement.find_element_by_xpath("//span[@class='baslika']").find_element_by_tag_name("a").text
        splitProceeding = proceedingElement.text.split("\n")
        if len(splitProceeding) > 1:
            proceeding["event"] = splitProceeding[1]

        proceedings.append(proceeding)
    
    academic.proceedings = json.dumps(proceedings, ensure_ascii=False)
    driver.back()

    'Books'
    driver.get(driver.find_element_by_id("booksMenu").find_element_by_tag_name("a").get_attribute("href"))
    bookElements = driver.find_element_by_class_name("projects").find_elements_by_tag_name("div")
    books = []
    for bookElement in bookElements:
        book = {
            "title": None,
            "publisher": None,
            "year": None
        }
        book["title"] = bookElement.find_element_by_tag_name("strong").text
        book["publisher"] = bookElement.find_element_by_xpath("(//p)[2]").text
        book["year"] = bookElement.find_element_by_xpath("//span[@class='label label-info']").text
        books.append(book)
    
    academic.books = json.dumps(books, ensure_ascii=False)

    fileToWriteIn.writerow({'Isim': academic.name, 'AkademikGorevler': academic.academicBackground, 'OgrenimBilgisi': academic.education, 'Kitaplar': academic.books, 'Makaleler': academic.publications, 'Bildiriler': academic.proceedings})
    driver.back()


'Initialising Iletisim'
'Gorsel Iletisim Tasarimi'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHPXlqzHXR9804alf5t3WAK_DSh--IWGUumkwXAa42sRR', com_dict_writer)
'Gazetecilik ve Medya Calismalari'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=maTx96xvkLaEhaUt-iYTtpVyLqdKiBfkYFheAY1HNMe6rGdYDplwTYkFx5fwwQCj', com_dict_writer)
'Halkla Iliskiler'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHPXlqzHXR9804alf5t3WAK-6rGdYDplwTYkFx5fwwQCj', com_dict_writer)
'Reklamcilik'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHIBHX0A_44iNr6MBE_iSuQrDSh--IWGUumkwXAa42sRR', com_dict_writer)
'Sinema'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHO02R_jAmOMNGBP1Va6lox9eEQelTm-XyRhBW_4oLHrN', com_dict_writer)
'Iletisim Calismalari'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=PWzTIkoQZ3UN9wT2tqLxE_MvzfzH5mo1_6YOKB4t-0i6rGdYDplwTYkFx5fwwQCj', iletisim_dict_writer)

'Initialising Psychology'
'Gelisim Psikolojisi'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHOfcr38r9BlK-88af1C2BV4_HK2vOcGPj0bi__hecw25', psych_dict_writer)
'Klinik Psikoloji'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHPXlqzHXR9804alf5t3WAK8_HK2vOcGPj0bi__hecw25', psych_dict_writer)
'Uygulamali Psikoloji'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHPdgx5SV1-JiGGjJP2g1XzZbvbgQ2O_T1ouh_7FLbWHJ', psych_dict_writer)
'Ogrenme-Bilissel-Biyo-Deneysel Psikoloji'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHMCAZIPWmaR6kCtoc8zSlhnDSh--IWGUumkwXAa42sRR', psych_dict_writer)
'Sosyal Psikoloji'
fetchAuthorLinks('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=uDtR4DFNBLiPHbTpsE4MHAhmeP8-0nlILe8ZLw_LROzDSh--IWGUumkwXAa42sRR', psych_dict_writer)

time.sleep(5)
driver.quit()
