from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.ie.webdriver import WebDriver
from .models import ToDoList, ListItem
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Test the toggle functionality
    def test_list_item_toggle(self): 
        self.test_list_item.isCompleted = not self.test_list_item.isCompleted
        test_isCompleted = self.test_list_item.isCompleted 
        self.test_list_item.save()

        # Re-Fetch objects form DB (Use the primary key)
        test_task = ListItem.objects.get(pk = self.test_list_item.pk)
        self.assertEqual(test_task.isCompleted, test_isCompleted)

# Testing the dashboard view 
class TestDashboardView(TestCase): 

    # setUp Method 
    def setUp(self): 
        User = get_user_model()
        self.client = Client()
        self.user_pswd = "123456789"
        self.test_user = User.objects.create_user(username= "test_username", email="test_email@gmail.com", password=self.user_pswd)

        self.client.login(username=self.test_user.username, password=self.user_pswd)
        self.test_list = ToDoList.objects.create(user= self.test_user, name= "Test_List" )
        self.test_task = ListItem.objects.create(list=self.test_list, text= "Dummy test text")

    # Test dashboard loading for logeed in users 
    def test_dashboard_loads_for_logged_in_user(self): 
        response = self.client.get(reverse('dashboard'))
        
        # Assertion 1: Check HTTP Status Code
        self.assertEqual(response.status_code, 200)

        # Assertion 2: Check Template Used
        self.assertTemplateUsed(response, 'todo_list_app/dashboard.html')

    # Test creating and adding a new ToDoList 
    def test_add_new_list(self): 
        form_data ={
            'form_type': 'add_list',
            'list_name': 'Test New List',
        }

        response = self.client.post(path=reverse('dashboard'), data=form_data )

        lists_count_after = ToDoList.objects.filter(user=self.test_user).count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert number of objects after creation 
        self.assertEqual(lists_count_after, 2)

    # Test creating and adding a new List Item to the test todo list 
    def test_add_new_list_item(self): 
        form_data = {
            'form_type': 'add_list_item', 
            'list_item_text': "Dummy Test Text"
        }

        list_id_kwargs = {
                'list_id': self.test_list.id, 
        }

        response = self.client.post(path=reverse('view_list_items', kwargs=list_id_kwargs), data= form_data)

        lists_count_after = ListItem.objects.filter(list= self.test_list).count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert number of objects after creation 
        self.assertEqual(lists_count_after, 2)

    # Test toggling list items 
    def test_list_item_toggle(self):
        form_data = {
            'form_type': "toggle_task" 
        }

        reverse_kwargs ={
            'list_id': self.test_list.id,
            'task_id': self.test_task.id,
        }

        response = self.client.post(path=reverse('toggle_task', kwargs=reverse_kwargs), data= form_data)

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert task's isCompleted
        toggled_task = ListItem.objects.get(pk=self.test_task.pk)

        self.assertEqual(toggled_task.isCompleted, True)

    # Test task deletion 
    def test_list_item_delete(self): 
        form_data = {
            'form_type': "delete_task",
        }

        reverse_kwargs ={
            'list_id': self.test_list.id,
            'task_id': self.test_task.id,
        }

        response = self.client.post(path=reverse('delete_task', kwargs=reverse_kwargs), data= form_data)

        list_items_count_after = ListItem.objects.filter(list= self.test_list).count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert list items count has decreased by one 
        self.assertEqual(list_items_count_after, 0)

    # Test the deletion of a todo list 
    def test_list_delete(self): 
        form_data = {
            'form_type': "delete_list",
        }

        reverse_kwargs ={
            'list_id': self.test_list.id,
        }

        response = self.client.post(path=reverse('delete_list', kwargs=reverse_kwargs), data=form_data)

        lists_count_after_deletion = ToDoList.objects.filter(user=self.test_user).count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert lists count after deletion 
        self.assertEqual(lists_count_after_deletion, 0)

