import pytest
from src.util import review_util



class TestReviewUtil:

    def test_validate_markup(self):
        validMarkupWithTags = r"""[b]Rating: 10.0[/b] [b]Kyoshi Novels Rating: 9.0[/b] [b]Favourite Episode: Sozin's Comet parts 2-4[/b] Most well-written children's animated show to date. The Series deserves the hype despite it starting out "kiddie" until around episode 3 where [spoiler] The genocide [/spoiler]"""
        validMarkupWithoutTags = r"This is a valid review without tags"
        invalidMarkupWithInvalidClosingTag = r"[b]Rating: 10.0[//b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithInvalidClosingTagType = r"[b]Rating: 10.0[/spoiler] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupWithNoClosingTags = r"[b]Rating: 10.0[b] [b]Kyoshi Novels Rating: 9.0[/b]"
        invalidMarkupToShort = "L"
        invalidMarkupIsProfane = "The string was normal until....Cock sucking ass bitch!!"


        assert review_util.validateMarkup(validMarkupWithTags, 1)
        assert review_util.validateMarkup(validMarkupWithoutTags, 1)
        assert not review_util.validateMarkup(invalidMarkupIsProfane, 1)
        assert not review_util.validateMarkup(invalidMarkupToShort, 2)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTag, 1)
        assert not review_util.validateMarkup(invalidMarkupWithInvalidClosingTagType, 1)
        assert not review_util.validateMarkup(invalidMarkupWithNoClosingTags, 1)

        with pytest.raises(ValueError) as error:  
            review_util.validateMarkup(None, 1)
        assert str(error.value) == "Error: please provide a markup string"
        

        


        
