
import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class Academic:
    def __init__(self, unvan=None, isim=None, calistigiYer=None, calismaAlanlari=None, egitimGecmisi=None, 
    kitapSayisi=None, uluslararasiYayinSayisi=None, yerliYayinSayisi=None, digerYayinSayisi=None,
    uluslararasiBildiriSayisi=None, yerliBildiriSayisi=None):
        self.unvan = unvan
        self.isim = isim
        self.calistigiYer = calistigiYer
        self.calismaAlanlari = calismaAlanlari
        self.egitimGecmisi = egitimGecmisi
        self.kitapSayisi = kitapSayisi
        self.uluslararasiYayinSayisi = uluslararasiYayinSayisi
        self.yerliYayinSayisi = yerliYayinSayisi
        self.digerYayinSayisi = digerYayinSayisi
        self.uluslararasiBildiriSayisi = uluslararasiBildiriSayisi
        self.yerliBildiriSayisi = yerliBildiriSayisi


keys = ['Unvan', 'Isim', 'CalistigiYer','Calisma Alanlari', 'Egitim Gecmisi', 'Kitap Sayisi', 
'Uluslararasi Yayin Sayisi', 'Yerli Yayin Sayisi', 'Diger Yayin Sayisi', 
'Uluslararasi Bildiri Sayisi', 'Yerli Bildiri Sayisi']

bolum_keywords = ['iletişim', 'yeni medya', 'medya ve iletişim', 'yeni medya ve iletişim', 'yeni medya ve gazetecilik',
'sinema ve dijital medya', 'yeni medya ve iletişim tasarımı']


chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)  # Optional argument, if not specified will search path.

def fetchUniInfobyDep(link):
    driver.get(link)
    uniElements = driver.find_element_by_class_name('searchable').find_elements_by_tag_name('tr')
    for uniElement in uniElements:
        driver.get(link)
        actualUniElements = driver.find_element_by_class_name('searchable').find_elements_by_tag_name('tr')
        driver.get(actualUniElements[uniElements.index(uniElement)].find_element_by_tag_name('a').get_attribute('href'))
        'Initialising Iletisim'
        birimElements = driver.find_element_by_id('searchlist').find_elements_by_tag_name('a')
        for birimElement in birimElements:
            actualBirimElements = driver.find_element_by_id('searchlist').find_elements_by_tag_name('a')
            if "İLETİŞİM" in actualBirimElements[birimElements.index(birimElement)].text:
                continue
            driver.get(actualBirimElements[birimElements.index(birimElement)].get_attribute('href'))
            try:
                depElementParent = driver.find_elements_by_xpath("(//ul[@class='list-group'])[4]")
                if len(depElementParent) > 0:
                    depElements = depElementParent[0].find_elements_by_tag_name("a")
                    for depElement in depElements:
                        actualDepElements = driver.find_element_by_xpath("(//ul[@class='list-group'])[4]").find_elements_by_tag_name("a")
                        depInterested = False
                        depNameLowerCase = actualDepElements[depElements.index(depElement)].text.lower()
                        for bolum in bolum_keywords:
                            if bolum in depNameLowerCase:
                                depInterested = True
                                break
                        if depInterested == True:
                            fetchAuthorLinks(actualDepElements[depElements.index(depElement)].get_attribute('href'), com_dict_bolum_writer)
                            driver.back()
                    driver.back()
            except NoSuchElementException:
                driver.back()
        driver.back()

        
def fetchUniInfo(link):
    driver.get(link)
    uniElements = driver.find_element_by_class_name('searchable').find_elements_by_tag_name('tr')
    for uniElement in uniElements:
        driver.get(link)
        actualUniElements = driver.find_element_by_class_name('searchable').find_elements_by_tag_name('tr')
        driver.get(actualUniElements[uniElements.index(uniElement)].find_element_by_tag_name('a').get_attribute('href'))
        'Initialising Iletisim'
        iletisimBirimElements = driver.find_element_by_id('searchlist').find_elements_by_partial_link_text('İLETİŞİM')
        for iletisimBirimElement in iletisimBirimElements:
            actualIletisimBirimElements = driver.find_element_by_id('searchlist').find_elements_by_partial_link_text('İLETİŞİM')
            fetchAuthorLinks(actualIletisimBirimElements[iletisimBirimElements.index(iletisimBirimElement)].get_attribute('href'), com_dict_writer)
            driver.back()
        'Initialising Psychology'
        psikolojiBirimElements = driver.find_element_by_id('searchlist').find_elements_by_partial_link_text('PSİKOLOJİ')
        for psikolojiBirimElement in psikolojiBirimElements:
            actualPsikolojiBirimElements = driver.find_element_by_id('searchlist').find_elements_by_partial_link_text('PSİKOLOJİ')
            fetchAuthorLinks(actualPsikolojiBirimElements[psikolojiBirimElements.index(psikolojiBirimElement)].get_attribute('href'), psych_dict_writer)
            driver.back()
        'We should be done by now...'
        driver.back()

    

