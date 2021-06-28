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

@pytest.fixture(scope='module')
def app_with_temp_board():
	file_path = find_dotenv('.env')
	load_dotenv(file_path, override=True)

	board_id = create_board("e2e Test Board")['id']
	os.environ['BOARD_ID'] = board_id
	
	application = app.create_app()
	
	thread = Thread(target=lambda: application.run(use_reloader=False))
	thread.daemon = True
	thread.start()
	yield app
	
	thread.join(1)
	delete_board(board_id)

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
