from todo_app.data.session_items import ViewModel,Card,List
from datetime import datetime,timedelta

class Test_Items_ToDo:

    @staticmethod
    def test_to_do_items():

        # Arrange
        to_do_item = Card('123', 'To Do', '987', '', '', datetime.utcnow())
        to_do_list = List('987', 'To Do')

        # Act
        view_model = ViewModel([to_do_item],[to_do_list])

        # Assert
        assert len(view_model.items) == 1
        assert len(view_model.to_do_items) == 1

class Test_Items_Doing:

    @staticmethod
    def test_doing_items():

        # Arrange
        doing_item = Card('234', 'Doing', '876', '', '', datetime.utcnow())
        doing_list = List('876', 'Doing')

        # Act
        view_model = ViewModel([doing_item],[doing_list])

        # Assert
        assert len(view_model.items) == 1
        assert len(view_model.doing_items) == 1
        
class Test_Items_Done:

    @staticmethod
    def test_done_items():

        # Arrange
        done_item = Card('345', 'Done', '765', '', '', datetime.utcnow())

        # Act
        view_model = ViewModel([done_item],[])

        # Assert
        assert len(view_model.items) == 1

class Test_Lists:

    @staticmethod
    def test_lists():

        # Arrange
        done_list = List('765', 'Done')

        # Act
        view_model = ViewModel([],[done_list])

        # Assert
        assert len(view_model.lists) == 1

class Test_Show_All_Done_Items:

    @staticmethod
    def test_show_all_done_items():

        # Arrange
        done_item_today1 = Card('345', 'Done', '765', '', '', datetime.utcnow())
        done_item_today2 = Card('345', 'Done', '765', '', '', datetime.utcnow())
        done_item_old1 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_item_old2 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_item_old3 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_list = List('765', 'Done')

        # Act
        view_model_true = ViewModel([done_item_today1,done_item_today2],[done_list])
        view_model_false = ViewModel([done_item_today1,done_item_today2,done_item_old1,done_item_old2,done_item_old3],[done_list])

        # Assert
        assert len(view_model_true.items) == 2
        assert view_model_true.show_all_done_items is True
        assert len(view_model_true.older_done_items) == 0
        assert len(view_model_true.recent_done_items) == 2
        assert len(view_model_false.items) == 5
        assert view_model_false.show_all_done_items is False
        assert len(view_model_false.older_done_items) == 3
        assert len(view_model_false.recent_done_items) == 2

class Test_Recent_Done_Items:

    @staticmethod
    def test_recent_done_items():

        # Arrange
        done_item_old = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_list = List('765', 'Done')

        # Act
        view_model = ViewModel([done_item_old],[done_list])

        # Assert
        assert len(view_model.items) == 1
        assert view_model.show_all_done_items is True
        assert len(view_model.older_done_items) == 1

class Test_Older_Done_Items:

    @staticmethod
    def test_older_done_items():

        # Arrange
        done_item_today = Card('345', 'Done', '765', '', '', datetime.utcnow())
        done_list = List('765', 'Done')

        # Act
        view_model = ViewModel([done_item_today],[done_list])

        # Assert
        assert len(view_model.items) == 1
        assert view_model.show_all_done_items is True
        assert len(view_model.recent_done_items) == 1

class Test_All:

    @staticmethod
    def test_all():

        # Arrange
        to_do_item = Card('123', 'to_do', '987', '', '', datetime.utcnow())
        doing_item = Card('234', 'doing', '876', '', '', datetime.utcnow())
        done_item_today1 = Card('345', 'Done', '765', '', '', datetime.utcnow())
        done_item_today2 = Card('345', 'Done', '765', '', '', datetime.utcnow())
        done_item_old1 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_item_old2 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        done_item_old3 = Card('345', 'Done', '765', '', '', (datetime.utcnow()- timedelta(days=2)))
        to_do_list = List('987', 'To Do')
        doing_list = List('876', 'Doing')
        done_list = List('765', 'Done')

        # Act
        view_model = ViewModel([to_do_item,doing_item,done_item_today1,done_item_today2,done_item_old1,done_item_old2,done_item_old3],[to_do_list,doing_list,done_list])

        # Assert
        assert len(view_model.items) == 7
        assert len(view_model.lists) == 3
        assert len(view_model.to_do_items) == 1
        assert len(view_model.doing_items) == 1
        assert view_model.show_all_done_items is False
        assert len(view_model.recent_done_items) == 2
        assert len(view_model.older_done_items) == 3