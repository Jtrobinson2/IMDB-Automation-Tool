"""Module that contains helper functions that manipulate validate the elements of a review before submisison"""
from src.model.review import Review
from better_profanity import profanity

def removeReviewMarkup(reviewBody : str, tagsToRemove : set[str]) -> str:
    """Removes the markup (spoiler tags n such) from a review

    Args:
        reviewBody (str): review body of a review 
        tagsToRemove (set): set of tags that that you want to be removed from the string 

    Returns:
        str: cleaned string without markup for review 

    Raises:
        ValueError: If reviewBody is empty or none
        ValueError: If the set of tags to remove is empty
    """  

    if(not reviewBody):
        raise ValueError("Error: you must submit markup to remove markup.")
    if(not tagsToRemove):
        raise ValueError("Error: you must provide at least one type of tag you want to remove")
    
    cleanedString = reviewBody
    #remove leading and trailing whitespace 
    cleanedString = cleanedString.strip()
    #for each tag in the set
    for tag in tagsToRemove: 
        #remove that tag from the string
        cleanedString = cleanedString.replace(tag, "")
    
    return cleanedString

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
    
    #recurisive function that validates the string one tag at a time breaking the string down after each opening tag is found
    def validateTags(openTagsStack : list[str], remainingStringToCheck : str) -> bool:        
        #base case no open tags without a closer and no string left we're good
        if(not remainingStringToCheck):
            return not openTagsStack
        
        #get the next opening tag 
        nextTagsFoundList = []
        for key, value in tagsMap.items():
            keyTagTuple = (key, remainingStringToCheck.find(key))
            valueTagTuple = (value ,remainingStringToCheck.find(value))
            #only append tags actually found in the string
            if(keyTagTuple[1] != -1):
                nextTagsFoundList.append(keyTagTuple)
            if(valueTagTuple[1] != -1):
                nextTagsFoundList.append(valueTagTuple)

        #if there's no tags either we processed them all or the string had no tags return true.
        if(not nextTagsFoundList): return True
        
        #order the list so the first tuple is the one that contains the tag found earliest in the string
        nextTagTuple = sorted(nextTagsFoundList, key= lambda elem : elem[1])[0]

        #if the next tag is an opener append it to the stack and keep processing
        if(nextTagTuple[0] not in tagsMap):
            openTagsStack.append(nextTagTuple[0])
            return validateTags(openTagsStack, remainingStringToCheck[nextTagTuple[1] + len(nextTagTuple[0]):])
        
        #if the next tag is an closer check the top of the stack for it's opener
        elif(nextTagTuple[0] in tagsMap):
            #the last tag we've seen should be the corresponding opener 
            if(openTagsStack[-1] == tagsMap[nextTagTuple[0]]):
                openTagsStack.pop()
                return validateTags(openTagsStack, remainingStringToCheck[nextTagTuple[1] + len(nextTagTuple[0]):])
            else:
                return False
            
        return True
    
    return validateTags([], markupString)