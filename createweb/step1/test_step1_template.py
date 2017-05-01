"""
Author: beng
Date: July 1, 2014

This is a test suite which checks the functionality of the "Create Survey From Template"
tab in create step 1.
"""
# create
from smsdk.qafw.create.create_start_template import SurveyFromTemplate
from smsdk.qafw.create.create_main import CreateMain
import smsdk.qafw.create.create_utils as common
from smsdk.qafw.create import create_start
# reporting
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_utils import get_driver_only, close_driver
# other python
import unittest
import datetime
import os


class TestStep1Template(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the context for the test to run.

        This includes creating a driver, logging in, and directing it to the create URL,
        and creating some miscellaneous variables.
        """
        env_init()
        testcasename = os.path.basename(__file__).split(
            '.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")
        cls.user = common.get_env_data()
        cls.driver = get_driver_only(testcasename)
        cls.create_main_check_id = "step2"
        cls.step_1_url = cls.user['domain'] + "/create/"
        report_path = cls.__class__.__name__
        cls.report = reporting_wrapper("Create",  # report_feature_name
                                       report_path,  # report_relative_location
                                       cls.__class__.__name__,
                                       # report_file_name_prefix
                                       "Testing the First Step in Create",
                                       # test_suite_title
                                       ("Testing features on the  step 1 create page "
                                        "related to editing an existing survey "
                                        "work as intended."),  # test_suite_description
                                       "utf-8",  # file_encoding
                                       # logging_dict
                                       {SplunkDataAttributes.TYPE:
                                        SplunkTestCaseTypes.REGRESSION},
                                       cls.driver)  # selenium_driver

    @classmethod
    def tearDownClass(cls):
        #cls.driver.quit()
        close_driver(cls.driver, cls.report, cls.user)
        cls.report.save_report()

    def setUp(self):
        """Create a report and navigate to the correct section of the page for each test."""
        print "Starting test: " + self._testMethodName

        self.driver.get(self.step_1_url)
        create_start.click_step_1_radio_button(self.driver, 3)

    def tearDown(self):
        """Save the report and return to the create URL."""
        if common.is_correct_url(self.driver, self.step_1_url + '?sm='):
            assert common.delete_survey(
                self.user["user_id"],
                survey_id=None,
                driver=self.driver)

    def test_net_promoter_score(self):
        """
        Test the NPS survey template.

        This does double duty, not just testing the functionality of starting from a template in a general sense,
        but also testing the appearance of the NPS question specifically.
        """
        survey_title = "Net Promoter Score Template"
        nps_string = "How likely is it that you would recommend this company to a friend or colleague?"
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Test Create Survey from Template"
            "Tests creating a survey from " +
            survey_title)
        survey = SurveyFromTemplate(self.driver)
        category_names = survey.get_category_names()
        survey.choose_category(category_names[1])
        survey.choose_template(survey_title, category_names[1])
        # do a wait here
        common.id_wait(self.driver, self.create_main_check_id)
        create_main = CreateMain(self.driver)

        correct_survey_title = create_main.get_survey_title() == survey_title
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Title Is Correct",
            "Title should reflect the template we used",
            correct_survey_title,
            False,
            not correct_survey_title,
            self.driver)

        question_title = create_main.get_question_with_title(nps_string)
        correct_question_title = question_title is not None and question_title.text.strip(
        ) == nps_string
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Question Text Is Correct",
            "Looks for any question with the expected question text.",
            correct_question_title)

        assert correct_survey_title
        assert correct_question_title
