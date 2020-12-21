# Stock_Check
A web-scraping Python program to check the stock of any links the user puts in.
Uses the "requests" library to get the content of each page and then parses it with BeautifulSoup.
Works for Canada Computers, Memory Express, Bestbuy and Newegg (Canadian versions).

## Run Instructions
First, install the requirements listed in "requirements.txt". You can make this easier by typing <br />
<code> > pip install -r requirements.txt </code> in the command line. <br />
Next, add the links you want to check into "links.txt", with a newline separating each link. <br />
Then, run the following instructions in your command line (Windows): <br />
<code> > git clone https://github.com/rohit-px2/Stock_Check.git Stock_Check </code> <br />
<code> > cd Stock_Check </code> <br />
<code> > cd src </code> <br />
<code> > python main.py </code>. <br />