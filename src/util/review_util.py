"""Module that contains helper functions that manipulate validate the elements of a review before submisison"""
from src.model.review import Review
from better_profanity import profanity
import re 

def removeReviewMarkup(reviewBody : str) -> str:
    """Removes the markup (spoiler tags n such) from a review

    Args:
        reviewBody (str): review body of a review 

    Returns:
        str: cleaned string without markup for review 

    Raises:
        ValueError: If reviewBody is empty or none
    """  
    pass

def isReviewValid(review : Review):
    """Checks the fields of a review to ensure they are valid for submission

    Args:
        review (Review): review to verify 

    Raises:
        ValueError: If review's headline is none, empty, or contains profanity or markup.
        ValueError: If review's review body is none, empty, or contains profanity or invalid markup.
        ValueError: If review's not demarked as either a movie or tv show or both.
        ValueError: if reviews review body is < 600 characters
    """  
    pass 

def validateMarkup(markupString : str, minStringLength : int) -> bool:
    """Validates that the markup is correct (all opening tags and closing tags are correct, review markup is long enough etc). 

    Args:
        markupString (str): markup string 

    Returns:
        Bool: True if the markup string is valid 

    Raises:
        ValueError: If markupString is empty or none
    """  

    if(not markupString):
        raise ValueError("Error: please provide a markup string")
    if( len(markupString) < minStringLength):
        return False
    if(profanity.contains_profanity(markupString)):
        return False
    
    #match all [spoiler],  [/spoiler] or [b] [/b] tags into one group, while "matching" (skipping) all the characters between the opening and closing tags
    tagsMap = {'[/spoiler]': '[spoiler]', '[b]': '[/b]'}

    #keep track of all the open tags we've seen
    openTagsStack = []

    for character in markupString:
        if (character in tagsMap and openTagsStack):
            topOfStack = openTagsStack[-1]
            #if we have the correct opener for the corresponding closer we just processed
            if(topOfStack == tagsMap[character]):
                openTagsStack.pop()
            else:
                return False        
        else:
            openTagsStack.append(character)
    #stack should have no openers if we had all the right pairs
    return len(openTagsStack) == 0



