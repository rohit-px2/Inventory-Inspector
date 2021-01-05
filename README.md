# Stock_Check
A web-scraping Python program to check the stock of any links the user puts in.
Uses the "requests" library to get the content of each page and then parses it with BeautifulSoup.
Works for Canada Computers, Memory Express, Bestbuy and Newegg (Canadian versions, American versions untested).

## Run Instructions
Add the links you want to check into "links.txt", with a newline separating each link. <br />
Then, run the following instructions in your command line (Windows): <br />
<code> > git clone https://github.com/rohit-px2/Stock_Check.git Stock_Check </code> <br />
<code> > cd Stock_Check </code> <br />
<code> > pip install -r requirements.txt </code> to install requirements (only need to do this once) <br />
If your Python version is less than 3.2, you must run <code> > pip install futures</code>. Otherwise you do
not need to do anything. Then <br />
<code> > cd src </code> <br />
<code> > python main.py</code> to run. Enter the interval time and the program will begin checking stock!

## Testing
To run tests, you need [Pytest](https://pypi.org/project/pytest/). To install Pytest, type <br />
<code> > pip install pytest </code>  into your console. Then to run the tests, navigate to the parent directory
of the project and type <br>
<code> > pytest </code>  to run the automated tests.