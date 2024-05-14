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
    
    reviewBody = reviewBody.strip()
    for tag in tagsToRemove: reviewBody = reviewBody.replace(tag, "")
    return reviewBody

def isReviewValid(review : Review, validTags = dict[str, str], minReviewLength=600) -> tuple[bool, str]:
    """Checks the fields of a review to ensure they are valid for submission no profanity valid tags etc.

    Args:
        review (Review): review to verify 
        validTags (dict[str, str]) : valid tags that can occur in the review body (CLOSING TAGS MUST BE THEY KEY. OPENING THE VALUE)

    Raises:
        ValueError: If review's headline is none, empty, or contains profanity or markup.
        ValueError: If review's review body is none, empty, or contains profanity or invalid markup.
        ValueError: If review's not demarked as either a movie or tv show or both.
        ValueError: if reviews review body is < the minimum review character cutoff for IMDB 
    """ 
    if(not review.headline):
        raise ValueError("Error: review must have a headline.")
    if(not review.reviewBody):
        raise ValueError("Error: review must have a review body.")
    if(not review.isMovie and not review.isTVShow):
        raise ValueError("Error: review must be marked as either a TV show or a Movie.")

    if(not validateMarkup(review.reviewBody, validTags)):
        return False, "Error: Invalid Markup"
    if(profanity.contains_profanity(review.reviewBody) or profanity.contains_profanity(review.headline)):
        return False, "Error: review's cannot contain profanity."

    review.reviewBody = removeReviewMarkup(review.reviewBody, validTags)

    if(len(review.reviewBody) < minReviewLength):
        return False, "Error, review is smaller than the min review length allowed on IMDB."
    
    return True


def validateMarkup(markupString : str, validTags : dict[str,str]) -> bool:
    """Validates that the markup is correct (all opening tags and closing tags are correct). 

    Args:
        markupString (str): markup string
        validTags dict[str : str]: valid tags that can be in the string. YOU MUST PASS 
        A MAP WITH closing tags as the key and open tags as the value e.g ([/spoiler] : [spoiler]) 

    Returns:
        Bool: True if the markup string is valid 

    Raises:
        ValueError: If markupString is empty or none
        ValueError: If valid tags is empty or None
    """  
    if(not markupString):
        raise ValueError("Error: please provide a markup string")
    if(not validTags):
        raise ValueError("Error: to validate markup we need the tags that are considered valid.")
    
    #recurisive function that validates the string one tag at a time breaking the string down after each opening tag is found
    def validateTags(openTagsStack : list[str], remainingStringToCheck : str) -> bool:        
        #base case no open tags without a closer and no string left we're good
        if(not remainingStringToCheck):
            return not openTagsStack
        
        #get the next opening tag 
        nextTagsFoundList = []
        for key, value in validTags.items():
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
        if(nextTagTuple[0] not in validTags):
            openTagsStack.append(nextTagTuple[0])
            return validateTags(openTagsStack, remainingStringToCheck[nextTagTuple[1] + len(nextTagTuple[0]):])
        
        #if the next tag is an closer check the top of the stack for it's opener
        elif(nextTagTuple[0] in validTags):
            #the last tag we've seen should be the corresponding opener 
            if(openTagsStack[-1] == validTags[nextTagTuple[0]]):
                openTagsStack.pop()
                return validateTags(openTagsStack, remainingStringToCheck[nextTagTuple[1] + len(nextTagTuple[0]):])
            else:
                return False
            
        return True
    
    return validateTags([], markupString)