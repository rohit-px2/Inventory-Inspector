import stock_checker
import sys
import os


def main() -> None:
    os.chdir("..")
    file_name : str = os.getcwd() + "\links.txt"
    txtfile = open(file_name)
    links = []
    for link in txtfile:
        links.append(link)
    stock_checker.check_stock(links)
    

if __name__ == "__main__":
    main()
