from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ToDoList, ListItem

# Create your tests here.

# Testing the ToDoList Model 
class TestToDoList(TestCase): 

    # setUp Method 
    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user(username= "test_username", email="test_email@gmail.com", password="123456789")
        self.test_list = ToDoList.objects.create(user= self.test_user, name="test_list_1")

    # Test the creation of the ToDoList object 
    def test_todo_list_creation(self): 
        self.assertEqual(self.test_list.user, self.test_user)
        self.assertEqual(self.test_list.name, 'test_list_1')

    # Test the __str__ method for the model
    def test_todo_list_str(self): 
        test_str = str(self.test_list)
        assert_test_str = "A To-Do List for the user: test_username, and title: test_list_1"
        self.assertEqual(test_str, assert_test_str)

# Testing the ListItem Model
class TestListItem(TestCase):

    # setUp Method 
    def setUp(self): 
        User = get_user_model()
        self.test_user = User.objects.create_user(username= "test_username", email="test_email@gmail.com", password="123456789")
        self.test_list = ToDoList.objects.create(user= self.test_user, name="test_list_1")
        self.test_list_item = ListItem.objects.create(list= self.test_list, text= "test_text_1", isCompleted= False)

    # Test the creation of the ListItem object
    def test_list_item_creation(self): 
        self.assertEqual(self.test_list_item.list, self.test_list)
        self.assertEqual(self.test_list_item.text, "test_text_1")
        self.assertEqual(self.test_list_item.isCompleted, False)

    # Test the __str__ method for the model 
    def test_list_item_str(self): 
        test_str = str(self.test_list_item)
        assert_test_str = "A list item in the test_list_1 list, of title test_text_1 and status False"
        self.assertEqual(test_str, assert_test_str)

    def toggle_complete(self):
        self.isCompleted = not self.isCompleted
        self.save()

    # Test the toggle functionality
    def test_list_item_toggle(self): 
        self.test_list_item.toggle_complete()
        # Re-Fetch objects form DB (Use the primary key)
        test_task = ListItem.objects.get(pk = self.test_list_item.pk)
        self.assertEqual(test_task.isCompleted, True)


