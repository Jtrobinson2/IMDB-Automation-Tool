import pytest
from src.util import review_util



class TestReviewUtil:

    def test_validate_markup(self):
        validMarkupWithTags = r"""[b]Rating: 10.0[/b] [b]Kyoshi Novels Rating: 9.0[/b] [b]Favourite Episode: Sozin's Comet parts 2-4[/b] Most well-written children's animated show to date. The Series deserves the hype despite it starting out "kiddie" until around episode 3 where [spoiler] The genocide [/spoiler]"""
        validMarkupWithoutTags = r"This is a valid review without tags"
        invalidMarkupWithInvalidClosingTag = r"[b]Rating: 10.0[//b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithInvalidClosingTagType = r"[b]Rating: 10.0[/spoiler] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithNoClosingTags = r"[b]Rating: 10.0[b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupIsProfane = "The string was normal until....Cock sucking ass bitch!!"


        assert review_util.validateMarkup(validMarkupWithTags)
        assert review_util.validateMarkup(validMarkupWithoutTags)
        assert not review_util.validateMarkup(invalidMarkupIsProfane)
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
        

        


        