def fetchAuthorLinks(link, fileToWriteIn):
    driver.get(link)
    authors = driver.find_elements_by_css_selector('[id^=authorInfo]')
    for author in authors:
        actualAuthors = driver.find_elements_by_css_selector('[id^=authorInfo')
        link_element = actualAuthors[authors.index(author)].find_element_by_tag_name('h4').find_element_by_tag_name('a')
        title = actualAuthors[authors.index(author)].find_element_by_xpath('(//h6)[1]').text
        name = actualAuthors[authors.index(author)].find_element_by_tag_name('h4').text
        position = actualAuthors[authors.index(author)].find_element_by_xpath('(//h6)[2]').text
        'Calisma Alanlari'
        calismaAlanlariStr = []
        calismaAlanlari = actualAuthors[authors.index(author)].find_elements_by_tag_name('span')
        for calismaAlani in calismaAlanlari:
            calismaAlaniText = calismaAlani.text
            if calismaAlaniText != '':
                calismaAlanlariStr.append(calismaAlaniText)
        extractAuthorInformation(link_element.get_attribute('href'), title, name, position, ';'.join(calismaAlanlariStr), fileToWriteIn)
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


def extractAuthorInformation(author, title, name, position, studyTopics, fileToWriteIn):
    driver.get(author)

    academic = Academic()
    academic.unvan = title
    academic.isim = name
    academic.calistigiYer = position
    academic.calismaAlanlari = studyTopics

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
        educationHistory.append(', '.join("{!s}".format(val) for (key,val) in education.items()))
    


    academic.egitimGecmisi = ";".join(educationHistory)

    'Publications'
    driver.get(driver.find_element_by_id("articleMenu").find_element_by_tag_name("a").get_attribute("href"))
    internationalPublicationElements = driver.find_elements_by_id('international')
    if len(internationalPublicationElements) > 0:
        academic.uluslararasiYayinSayisi = len(internationalPublicationElements[0].find_element_by_class_name("searchable").find_elements_by_tag_name("tr"))
    else:
        academic.uluslararasiYayinSayisi = 0
    domesticPublicationElements = driver.find_elements_by_id('national')
    if len(domesticPublicationElements) > 0:
        academic.yerliYayinSayisi = len(domesticPublicationElements[0].find_element_by_class_name("searchable").find_elements_by_tag_name("tr"))
    else:
        academic.yerliYayinSayisi = 0
    otherPublicationElements = driver.find_element_by_id('all').find_element_by_class_name("searchable").find_elements_by_tag_name("tr")
    academic.digerYayinSayisi = len(otherPublicationElements)
    
    driver.back()

    'Proceedings'
    driver.get(driver.find_element_by_id("proceedingMenu").find_element_by_tag_name("a").get_attribute("href"))
    internationalProceedingElements = driver.find_elements_by_id('international')
    if len(internationalProceedingElements) > 0:
        academic.uluslararasiBildiriSayisi = len(internationalProceedingElements[0].find_element_by_class_name("searchable").find_elements_by_tag_name("tr"))
    else:
        academic.uluslararasiBildiriSayisi = 0
    domesticProceedingElements = driver.find_elements_by_id('national')
    if len(domesticProceedingElements) > 0:
        academic.yerliBildiriSayisi = len(domesticProceedingElements[0].find_element_by_class_name("searchable").find_elements_by_tag_name("tr"))
    else:
        academic.yerliBildiriSayisi = 0

    driver.back()

    'Books'
    driver.get(driver.find_element_by_id("booksMenu").find_element_by_tag_name("a").get_attribute("href"))
    bookElements = driver.find_element_by_class_name("projects").find_elements_by_tag_name("div")
    academic.kitapSayisi = len(bookElements)
    
    if "Doktora" in academic.egitimGecmisi:
        fileToWriteIn.writerow({'Unvan': academic.unvan, 'Isim': academic.isim, 'CalistigiYer': academic.calistigiYer, 'Calisma Alanlari': academic.calismaAlanlari, 'Egitim Gecmisi': academic.egitimGecmisi, 
        'Kitap Sayisi': academic.kitapSayisi, 'Uluslararasi Yayin Sayisi': academic.uluslararasiYayinSayisi, 'Yerli Yayin Sayisi': academic.yerliYayinSayisi,
        'Diger Yayin Sayisi': academic.digerYayinSayisi, 'Uluslararasi Bildiri Sayisi': academic.uluslararasiBildiriSayisi, 'Yerli Bildiri Sayisi': academic.yerliBildiriSayisi})

    driver.back()


comOutfileBolum = "outputs/iletisim_bolum.csv"
comOutputFileBolum = open(comOutfileBolum, 'w', newline='', encoding='utf-8')
com_dict_bolum_writer = csv.DictWriter(comOutputFileBolum, keys)
com_dict_bolum_writer.writeheader()
fetchUniInfobyDep('https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp')
comOutputFileBolum.close()

psychOutfile = "outputs/psikoloji.csv" 
psychOutputFile = open(psychOutfile, 'w', newline='', encoding='utf-8')
psych_dict_writer = csv.DictWriter(psychOutputFile, keys)
psych_dict_writer.writeheader()

comOutfile = "outputs/iletisim.csv" 
comOutputFile = open(comOutfile, 'w', newline='', encoding='utf-8')
com_dict_writer = csv.DictWriter(comOutputFile, keys)
com_dict_writer.writeheader()

fetchUniInfo('https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp')
psychOutputFile.close()
comOutputFile.close()

'''
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
'''


time.sleep(5)
driver.quit()


"""
for academic.egitimGecmisi we are only considering doktora. If someone holds a doktora, we are only considering that. Egitim gecmisi field would still have postgraduate, and graduate information.
"""
