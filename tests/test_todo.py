from todo_app.data.session_items import *

class TestGetCards_ToDo:

    @staticmethod
    def test_to_do_items():

        # Arrange
        list_id = '6023b202e61c2b748a497dea'

        # Act
        cards = get_cards_from_list(list_id)

        # Assert
        assert len(cards) == 2

class TestGetCards_Doing:

    @staticmethod
    def test_to_do_items():

        # Arrange
        list_id = '6023b202e61c2b748a497deb'

        # Act
        cards = get_cards_from_list(list_id)

        # Assert
        assert len(cards) == 1
        
class TestGetCards_Done:

    @staticmethod
    def test_to_do_items():

        # Arrange
        list_id = '6023b202e61c2b748a497dec'

        # Act
        cards = get_cards_from_list(list_id)

        # Assert
        assert len(cards) == 7

class TestGetLists:

    @staticmethod
    def test_get_lists():

        # Arrange

        # Act
        lists = get_lists()

        # Assert
        assert len(lists) == 3

class TestGetRecentDoneItems:

    @staticmethod
    def test_get_lists():

        # Arrange
        cards = get_cards_from_list('6023b202e61c2b748a497dec')

        # Act
        recent_items = recent_done_items(cards)

        # Assert
        assert len(recent_items) == 1

class TestGetOlderDoneItems:

    @staticmethod
    def test_get_lists():

        # Arrange
        cards = get_cards_from_list('6023b202e61c2b748a497dec')

        # Act
        recent_items = older_done_items(cards)

        # Assert
        assert len(recent_items) == 6