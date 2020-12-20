import stock_checker

def main():
    links = []
    link = input("Paste your links here, and type \"end\" to end.")
    while link != 'end':
        links.append(link)
    stock_checker.check_stock(links)
    

if __name__ == "__main__":
    main()
