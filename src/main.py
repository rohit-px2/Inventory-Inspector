import stock_checker
import sys
import os

def main() -> None:
    file_name : str = os.getcwd() + "\links.txt"
    txtfile = open(file_name)
    links = []
    for link in txtfile:
        links.append(link)
    sleep_time : float = float(input("How many seconds to wait before checking again? \n"))
    stock_checker.check_stock(links, sleep_time)
    

if __name__ == "__main__":
    main()
