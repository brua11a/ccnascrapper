from testownik_maker import testo_filter, page_to_testo
from ccna_scrapper import scrap_ccna
import os
import urllib.request

def testo_write(directory, base):
    # print(os.getcwd())
    # print(os.getcwd())
    try:
        os.mkdir(directory)
        print(f"Folder na baze '{directory}' stworzony.\n")
    except FileExistsError:
        print(f"Folder na baze '{directory}' już istnial.\n")
    except PermissionError:
        print(f"Brak uprawnien\n")
    except Exception as e:
        print(f"Wyjebka :/ {e}\n")
    os.chdir(directory)
    # print(os.getcwd())
    for i in range(len(base)):
        answers = base[i][0]
        questions = base[i][1]
        for j in range(len(questions)):
            if questions[j].startswith("https"):
                url = questions[j]
                # Add a User-Agent header to the request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                req = urllib.request.Request(url, headers=headers)

                try:
                    with urllib.request.urlopen(req) as response:
                        with open(f"{i+1}.png", 'wb') as out_file:
                            out_file.write(response.read())
                    if answers == "X1":
                        questions[j] = f"[img]{i+1}.png[/img]"
                    else:
                        questions[j] = f"[img]{i + 1}.png[/img]\n"
                except urllib.error.HTTPError as e:
                    print(f"Chuje nie pozwalaja pobrac obrazka kys {url}: {e}\n")
                except Exception as e:
                    print(f"Wyjebka w pobieraniu {url}: {e}\n")


        # print(f"Filename: {i+1}.txt\n", end="")
        # print(answers, end="")
        # print("".join(questions))
        with open(f"{i+1}.txt", "w", encoding="utf-8") as file:
            file.write(answers + "".join(questions))


if __name__ == "__main__":
    webpage = scrap_ccna("https://itexamanswers.net/ccna-2-v7-0-final-exam-answers-full-switching-routing-and-wireless-essentials.html", "CCNA 2 (Version 7.00) SRWE Practice Final Exam Answers")
    base = testo_filter(page_to_testo(webpage))
    # print(base)
    testo_write("BAZASIECI", base)
    # print(os.getcwd())
    # os.chdir("..")
    # print(os.getcwd())