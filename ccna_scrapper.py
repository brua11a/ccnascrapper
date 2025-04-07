from selenium import webdriver
from bs4 import BeautifulSoup

class Entries:
    def __init__(self, content, type):
        self.content = content
        self.type = type

def scrap_ccna(url, ender):

    web_content = []

    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    elements = soup.find_all(
        lambda tag: (
            tag.name in ["p", "li"] or
            (tag.name == "div" and tag.get("class") == ["wp-caption", "aligncenter"])
        )
    )

    flag = False

    for element in elements:
        if element.name in ["p", "div"]:
            image = Entries(None, "0")
            question = Entries(None, "X")
            img = element.find("img")
            if img:
                image.content = img["src"]
            text = element.get_text(strip=True)
            if text.startswith("1."):
                flag = True
            if text == ender:
                break
            if flag==True and not (text.startswith("Exp") or text.startswith("CCNA") or text.startswith("Reference")):
                question.content = text
            if question.content:
                web_content.append(question)
            if image.content:
                web_content.append(image)
        elif element.name == "li" and flag == True:
            answer = Entries(None, "0")
            answer.content = element.get_text(strip=True)
            span = element.find("span")
            corr = "correct_answer" in element.get("class", "")
            if span or corr:
                answer.type = "1"
            web_content.append(answer)

    return web_content


if __name__ == "__main__":
    res = scrap_ccna("https://itexamanswers.net/ccna-2-v7-0-final-exam-answers-full-switching-routing-and-wireless-essentials.html", "CCNA 2 (Version 7.00) SRWE Practice Final Exam Answers")
    for item in res:
        print(item)
        print(item.content, item.type)