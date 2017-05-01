#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: beng
Date: July 1, 2014

This is a test suite which checks the functionality of the "Create Survey From Scratch"
tab in create step 1.

Most of these test methods have names which fairly accurately describe their function. Therefore,
I have left out docstrings for all the test_* methods unless they don't have a very descriptive name.
"""
# create
from smsdk.qafw.create.create_main import CreateMain
import smsdk.qafw.create.create_utils as common
from smsdk.qafw.create.create_start_new import NewSurvey
# reporting
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init, wait_Accordion_Ready
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_utils import get_driver_only, close_driver
# other python
import unittest
import datetime
import os
import traceback
import pytest
import HTMLParser


class TestStep1New(unittest.TestCase):

    short_title = "Short test survey title"
    odd_title = r"!@#$%^&*()_+{}|:\"<>?~,./;'[]\=-"
    too_long_title = "L0rem 1psum d0l0r s1t 4m3t, c0ns3c737ur 4dipiscing 3l17. Vivamus ut eros eu cursus posuere! \
Lorem ipsum dolor sit amet, consectetur adipiscing AtBCtD. 1234567 4ccumsan nibh nonz f3rmentum tincidunt. Donec \
ut lacus sit amet felis aliquam orci aliquam."
    exp_long_title = "L0rem 1psum d0l0r s1t 4m3t, c0ns3c737ur 4dipiscing 3l17. Vivamus ut eros eu cursus posuere! \
Lorem ipsum dolor sit amet, consectetur adipiscing AtBCtD. 1234567 4ccumsan nibh nonz f3rmentum tincidunt. Donec \
ut lacus sit amet felis aliquam orci aliquam."

    def setUp(self):
        """Create a report for each test."""
        env_init('classic_question_bank')
        testcasename = os.path.basename(__file__).split(
            '.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")
        self.user = common.get_env_data()
        self.driver = get_driver_only(testcasename)
        self.step_1_url = self.user['domain'] + "/create/"
        self.driver.get(self.step_1_url)
        # reporting
        report_file_path = self.__class__.__name__
        self.report = reporting_wrapper("Create",  # report_feature_name
                                        report_file_path,  # report_relative_location
                                        "test_step1_new",  # report_file_name_prefix
                                        "Testing the First Step in Create",
                                        # test_suite_title
                                        ("Testing features on the  step 1 create page "
                                         "related to creating a new survey "
                                         "work as intended."),  # test_suite_description
                                        "utf-8",  # file_encoding
                                        # logging_dict
                                        {SplunkDataAttributes.TYPE:
                                         SplunkTestCaseTypes.BVT},
                                        self.driver)  # selenium_driver

    def tearDown(self):
        """Save the report and return to the step 1 URL."""
        if common.is_correct_url(self.driver, self.step_1_url + '?sm='):
            assert common.delete_survey(
                self.user["user_id"],
                survey_id=None,
                driver=self.driver)
        close_driver(self.driver, self.report, self.user)
        self.report.save_report()

    def wrapper(self, title_str, exp_title_str, category=False):
        try:
            survey = NewSurvey(self.driver)
            survey.create_survey_from_scratch()
            # STEP 1:
            enter_survey_result = survey.enter_survey_title(title_str)
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Enter survey title text for New Survey",
                "Enters text on Create Step1: " +
                str(title_str),
                enter_survey_result,
                False,
                not enter_survey_result,
                self.driver)
            # STEP 1.5:
            if category:
                # selects category from menu drop down
                category_names = survey.get_category_names()
                # This is arbitrary - could be any category
                selected_category = category_names[4]
                category_result = survey.select_category(selected_category)
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Selects Cagetory",
                    "Selects a category from the drop down menu",
                    enter_survey_result,
                    False,
                    not enter_survey_result,
                    self.driver)
            else:
                category_result = True

            # STEP 2:
            new_survey_result = survey.click_lets_go_new()
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Click Lets Go button",
                "",
                new_survey_result,
                False,
                not new_survey_result,
                self.driver)

            create_main = CreateMain(self.driver)
            wait_Accordion_Ready(self.driver)
            # STEP 3
            create_main_url = self.user["domain"] + '/create/?sm='
            correct_url = common.is_correct_url(self.driver, create_main_url)
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Redirects correctly to main create page",
                "Checks url to see we get redirected to create step 2.",
                correct_url,
                False,
                not correct_url,
                self.driver)
            if correct_url:
                # STEP 4
                correct_page = create_main.verify_create_main_displayed()
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Page looks correct",
                    "Checks a few DOM elements to make sure the page looks correct.",
                    correct_page,
                    False,
                    not correct_page,
                    self.driver)
                # STEP 5
                current_title_str = HTMLParser.HTMLParser().unescape(create_main.get_survey_title())
                correct_title = current_title_str == exp_title_str
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Correct title",
                    "Verifies that the survey title is the one we gave it earlier.",
                    correct_title,
                    False,
                    not correct_title,
                    self.driver)
                if category:
                    correct_primed_qb_category = True
                    # todo: commented the following as it's blocked by QBL-147
                    # primed_qb_category = create_main.get_primed_qb_category()
                    # correct_primed_qb_category = primed_qb_category in selected_category
                    # self.report.add_report_record(
                    #     ReportMessageTypes.TEST_STEP,
                    #     "Correct Question Bank Category is Highlighted",
                    #     "The highlighted category in the question bank should match the category we "
                    #     "chose.",
                    #     correct_primed_qb_category)
                else:
                    correct_primed_qb_category = True
                return correct_url and category_result and correct_page and correct_title and correct_primed_qb_category

            else:
                return False

        except:
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Exception occured during test",
                traceback.format_exc(),
                False,
                False,
                True,
                self.driver)
            return False

    @pytest.mark.BVT
    @pytest.mark.TC_BVT
    def test_happy_path(self):
        """Test the expected user path through the page."""
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Normal Path",
            "Tests the way the average user would be expected to use the page")
        assert self.wrapper(self.short_title, self.short_title)

    #@pytest.mark.skip(reason="skip QBL testing for now")
    @pytest.mark.QBL
    def test_survey_with_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Normal Path with Category Selection",
            "Tests creating a survey with a category selected.")
        assert self.wrapper(self.short_title, self.short_title, category=True)


    @pytest.mark.QBL
    def test_long_name_with_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Too Long Name + Category",
            "Survey name should be limited to 250 characters, even when a "
            "category is selected")
        assert self.wrapper(
            self.too_long_title,
            self.exp_long_title,
            category=True)


    @pytest.mark.QBL
    def test_odd_name_no_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Odd Name",
            "Tests making a survey from scratch with an unusual name and no category")
        assert self.wrapper(self.odd_title, self.odd_title)


    @pytest.mark.QBL
    def test_odd_name_with_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Odd Name + Category",
            "Tests Step 1 - New with an unusual name and an arbitrary category")
        assert self.wrapper(self.odd_title, self.odd_title, category=True)

    # We are expecting the title NOT to be the same in the created survey as
    # in the code

    @pytest.mark.QBL
    def test_long_name_no_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Too Long Name",
            "Survey name should be limited to 250 characters")
        assert self.wrapper(self.too_long_title, self.exp_long_title)

    def wrapper_all_cat(
            self,
            title_str,
            exp_title_str,
            category=True,
            cat_num=0):
        try:
            survey = NewSurvey(self.driver)
            survey.create_survey_from_scratch()
            # STEP 1:
            enter_survey_result = survey.enter_survey_title(title_str)
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Enter survey title text for New Survey",
                "Enters text on Create Step1: " +
                str(title_str),
                enter_survey_result,
                False,
                not enter_survey_result,
                self.driver)
            # STEP 1.5:
            if category:
                # selects category from menu drop down
                category_names = survey.get_category_names()
                # This is arbitrary - could be any category
                selected_category = category_names[cat_num]
                category_result = survey.select_category(selected_category)
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Selects Cagetory of : ------ %s" %
                    selected_category,
                    "Selects a category from the drop down menu",
                    enter_survey_result,
                    False,
                    not enter_survey_result,
                    self.driver)
            else:
                category_result = True

            # STEP 2:
            new_survey_result = survey.click_lets_go_new()
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Click Lets Go button",
                "",
                new_survey_result,
                False,
                not new_survey_result,
                self.driver)

            create_main = CreateMain(self.driver)
            wait_Accordion_Ready(self.driver)
            # STEP 3
            create_main_url = self.user["domain"] + '/create/?sm='
            correct_url = common.is_correct_url(self.driver, create_main_url)
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Redirects correctly to main create page",
                "Checks url to see we get redirected to create step 2.",
                correct_url,
                False,
                not correct_url,
                self.driver)
            if correct_url:
                # STEP 4
                correct_page = create_main.verify_create_main_displayed()
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Page looks correct",
                    "Checks a few DOM elements to make sure the page looks correct.",
                    correct_page,
                    False,
                    not correct_page,
                    self.driver)
                # STEP 5
                correct_title = create_main.get_survey_title() == exp_title_str
                self.report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Correct title",
                    "Verifies that the survey title is the one we gave it earlier.",
                    correct_title,
                    False,
                    not correct_title,
                    self.driver)
                if category and selected_category.strip() != 'Other':
                    correct_primed_qb_category = True
                    # todo: commented the following as it's blocked by QBL-147
                    # primed_qb_category = create_main.get_primed_qb_category()
                    # correct_primed_qb_category = primed_qb_category in selected_category
                    # self.report.add_report_record(
                    #     ReportMessageTypes.TEST_STEP,
                    #     "Correct Question Bank Category is Highlighted",
                    #     "The highlighted category in the question bank should match the category we "
                    #     "chose.",
                    #     correct_primed_qb_category)
                else:
                    correct_primed_qb_category = True

                return correct_url and category_result and correct_page and correct_title and correct_primed_qb_category

            else:
                return False

        except:
            self.report.add_report_record(
                ReportMessageTypes.TEST_STEP,
                "Exception occured during test",
                traceback.format_exc(),
                False,
                False,
                True,
                self.driver)
            return False


    @pytest.mark.QBL
    def test_with_all_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Go through all Category",
            "Survey can be created with all categories ")
        survey = NewSurvey(self.driver)
        survey.create_survey_from_scratch()
        category_names = survey.get_category_names()
        for cat_num in xrange(len(category_names)):
            self.driver.get(self.step_1_url)
            assert self.wrapper_all_cat(
                self.too_long_title,
                self.exp_long_title,
                category=True,
                cat_num=cat_num)

    def test_no_title(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "No Title",
            "Trying to make a survey with no name should show an error label.")
        survey = NewSurvey(self.driver)
        survey.create_survey_from_scratch()
        new_survey_result = survey.click_lets_go_new()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Lets Go button",
            "",
            new_survey_result,
            False,
            not new_survey_result,
            self.driver)
        test_status = survey.is_label_error()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Error Label",
            "An error label should show up in the DOM.",
            test_status,
            False,
            not test_status,
            self.driver)

        assert new_survey_result and test_status

    def test_no_title_with_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "No Title + Category",
            "Trying to make a survey with no name & a category should fail")
        survey = NewSurvey(self.driver)
        survey.create_survey_from_scratch()
        categories = survey.get_category_names()
        # choose an arbitrary category name from the list
        category_result = survey.select_category(categories[1])
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Select category from drop down menu",
            "",
            category_result,
            False,
            not category_result,
            self.driver)

        new_survey_result = survey.click_lets_go_new()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Lets Go button",
            "",
            new_survey_result,
            False,
            not new_survey_result,
            self.driver)

        test_status = survey.is_label_error()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Error Label",
            "An error label should show up on the create step 1 page.",
            test_status,
            False,
            not test_status,
            self.driver)

        assert new_survey_result and test_status

    @pytest.mark.IB
    @pytest.mark.BVT
    @pytest.mark.quiz
    @pytest.mark.C12809425
    def test_verify_quiz_category(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Verify create a survey with quiz category at Create Step 1",
            "Verifies that Quiz category display in category dropdown")
        survey = NewSurvey(self.driver)
        survey.create_survey_from_scratch()
        enter_survey_result = survey.enter_survey_title("test survey title")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Enter survey title text for New Survey",
            "Enters text on Create Step1: test survey title",
            enter_survey_result,
            False,
            not enter_survey_result,
            self.driver)
        assert enter_survey_result, "Failed to enter survey title"
        survey.get_category_names()
        category_result = survey.select_category("Quiz")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Select Quiz category from drop down menu",
            "",
            category_result,
            False,
            not category_result,
            self.driver)
        assert category_result, "Failed to select quiz category"

        new_survey_result = survey.click_lets_go_new()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Lets Go button",
            "",
            new_survey_result,
            False,
            not new_survey_result,
            self.driver)
        assert new_survey_result, "Failed to create survey"
