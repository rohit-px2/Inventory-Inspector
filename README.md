# Inventory Inspector
### Check the online inventory of electronics retailers
Inventory Inspector is a Python GUI tool made using PyQt5. The handling of links is done with a combination of BeautifulSoup and the integrated Requests library. <br>
So far, the program supports Canada Computers, Newegg (CA), BestBuy (CA), and MemoryExpress, but more retailers may be added in the future.

## Supported Websites
<ul>
	<li>Canada Computers</li>
	<li>BestBuy (CA)</li>
	<li>Newegg (CA)</li>
	<li>Memory Express</li>
</ul>

## Run Instructions
Add the links you want to check into "links.txt", with a newline separating each link. <br />
Then, run the following instructions in your command line (Windows): <br />
<code>git clone https://github.com/rohit-px2/Inventory-Inspector.git Inventory-Inspector</code> <br />
<code>cd Inventory-Inspector</code> <br />
<codepip install -r requirements.txt </code> to install requirements (only need to do this once) <br />
If your Python version is less than 3.2, you must run <code> > pip install futures</code>. Otherwise you do
not need to do anything. Then <br />
<code>cd src</code> <br />
<code>python main.py</code> to run. Enter the interval time and the program will begin checking stock!

## Testing
To run tests, you need [Pytest](https://pypi.org/project/pytest/). To install Pytest, type <br />
<code> > pip install pytest </code>  into your console. <br/> To run the tests, navigate to the parent directory
of the project, <code>cd test</code> and run <code>pytest</code>