# Testig the registeration view 
class TestRegisterView(TestCase):

    # setUp Method 
    def setUp(self):
        self.User = get_user_model()
        self.client = Client()

    # Test the normal scenario of registeration
    def test_successful_registration(self): 
        form_data = {
            'username': "test_username",
            'email': "test_email@gmail.com",
            'password': "12345678",
            'confirm_password': "12345678",
        }

        response = self.client.post(path=reverse('register') ,data=form_data)

        users_count = self.User.objects.count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert user creation 
        self.assertEqual(users_count ,1)

    # Test the registeration of mismatching password and confirm password fields 
    def test_failed_registeration_pswd_mismatch(self): 
        form_data = {
            'username': "test_username",
            'email': "test_email@gmail.com",
            'password': "12345678",
            'confirm_password': "12345679",
        }

        response = self.client.post(path=reverse('register') ,data=form_data)

        users_count = self.User.objects.count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert user creation 
        self.assertEqual(users_count ,0)   

    # Test the registeration of Invalid E-mail format 
    def test_failed_registeration_invld_mail(self): 
        form_data = {
            'username': "test_username",
            'email': "invalid_mail",
            'password': "12345678",
            'confirm_password': "12345678",
        }

        response = self.client.post(path=reverse('register') ,data=form_data)

        users_count = self.User.objects.count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert user creation 
        self.assertEqual(users_count ,0)   

    # Test the registeration of a username that has been registered before 
    def test_failed_registeration_unique_username(self): 
        form_data = {
            'username': "test_username",
            'email': "test_email@gmail.com",
            'password': "12345678",
            'confirm_password': "12345678",
        }

        response = self.client.post(path=reverse('register') ,data=form_data)

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        form_data['email'] = "test2_email@gmail.com"

        response = self.client.post(path=reverse('register') ,data=form_data)

        users_count = self.User.objects.count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert user creation 
        self.assertEqual(users_count ,1)  

    # Test the registeration of an e-mail that has been registered before 
    def test_failed_registeration_unique_email(self): 
        form_data = {
            'username': "test_username",
            'email': "test_email@gmail.com",
            'password': "12345678",
            'confirm_password': "12345678",
        }

        response = self.client.post(path=reverse('register') ,data=form_data)

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        form_data['username'] = "test2_username"

        response = self.client.post(path=reverse('register') ,data=form_data)

        users_count = self.User.objects.count()

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert user creation 
        self.assertEqual(users_count ,1)  

class TestLoginView(TestCase): 

    # setUp Method
    def setUp(self): 
        User = get_user_model()
        self.client = Client()
        self.test_password = "12345678"
        self.test_user = User.objects.create_user(username="dummy_test_user", password= self.test_password)

    # Test the normal login scenario 
    def test_successfull_login(self): 
        form_data = {
            'username': self.test_user.username,
            'password': self.test_password,
        }

        response = self.client.post(path=reverse('login'), data= form_data )

        session_user_id = self.client.session.get('_auth_user_id')

        # Assert HTTP status code
        self.assertEqual(response.status_code, 302)

        # Assert the session key 
        self.assertEqual(session_user_id, f"{self.test_user.id}")
    
    # Test the normal faliure scenario wrong username or password  
    def test_failure_login(self): 
        form_data = {
            'username': "wrong_user_name",
            'password': self.test_password,
        }

        response = self.client.post(path=reverse('login'), data= form_data )

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)


class UserJourneyText(LiveServerTestCase): 

    # setUp Method 
    def setUp(self): 
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
         
        self.web_driver = webdriver.Chrome(options= options)
        self.wait = WebDriverWait(self.web_driver, 10)

    # tearDown Method 
    def tearDown(self): 
        self.web_driver.quit()

    # Test the full registeration flow 
    def test_full_registeration_and_login(self): 
        # Navigate to the home page from the bas URL   
        self.web_driver.get(url=f"{self.live_server_url}")

        # Get the regiter element by text  
        register_element = self.web_driver.find_element(by=By.LINK_TEXT, value="Register")

        # Click the link
        register_element.click()

        register_page_url = self.live_server_url + reverse('register')
        self.assertEqual(self.web_driver.current_url, register_page_url )

        # Access the form input fields 
        form_reg_username_element = self.web_driver.find_element(by=By.ID, value="id_username")
        form_reg_email_element = self.web_driver.find_element(by=By.ID, value="id_email")
        form_reg_pswd_element = self.web_driver.find_element(by=By.ID, value="id_password1")
        form_reg_confirm_pswd_element = self.web_driver.find_element(by=By.ID, value="id_password2")

        # Accessing the button element 
        form_register_btn = self.web_driver.find_element(by=By.TAG_NAME, value="button")

        # Fill in the form programaticaly 
        form_reg_username_element.send_keys("Dummy-User-Name")
        form_reg_email_element.send_keys("dummy@gmail.com")
        form_reg_pswd_element.send_keys("12345678")
        form_reg_confirm_pswd_element.send_keys("12345678")

        # Pressing the register button 
        form_register_btn.click()
        
        # Check landing to login page 
        login_page_url = self.live_server_url + reverse('login')
        self.wait.until(EC.url_to_be(login_page_url))
        self.assertEqual(self.web_driver.current_url, login_page_url )

        form_log_username_element = self.web_driver.find_element(by=By.ID, value="id_username")
        form_log_pswd_element = self.web_driver.find_element(by=By.ID, value="id_password")
        form_login_btn = self.web_driver.find_element(by=By.TAG_NAME, value="button")

        # Fill in the form
        form_log_username_element.send_keys("Dummy-User-Name")
        form_log_pswd_element.send_keys("12345678")

        # press the login btn
        form_login_btn.click()

        dashboard_page_url = self.live_server_url + reverse('dashboard')
        self.wait.until(EC.url_to_be(dashboard_page_url))
        self.assertEqual(self.web_driver.current_url, dashboard_page_url)

