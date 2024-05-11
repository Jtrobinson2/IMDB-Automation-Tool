"""Module that contains helper functions that manipulate validate the elements of a review before submisison"""
from src.model.review import Review
from better_profanity import profanity
import sys
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

    tagsMap = {'[/spoiler]': '[spoiler]', '[/b]': '[b]'}

    spoilerTagLen = len("[spoiler]")
    boldTagLen = len("[b]")
    spoilerTagCloserLen = spoilerTagLen + 1
    boldTagCloserLen = boldTagLen + 1
    

    # [b]Rating: 10.0[//b] [b]Kyoshi Novels Rating: 9.0[/b]

    #recurisive function that validates the string one tag at a time breaking the string down after each opening tag is found
    def validateTags(openTagsStack : list[str], remainingStringToCheck : str) -> bool:        
        #base case there is no string left check that the stack is empty and return true
        if(not remainingStringToCheck):
            print(f"Ran out of string tags stack evaluates to {not openTagsStack}")
            return not openTagsStack
        
        #check which opening tag you find first
        firstSpoilerOpenerOccurence =  remainingStringToCheck.find('[spoiler]') if remainingStringToCheck.find('[spoiler]') != -1 else sys.maxsize 
        firstBoldOpenerOccurence =  remainingStringToCheck.find('[b]') if remainingStringToCheck.find('[b]') != -1 else sys.maxsize 

        if(firstSpoilerOpenerOccurence < firstBoldOpenerOccurence):
            #if you find an opener push this onto the opener stack  
                print(f"found spoiler opener append to stack of length {len(openTagsStack)}")
                openTagsStack.append('[spoiler]')
                #pass in the rest of the string after that opener for searching
                validateTags(openTagsStack, remainingStringToCheck[firstSpoilerOpenerOccurence + spoilerTagLen:])
        elif(firstBoldOpenerOccurence < firstSpoilerOpenerOccurence):
                print(f"found bold opener append to stack of length {len(openTagsStack)}")
                openTagsStack.append('[b]')
                #pass in the rest of the string after that opener for searching
                validateTags(openTagsStack, remainingStringToCheck[firstBoldOpenerOccurence + boldTagLen:])
        else:
             #if there are closers in the string the entire string is invalid because we have no openers (this is inefficent)
             for key in tagsMap.keys():
                  if(key in remainingStringToCheck):
                       return False
                              
        #search the remaining string for any closing tags 
        elif(remainingStringToCheck.find('[/spoiler]') != -1):
            #if you find one check that the top of the stack is the opener for that closer
            print(f"found spoiler closer")
            if(openTagsStack[-1] == tagsMap['[/spoiler]']):
                print(f"top of stack matches found spoiler closer popping from stack of length {len(openTagsStack)}")  
                #if it is pop that opener off the stack
                openTagsStack.pop()
                 #continue searching the string for openers
                validateTags(openTagsStack, remainingStringToCheck[remainingStringToCheck.find('[/spoiler]') + spoilerTagCloserLen:])
            else:
                #otherwise it wasn't a match return false
                return False
            
        elif(remainingStringToCheck.find('[/b]') != -1):
            print(f"found bold closer")
            #if you find one check that the top of the stack is the opener for that closer
            if(openTagsStack[-1] == tagsMap['[/b]']):
                print(f"top of stack matches found bold closer popping from stack of length {len(openTagsStack)}")  
                #if it is pop that opener off the stack
                openTagsStack.pop()
                validateTags(openTagsStack, remainingStringToCheck[remainingStringToCheck.find('[/b]') + boldTagCloserLen:])
            else:
                return False
            

    """ [b]Rating: 10.0[/b] [b]Kyoshi Novels Rating: 9.0[/b] 
        [b]Favourite Episode: Sozin's Comet parts 2-4[/b] 
        Most well-written children's animated show to date. 
        The Series deserves the hype despite it starting out "kiddie" 
        until around episode 3 where 
        [spoiler] The genocide [/spoiler]    """
    return validateTags([], markupString)


    # for character in markupString:
    #     if (character in tagsMap and openTagsStack):
    #         topOfStack = openTagsStack[-1]
    #         #if we have the correct opener for the corresponding closer we just processed
    #         if(topOfStack == tagsMap[character]):
    #             openTagsStack.pop()
    #         else:
    #             return False        
    #     else:
    #         openTagsStack.append(character)
    # #stack should have no openers if we had all the right pairs
    # return len(openTagsStack) == 0



