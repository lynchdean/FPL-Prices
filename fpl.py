from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import getpass
import re
import time

status = {
    "A" : "Active",
    "I" : "Inactive"
    }

position = {
    "G" : "Goal Keeper",
    "D" : "Defender",
    "M" : "Midfielder",
    "F" : "Forward"
    }

space_teams = ["CrystalPalace", "ManCity", "ManUtd", "WestHam"]

def stats():
    url = "http://www.fplstatistics.co.uk/Home/"
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get(url)

    extend_table = Select(driver.find_element_by_name('myDataTable_length'))
    extend_table.select_by_value("50")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    rows = []
    for line in soup.findAll(True, {"class":["odd", "even"]}):
       rows.append(line)

    for row in rows:
        if str(row).find("double-up") != -1:
            row.append("UP+")
        elif str(row).find("angle-up") != -1:
            row.append("UP")
        elif str(row).find("double-down") != -1:
            row.append("DOWN+")
        else:
            row.append("DOWN")

    players = [re.sub("<.*?>", " ", str(row).strip()).split() for row in rows]

    for player in players:
        player.pop(-3)

        if player[-6] + player[-5] in space_teams:
            player[-5] = player[-5] + " " + player[-4]
            player.pop(-5)

        if len(player) == 7:
            player[0] = player[0] + " " + player[1]
            player.pop(1)

        player[-4] = position[player[-4]]
        player[-3] = status[player[-3]]
        player[0] = player[0] + " " * (16 - len(player[0]))
        player[1] = player[1] + " " * (12 - len(player[1]))
        player[2] = player[2] + " " * (11 - len(player[2]))
        player[3] = player[3] + " " * (8 - len(player[3]))
        player[4] = player[4] + " " * (5 - len(player[4]))
        player[5] = player[5] + " " * (5 - len(player[5]))

        print("| " + " | ".join(player) + " |")


def main():
    """
    print "Username:",
    username = raw_input()
    password = getpass.getpass()
    print("")
    """

    stats()

if __name__ == '__main__':
    main()
