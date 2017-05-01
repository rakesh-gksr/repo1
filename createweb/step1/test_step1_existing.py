"""
Author: beng
Date: July 1, 2014

This is a test suite which checks the functionality of the "Edit An Existing Survey"
tab in create step 1.

Essentially, the tests are all exactly the same for this one. It's more about having many
different types of surveys, with different contents, than it is about having many different
test cases.

My automation account has a survey named "Some Questions" which should have an image,
a matrix, a multiple choice, and a single text field, with a progress bar and page
numbers, spread across two separate pages. We'll copy it and make sure everything gets
transferred over properly.
"""

from smsdk.qafw.create.create_start_existing import EditExistingSurvey
from smsdk.qafw.create.create_main import CreateMain
import smsdk.qafw.create.create_utils as common
from smsdk.qafw.create import create_start
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.create.create_utils import get_driver_only, close_driver
from selenium.common.exceptions import NoSuchElementException
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import unittest
import datetime
import os
import pytest


@pytest.mark.MT1
class TestStep1Existing(unittest.TestCase):

    survey_name = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y") + '--' + "00000000"

    def setUp(self):
        env_init()
        env = common.get_env_data()
        svc_holder = common.get_svc_holder()
        rs = svc_holder.svysvc.copy_survey(('100617006'), ('57496951'), (env['user_id']), self.survey_name)
        testcasename = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y") + '--' + os.path.basename(__file__).split(
            '.')[0]
        self.user = common.get_env_data()
        self.survey_id = rs['survey_id']
        self.driver = get_driver_only(testcasename)
        self.step_1_url = self.user['domain'] + "/create/"
        self.driver.get(self.step_1_url)
        self.survey = EditExistingSurvey(self.driver)
        self.create_main = None
        report_path = self.__class__.__name__
        self.report = reporting_wrapper("Create",  # report_feature_name
                                        report_path,  # report_relative_location
                                        self.__class__.__name__,
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
                                        self.driver)  # selenium_driver
        create_start.click_step_1_radio_button(self.driver, 2)

    def tearDown(self):
        if common.is_correct_url(self.driver, self.step_1_url + '?sm='):
            assert common.delete_survey(
                self.user["user_id"],
                survey_id=None,
                driver=self.driver)
        close_driver(self.driver, self.report, self.user)
        self.report.save_report()

    def test_basic(self):
        """
        Copy over a survey with all sorts of logic options enabled, and check that it all gets copied over properly.

        There are a lot of test steps here, and I'm probably going to add more soon.
        """
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Copy Survey With Logo & Logic options",
            "Tests that a survey (Test Survey Basic) with multiple features "
            "is copied over properly.")

        self.create_main = CreateMain(self.driver)
        ex = self.create_main.choose_first_existing_survey(self.survey_name)
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Title",
            "Survey has the expected title is: Copy of Test Survey Basic",
            ex,
            False,
            not ex,
            self.driver)

        title_correct = self.create_main.get_survey_title(
        ) == "Copy of " + self.survey_name
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Title",
            "Survey has the expected title is: Copy of Test Survey Basic",
            title_correct,
            False,
            not title_correct,
            self.driver)

        logo = self.create_main.verify_logo_displayed()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Logo",
            "The survey's logo appears, as expected",
            logo,
            False,
            not logo,
            self.driver)

        page_skip = self.create_main.verify_logic_is_on("page_skip")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Page Skip Logic",
            "Page skip logic is on by checking option is highlighted in builder.",
            page_skip,
            False,
            not page_skip,
            self.driver)

        page_rand = self.create_main.verify_logic_is_on("page_rand")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Page Randomization Logic",
            "Page randomization logic is on by checking option is highlighted in builder.",
            page_rand,
            False,
            not page_rand,
            self.driver)

        q_rand = self.create_main.verify_logic_is_on("question_rand")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Question Randomization Logic",
            "Survey has question randomization turned on by checking option is highlighted in builder.",
            q_rand,
            False,
            not q_rand,
            self.driver)

        quotas = self.create_main.verify_logic_is_on("quotas")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Quotas",
            "Survey has quotas turned on by checking option is highlighted in builder.",
            quotas,
            False,
            not quotas,
            self.driver)

        custom_vars = self.create_main.verify_logic_is_on("custom_vars")
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Custom Variables",
            "Survey has custom variables turned on by checking option is highlighted in builder.",
            custom_vars,
            False,
            not custom_vars,
            self.driver)

        assert title_correct
        assert logo
        assert page_skip
        assert page_rand
        assert q_rand
        assert quotas
        assert custom_vars

    @pytest.mark.skipif(True, reason="Skip this test case because new desing of copy from existing survey page "
                              "does not have 'go' button")
    def test_copy_no_selection(self):
        """Try to hit 'let's go' without actually selecting a survey."""
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "No Survey Selected",
            "Should not allow a user to copy a survey if none has been selected.")
        new_survey_result = self.survey.click_lets_go_existing()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Lets Go button",
            "Clicks let's go button under section Edit a Copy of an Existing Survey",
            new_survey_result,
            False,
            not new_survey_result,
            self.driver)

        correct_url = common.is_correct_url(self.driver, self.step_1_url)
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Don't Get Redirected",
            "We should still be at the same URL.",
            correct_url,
            False,
            not correct_url,
            self.driver)

        error_label = self.survey.is_copy_label_error()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Error Label Appears",
            "A little error message should show up in the DOM.",
            error_label,
            False,
            not error_label,
            self.driver)

        assert correct_url
        assert error_label

    @pytest.mark.skipif(True, reason="Skip this test case because new desing does not have input box to rename the survey")
    def test_copy_no_title(self):
        """Try to hit 'let's go' without actually giving the copied survey a name."""
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "No Name Given",
            "Shouldn't allow a user to copy a survey if no name for the copy has been given.")
        try:
            self.survey.choose_survey(self.survey_name)
        except NoSuchElementException:
            assert False

        self.survey.enter_survey_title("")
        new_survey_result = self.survey.click_lets_go_existing()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Lets Go button",
            "Clicks let's go button under section Edit a Copy of an Existing Survey",
            new_survey_result,
            False,
            not new_survey_result,
            self.driver)

        correct_url = common.is_correct_url(self.driver, self.step_1_url)
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Don't Get Redirected",
            "We should still be at the same URL.",
            correct_url)

        error_label = self.survey.is_title_label_error()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Error Label Appears",
            "A little error message should show up in the DOM.",
            error_label)

        assert correct_url
        assert error_label
