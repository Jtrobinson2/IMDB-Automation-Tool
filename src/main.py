from pathlib import Path
import sys

# Get the directory where the script is located
script_path = Path(__file__).resolve()
# Get the parent directory
parent_dir = script_path.parent.parent
sys.path.append( str(parent_dir) )

from src.web_controller import web_actions
from src.model.review import Review
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)

headine = "This is a test headline"
reviewBody = """Wayyy to much romantic melodrama in this. 
The opening scene was Harry about the get laid and the ending scene (right after Dumbledore's funeral) was Hermione talking to Harry about "snogging" Ginny. 
That and having to watch the melodrama of Ron getting it on with comically crazy Lavender Brown while Hermione implodes and Harry avoids getting drugged by yet another love interest was cringe and disrupted the otherwise dark tone of the film. 
Many pivotal scenes in this didn't really make sense such as why Harry didn't just use the water spell directly in Dumbledore's mouth when he couldn't spoon feed him water, why Bellatrix randomly attacked the burrow (they can't harm harry so what's the point), or why Snape refers to himself as the Half blood prince. 
Why did he even decide to to become a death eater. Last movie he was teaching Harry how to protect his mind from Voldemort but it's unclear why he changed sides (this may be revealed in the subsequent movie). 
The revelation of the half blood prince as well as Dumbledore's death was weirdly anticlimactic since one revelation had zero leadup and the other suspends your disbelief that the most powerful wizard alive would go down to Snape without a fight. 
One could argue this is ok because he was weakened but a weakened master should still solo an advanced magic user. This entry was a tonal mess, that relied to heavily on corny interpersonal 
conflicts however we got to see more of Tom riddle pre-deformation which was the highlight of this film."""
itemTitle = "Frieren: Beyond Journey's End"

web_actions.login(driver, "03jrob@gmail.com", "testpass", "TestAccount")
web_actions.submitReview(driver, Review("This is a test headline", reviewBody, True, False, itemTitle, 10, False))