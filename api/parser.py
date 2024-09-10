import requests
from bs4 import BeautifulSoup
import json

class NewykParser:
    
    def __init__(self):
        self.dict_of_classes = {}
        pass
    
    def _get_data_(self, url: str) -> requests.models.Response:
        if not url:
            raise Exception("URL is required")
        try:
            response = requests.get(url)
            return response
        except Exception as e:
            raise Exception(f"Error with getting url ({url}): {e}")
    
    def _parse_data_(self, response: requests.models.Response) -> BeautifulSoup:
        if not response:
            raise Exception("Response is required")
        elif response.status_code != 200:
            raise Exception(f"Error with getting url ({response.url}): {response.status_code}")
        try:
            data = response.text
            parser = BeautifulSoup(data, 'lxml')
            return parser
        except Exception as e:
            raise Exception(f"Error with parsing response: {e}")
        
    def _load_dict_(self, file_name: str = "sources/classes_to_parse.json") -> dict:
        if not file_name:
            raise Exception("File name is required")
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
            self.dict_of_classes = data
            return data
        except Exception as e:
            raise Exception(f"Error with loading data: {e}")
        
    def _get_news_(self, url: str, parser: BeautifulSoup) -> list:
        if not parser:
            raise Exception("Parser is required")
        elif not self.dict_of_classes:
            raise Exception("Dictionary of classes is empty")
        try:
            news = []
            for url1 in self.dict_of_classes:
                if url1 in url:
                    for pair in self.dict_of_classes[url1]:
                        news = news + list(parser.find_all(pair[0], {pair[1]: pair[2]}))
            return news
        except Exception as e:
            raise Exception(f"Error with getting news: {e}")
        
    def _filter_news_(self, news: list) -> list:
        hrefs = []
        for element in news:
            href_element = element.find("a", {"data-testid": "internal-link"})
            if href_element:
                href = href_element.get("href")
                hrefs.append("https://www.bbc.com"+href)
                
        hrefs = list(set(hrefs))
        return hrefs
    
    def _get_new_data_(self, url: str) -> dict:
        images = []
        response = self._get_data_(url)
        parser = self._parse_data_(response)
        article = parser.find("article")
        if "sport" in url:
            title_tag_tuple = ("h1", "class", "ssrcss-1mguc0h-Heading e10rt3ze0")
            text_elements_tuple = ("p", "class", "ssrcss-1q0x1qg-Paragraph e1jhz7w10")
            image_tag_tuple = ("img", "class", "ssrcss-11yxrdo-Image edrdn950")
        else:
            title_tag_tuple = ("h1", "class", "sc-518485e5-0 bWszMR")
            text_elements_tuple = ("p", "class", "sc-eb7bd5f6-0 fYAfXe")
            image_tag_tuple = ("img", "class", "sc-814e9212-0 hIXOPW")
            
        title_tag = title_tag_tuple[0]
        title_attribute = title_tag_tuple[1]
        title_value = title_tag_tuple[2]
        
        text_tag = text_elements_tuple[0]
        text_attribute = text_elements_tuple[1]
        text_value = text_elements_tuple[2]
        
        image_tag = image_tag_tuple[0]
        image_attribute = image_tag_tuple[1]
        image_value = image_tag_tuple[2]
        
        title = article.find(title_tag, {title_attribute: title_value}).text
        text_elements = article.find_all(text_tag, {text_attribute: text_value})
        text = []
        for element in text_elements:
            text.append(element.text)
        text_str = "".join(text)
        imgs = article.find_all(image_tag, {image_attribute: image_value})
        for img in imgs:
            images.append((img.get("src"), img.get("alt")))
        return {"title": title, "text": text_str, "images": images, "url": url}
        
    def __call__(self, url: str) -> list:
        list_of_data = []
        self._load_dict_()
        response = self._get_data_(url)
        parser = self._parse_data_(response)
        news = self._get_news_(url, parser)
        hrefs = self._filter_news_(news)
        for href in hrefs:
            #print(href)
            list_of_data.append(self._get_new_data_(href))
        return list_of_data
        
    



b = NewykParser()
a = b("https://www.bbc.com/news")
for i in a:
    print(i)
    print("\n\n")






    

