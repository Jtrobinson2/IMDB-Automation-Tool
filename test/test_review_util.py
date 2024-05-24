import pytest
from src.model.review import Review
from src.util import review_util

class TestReviewUtil:

    def test_validate_markup(self):
        validTagsMap = tagsMap = {'[/spoiler]': '[spoiler]', '[/b]': '[b]'}
    
        validMarkupWithTags = r"""[b]Rating: 10.0[/b] [b]Kyoshi Novels Rating: 9.0[/b] [b]Favourite Episode: Sozin's Comet parts 2-4[/b] Most well-written children's animated show to date. The Series deserves the hype despite it starting out "kiddie" until around episode 3 where [spoiler] The genocide [/spoiler]"""
        validMarkupWithoutTags = r"This is a valid review without tags"
        invalidMarkupWithInvalidClosingTag = r"[b]Rating: 10.0[//b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithInvalidClosingTagType = r"[b]Rating: 10.0[/spoiler] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithNoClosingTags = r"[b]Rating: 10.0[b] [b]Kyoshi Novels Rating: 9.0[/b]"

        assert review_util.validateMarkup(validMarkupWithTags, validTagsMap)
        assert review_util.validateMarkup(validMarkupWithoutTags, validTagsMap)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTag, validTagsMap)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTagType, validTagsMap)
        assert not review_util.validateMarkup(invalidMarkupWithNoClosingTags, validTagsMap)

        with pytest.raises(ValueError) as error:  
            review_util.validateMarkup(None, validTagsMap)
        assert str(error.value) == "Error: please provide a markup string"
        
        with pytest.raises(ValueError) as error:  
            review_util.validateMarkup("Markup ", None)
        assert str(error.value) == "Error: to validate markup we need the tags that are considered valid."

        with pytest.raises(ValueError) as error:  
            review_util.validateMarkup("Markup ", dict())
        assert str(error.value) == "Error: to validate markup we need the tags that are considered valid."        

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
    #TODO refactor this test with new review fields
    def testIsReviewValid(self):
        validTags = {"[/spoiler]" : "[spoiler]", "[/b]": "[b]"}
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

        assert review_util.isReviewValid(validReview, validTags, 1)

        assert not review_util.isReviewValid(invalidReviewProfaneHeadline, validTags, 1)[0]
        assert "Error: review's cannot contain profanity." == review_util.isReviewValid(invalidReviewProfaneHeadline, validTags, 1)[1]
        assert not review_util.isReviewValid(invalidReviewProfaneBody, validTags, 1)[0]
        assert "Error: review's cannot contain profanity." == review_util.isReviewValid(invalidReviewProfaneBody, validTags, 1)[1]
        assert not review_util.isReviewValid(invalidReviewBadMarkup, validTags, 1)[0]
        assert "Error: Invalid Markup" == review_util.isReviewValid(invalidReviewBadMarkup, validTags, 1)[1]
        assert not review_util.isReviewValid(invalidReviewTooShort, validTags, 2)[0]
        assert "Error, review is smaller than the min review length allowed on IMDB." == review_util.isReviewValid(invalidReviewTooShort, validTags, 2)[1]

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewEmptyHeadline, validTags, 1)
        assert str(error.value) == "Error: review must have a headline."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNoneHeadline, validTags, 1)
        assert str(error.value) == "Error: review must have a headline."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewEmptyBody, validTags, 1)
        assert str(error.value) == "Error: review must have a review body."        

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNoneBody, validTags, 1)
        assert str(error.value) == "Error: review must have a review body."

        with pytest.raises(ValueError) as error:  
            review_util.isReviewValid(invalidReviewNotShowOrMovie, validTags, 1)
        assert str(error.value) == "Error: review must be marked as either a TV show or a Movie."
                                