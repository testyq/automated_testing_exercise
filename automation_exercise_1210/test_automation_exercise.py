# coding=utf-8

import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as page_check



class TestExerciseScenarios(object):

    def setup(self):
        self.driver = Chrome()
        self.driver.get("https://image.baidu.com/")
        self.driver.implicitly_wait("15")
        
    def teardown(self):
        self.driver.close()

    def test_webpage_layout(self):
        """
        Page layout test:
        1. Open "https://image.baidu.com/".
        2. Go through the web page to check the static content and button,
        3. Click the '按图片搜索' button to open the upload window
        4. Upload image successfully.
        """
        # Check content "背景图片来源" displayed on the  lower left side of the form
        page_check.text_to_be_present_in_element("wrapperImgFromBox", "背景图片来源")
        # Check ‘百度首页’ button on the upper right side of the form
        page_check.element_to_be_clickable("new-userinfo-baiduIndex")
        # Check icon besides the login user on the upper right side of the form
        page_check.visibility_of_element_located("s-top-img-wrapper")
        # Check there is '按图片搜索' icon in the text box
        page_check.visibility_of_element_located("st_camera_off")
        # Click the '按图片搜索' button to open the upload file window
        self.driver.find_element_by_class_name("st_camera_on").click()
        # Check there is "拖拽图片到这里" content under the text box
        page_check.visibility_of_element_located("dttip")
        # Check there is "选择文件" button on the right of the form
        page_check.element_to_be_clickable("uploadImg")

    def test_form_input(self):
        """
        Form input test:
        1. Try inputting invalid image url .
        2. Try to upload invalid format file.
        """
        cwd = os.getcwd()
        file_path = cwd + '/test_automation_exercise.py'
        # Check inputting invalid image url
        content = self.driver.find_element_by_id("stuurl")
        content.send_keys("test invalid url")
        self.driver.find_element_by_id("sbobj").click()
        error_message = self.driver.find_element_by_class_name("stutips").text
        assert error_message == "请输入正确的网址格式"
        # Upload *.py format file will get error
        self.driver.find_element_by_class_name("st_camera_on").click()
        upload_image = self.driver.find_element_by_id("stfile")
        upload_image.send_keys(file_path)
        upload_image.submit()
        self.switch_window()
        # Check page is redirected to the result page
        error_message = self.driver.find_element_by_class_name("graph-noresult-text1").text
        assert error_message == "功能优化中，敬请期待"

    def test_upload_image(self):
        """
        Upload file test:
        1. Upload an image and check the image is uploaded successfully
        """
        cwd = os.getcwd()
        image_path = cwd + '/image.jpg'
        # Upload image will redirect to the new page
        self.driver.find_element_by_class_name("st_camera_on").click()
        time.sleep(5)
        upload_image = self.driver.find_element_by_id("stfile")
        upload_image.send_keys(image_path)
        upload_image.submit()
        self.switch_window()
        # Check page is redirected to the result page
        info = self.driver.find_element_by_class_name("general-title").text
        assert info == '相似图片'

    def test_link_redirect(self):
        """
        Link redirect test:
        1. Click '更多' on page and check the new page is opened
        """
        self.driver.get("https://image.baidu.com/")
        self.driver.find_element_by_name("i_briicon").click()
        self.switch_window()
        url = self.driver.current_url()
        assert url == "https://www.baidu.com/more/"

    def test_security(self):
        """
        Security test:
        1. XSS
        2. SQL injection
        """
        # XSS
        content = self.driver.find_element_by_id("stuurl")
        content.send_keys('<input type="text" id="stuurl_tmp" placeholder="请输入或粘贴图片地址" '
                          'value autocomplete="off" class="stuurl" name="objurl">')
        self.driver.find_element_by_id("sbobj").click()
        xss_error_message = self.driver.find_element_by_class_name("stutips")
        assert xss_error_message == "请输入正确的网址格式"
        # SQL injection
        content = self.driver.find_element_by_id("stuurl")
        content.send_keys("select * from table name")
        self.driver.find_element_by_id("sbobj").click()
        sql_error_message = self.driver.find_element_by_class_name("stutips")
        assert sql_error_message == "请输入正确的网址格式"

    def switch_window(self):
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles

        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
        print("ok")


if __name__ == "__main__":
    TestExerciseScenarios.test_webpage_layout()
    TestExerciseScenarios.test_form_input()
    TestExerciseScenarios.test_upload_image()
    TestExerciseScenarios.test_link_redirect()
    TestExerciseScenarios.test_security()
