import pytest
import os
from threading import Thread
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from todo_app import app
from todo_app.data.session_items import create_board, delete_board
from dotenv import find_dotenv,load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from todo_app.user import TestUser

@pytest.fixture(scope='module')
def app_with_temp_board():
	file_path = find_dotenv('.env')
	load_dotenv(file_path,override=True)

	os.environ['FLASK_ENV'] = "e2e_Test"
	os.environ['MONGO_DATABASE'] = "e2e_Test_Board"
	db = create_board(os.environ.get('MONGO_DATABASE'))

	default_lists = [{"name": "To Do"},{"name": "Doing"},{"name": "Done"}]
	for default_list in default_lists:
		db.lists.update_one(default_list,{"$set": default_list},True)
	
	test_app = app.create_app()
	test_app.config['LOGIN_DISABLED'] = True
	
	thread = Thread(target=lambda: test_app.run(use_reloader=False))
	thread.daemon = True
	thread.start()
	yield test_app
	
	thread.join(1)
	#delete_board("e2e_Test_Board")

@pytest.fixture(scope="module")
def driver():
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	with webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options) as driver:
		yield driver

def test_task_journey(driver,app_with_temp_board):
	driver.get('http://127.0.0.1:5000')

	assert driver.title == 'To-Do App'

	driver.find_element_by_id('card_name').send_keys('Test Item Name')
	driver.find_element_by_id('card_desc').send_keys('Test Item Description')
	driver.find_element_by_id('card_due').send_keys((datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y"))
	driver.find_element_by_id('add_to_dropdown').click()
	driver.find_element_by_id('add_to_To Do').click()

	assert driver.find_element_by_xpath("//*[starts-with(@id,'to_do_item_')]")

	driver.find_element_by_xpath("//*[starts-with(@id,'dropdownMenuButton')]").click()
	driver.find_element_by_xpath("//a[contains(text(),'Move to: Doing')]").click()

	assert driver.find_element_by_xpath("//*[starts-with(@id,'doing_item_')]")

	driver.find_element_by_xpath("//*[starts-with(@id,'dropdownMenuButton')]").click()
	driver.find_element_by_xpath("//a[contains(text(),'Move to: Done')]").click()

	assert driver.find_element_by_xpath("//*[starts-with(@id,'done_item_')]")

	driver.find_element_by_xpath("//*[starts-with(@id,'dropdownMenuButton')]").click()
	driver.find_element_by_xpath("//a[contains(text(),'Remove')]").click()
	
	with pytest.raises(NoSuchElementException):
		driver.find_element_by_xpath("//*[starts-with(@id,'to_do_item_')]")

	with pytest.raises(NoSuchElementException):
		driver.find_element_by_xpath("//*[starts-with(@id,'doing_item_')]")

	with pytest.raises(NoSuchElementException):
		driver.find_element_by_xpath("//*[starts-with(@id,'done_item_')]")
