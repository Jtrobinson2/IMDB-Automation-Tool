import pytest
from src.model.review import Review
from src.util import review_util



class TestReviewUtil:

    def test_validate_markup(self):
        validMarkupWithTags = r"""[b]Rating: 10.0[/b] [b]Kyoshi Novels Rating: 9.0[/b] [b]Favourite Episode: Sozin's Comet parts 2-4[/b] Most well-written children's animated show to date. The Series deserves the hype despite it starting out "kiddie" until around episode 3 where [spoiler] The genocide [/spoiler]"""
        validMarkupWithoutTags = r"This is a valid review without tags"
        invalidMarkupWithInvalidClosingTag = r"[b]Rating: 10.0[//b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithInvalidClosingTagType = r"[b]Rating: 10.0[/spoiler] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithNoClosingTags = r"[b]Rating: 10.0[b] [b]Kyoshi Novels Rating: 9.0[/b]"
        
        assert review_util.validateMarkup(validMarkupWithTags)
        assert review_util.validateMarkup(validMarkupWithoutTags)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTag)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTagType)
        assert not review_util.validateMarkup(invalidMarkupWithNoClosingTags)

        with pytest.raises(ValueError) as error:  
            review_util.validateMarkup(None)
        assert str(error.value) == "Error: please provide a markup string"

    def test_removeMarkup(self):
        markupPreRemoval = " [b]Rating: 10.0[/b]\n[b]Kyoshi Novels Rating: 9.0[/b]\n[spoiler]The genocide[/spoiler] "
        markupPostRemoval = "Rating: 10.0\nKyoshi Novels Rating: 9.0\nThe genocide"
        tagsToRemove = {"[spoiler]", "[/spoiler]", "[b]", "[/b]"}
        
        assert review_util.removeReviewMarkup(markupPreRemoval, tagsToRemove=tagsToRemove) == markupPostRemoval

        with pytest.raises(ValueError) as error:  
            review_util.removeReviewMarkup("", "[example]")
        assert str(error.value) == "Error: you must submit markup to remove markup."

        with pytest.raises(ValueError) as error:  
            review_util.removeReviewMarkup(None, "[example]")
        assert str(error.value) == "Error: you must submit markup to remove markup."

        with pytest.raises(ValueError) as error:  
            review_util.removeReviewMarkup("Example", set())
        assert str(error.value) == "Error: you must provide at least one type of tag you want to remove"

        with pytest.raises(ValueError) as error:  
            review_util.removeReviewMarkup("Example", None)
        assert str(error.value) == "Error: you must provide at least one type of tag you want to remove"
    
    def testIsReviewValid(self):
        validTagsSet = {"[spoiler]", "[/spoiler]", "[b]", "[/b]"}
        validReview = Review("Clean Headline", "Clean ReviewBody", True, False, True)
        invalidReviewProfaneHeadline = Review("Profane ass headline you CUCK!", "Clean ReviewBody", True, False, True)
        invalidReviewProfaneBody = Review("Clean Headline", "Profane as fuck body", True, False, True)
        invalidReviewEmptyHeadline = Review("", "Clean ReviewBody", True, False, True)
        invalidReviewNoneHeadline = Review(None, "Clean ReviewBody", True, False, True)
        invalidReviewEmptyBody = Review("Clean Headline", "", True, False, True)
        invalidReviewNoneBody = Review("Clean Headline", None, True, False, True)
        invalidReviewNotShowOrMovie = Review("Clean Headline", "Clean ReviewBody", False, False, True)
        invalidReviewBadMarkup = Review("Clean Headline", "This has [b] bad markup [b] [/spoiler] [spoiiler] [/b]", True, False, True)
        invalidReviewTooShort = Review(".", ".", True, False, True)

        assert review_util.isReviewValid(validReview, validTagsSet, 1)

        assert not review_util.isReviewValid(invalidReviewProfaneHeadline, validTagsSet, 1)[0]
        assert "Error: review's cannot contain profanity." == review_util.isReviewValid(invalidReviewProfaneHeadline, validTagsSet, 1)[1]
        assert not review_util.isReviewValid(invalidReviewProfaneBody, validTagsSet, 1)[0]
        assert "Error: review's cannot contain profanity." == review_util.isReviewValid(invalidReviewProfaneBody, validTagsSet, 1)[1]
        assert not review_util.isReviewValid(invalidReviewBadMarkup, validTagsSet, 1)[0]
        assert "Error: Invalid Markup" == review_util.isReviewValid(invalidReviewBadMarkup, validTagsSet, 1)[1]
        assert not review_util.isReviewValid(invalidReviewTooShort, validTagsSet, 2)[0]
        assert "Error, review is smaller than the min review length allowed on IMDB." == review_util.isReviewValid(invalidReviewTooShort, validTagsSet, 2)[1]

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewEmptyHeadline, validTagsSet, 1)
        assert str(error.value) == "Error: review must have a headline."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNoneHeadline, validTagsSet, 1)
        assert str(error.value) == "Error: review must have a headline."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewEmptyBody, validTagsSet, 1)
        assert str(error.value) == "Error: review must have a review body."        

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNoneBody, validTagsSet, 1)
        assert str(error.value) == "Error: review must have a review body."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNotShowOrMovie, validTagsSet, 1)
        assert str(error.value) == "Error: review must be marked as either a TV show or a Movie."
                                
        

        


        
