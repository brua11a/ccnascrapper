if __name__ == "__main__":
    from ccna_scrapper import scrap_ccna, Entries
import re

def page_to_testo(webpage):
    results = []
    answers = ""
    contents = []

    for i in range(len(webpage)):
        content = webpage[i].content
        type = webpage[i].type
        if type == "X" and not(i == 0):
            results.append([answers, contents])
            # print(answers)
            answers = ""
            # print(contents)
            contents = []
        answers += type
        if content.startswith("Case") and type == "X":
            j = i
            while (True):
                if not(webpage[j].content).startswith("Case") and webpage[j].type == "X":
                    content = webpage[j].content
                    break
                j-=1
        contents.append(content)
        if i == len(webpage)-1:
            results.append([answers, contents])
            # print(answers)
            answers = ""
            # print(contents)
            contents = []
    return results

def testo_filter(testo):

    filtered = [
        [
            "X1\n" if item[0] == "X0" else item[0]+"\n",
            [re.sub(r'^\d+\.\s*', '', content) + '\n' if idx < len(item[1]) - 1 else
             re.sub(r'^\d+\.\s*', '', content)
             for idx, content in enumerate(item[1])]
        ]
        for item in testo
        if not item[0] == "X"
    ]
    return filtered

if __name__ == "__main__":
    webpage = scrap_ccna("https://itexamanswers.net/ccna-2-v7-0-final-exam-answers-full-switching-routing-and-wireless-essentials.html", "CCNA 2 (Version 7.00) SRWE Practice Final Exam Answers")
    for result in testo_filter(page_to_testo(webpage)):
        print(result)