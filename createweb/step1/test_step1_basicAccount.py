import unittest
import smsdk.qafw.create.create_utils as common
from smsdk.qafw.create import create_start
from smsdk.qafw.create.create_start_template import SurveyFromTemplate
from smsdk.qafw.create.create_start_existing import EditExistingSurvey
from smsdk.qafw.create.create_main import CreateMain
from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.create.create_utils import get_driver_only, close_driver
from smsdk.qafw.create.survey import Survey
import datetime
import os
import pytest

CAT_name = 'Events'
TEMPLATE_name = "Professional Event Feedback Template"
CREATE_MAIN_CHECK_ID = "step2"
CREATE_STEP_1_ID = "step1"
STEP_2_CHECK_ID = "step2"

class TestBasicAccount(unittest.TestCase):

    def setUp(self):
        """Create a report for each test."""
        env_init('basic')
        testcasename = os.path.basename(__file__).split(
            '.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")
        self.user = common.get_env_data()
        self.driver = get_driver_only(testcasename)
        self.step_1_url = self.user['domain'] + "/create/"
        self.driver.get(self.step_1_url)
        self.mySurvey = Survey(self.driver, self.user, ' ')
        report_path = self.__class__.__name__
        self.report = reporting_wrapper("Create",  # report_feature_name
                                        report_path,  # report_relative_location
                                        self.__class__.__name__,
                                        # report_file_name_prefix
                                        "Testing the First Step in Create",
                                        # test_suite_title
                                        ("Testing for the presence of some upgrade prompts "
                                         "for basic users."),  # test_suite_description
                                        "utf-8",  # file_encoding
                                        # logging_dict
                                        {SplunkDataAttributes.TYPE:
                                         SplunkTestCaseTypes.BVT},
                                        self.driver)  # selenium_driver
        env_init('basic')

    def tearDown(self):
        """Save the report and return to the step 1 URL."""

        if common.is_correct_url(self.driver, self.step_1_url + '?sm='):
            assert common.delete_survey(
                self.user["user_id"],
                survey_id=None,
                driver=self.driver)
        close_driver(self.driver, self.report, self.user)
        self.report.save_report()

    @pytest.mark.BVT
    @pytest.mark.TC_BVT
    def test_upgrade_to_edit(self):
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Upgrade To Edit Prompt",
            "Basic users can copy templates with >10 questions. However, they should not be "
            "able to edit any of the questions, and should instead see an upgrade prompt.")

        start_template_result = create_start.click_step_1_radio_button(
            self.driver,
            3)
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Click Start from an Expert Template",
            "Clicks the 3 radio selection on the /create/ page.",
            start_template_result,
            False,
            not start_template_result,
            self.driver)

        template = SurveyFromTemplate(self.driver)
        category_names = template.get_category_names()
        category_name = template.get_specific_category_name(
            category_names, CAT_name
        )
        category_result = template.choose_category(category_name)
        tempate_result = template.choose_template(TEMPLATE_name, category_name)
        select_template_result = category_result and tempate_result
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Use Professional Event Feedback Template",
            "Clicks on the Events Category and then on the specified template.",
            select_template_result,
            False,
            not select_template_result,
            self.driver)

        common.wait_Notify_Window_Gone(self.driver)
        common.id_wait(self.driver, STEP_2_CHECK_ID)


        create_main = CreateMain(self.driver)
        create_displayed = create_main.verify_create_main_displayed()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify Create Page is Displayed",
            "Create a new survey from the Professional Event Feedback Template, then checks "
            "that the page is displayed by checking for the preview, print, & send buttons, "
            "and the 'last saved' bar.",
            create_displayed,
            False,
            not create_displayed,
            self.driver)
        # this call is a redundant part as there is no popup dialog at this
        # stage
        # walkme_displayed = self.mySurvey.myAccordion.close_walke_me_dialog()
        # self.report.add_report_record(
        #     ReportMessageTypes.TEST_STEP,
        #     "Verify walk me dialog is Displayed",
        #     "Check the walk me dialog showed up correctly and closed ok",
        #     walkme_displayed,
        #     False,
        #     not walkme_displayed,
        #     self.driver)
        page = create_main.get_survey_page('1')
        page_found = page is not None
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Desired Page Exists",
            "We try to get the web "
            "element for page 1 of the survey (div with id containing 'pageid').",
            page_found,
            False,
            page_found,
            self.driver)

        question = create_main.get_question('3')
        question_found = question is not None
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Desired Question Exists",
            "Try to get the Third "
            "question in the survey by finding the element with 'data-qnumber' of 3.",
            question_found,
            False,
            not question_found,
            self.driver)
        actions = create_main.get_q_actions(question)
        actions_found = actions is not None
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Question Actions panel Exists",
            "Hover over the "
            "question we got earlier, and confirm the actions panel appears.",
            actions_found,
            False,
            not actions_found,
            self.driver)
        upgrade_to_edit = create_main.get_action_by_name(
            actions, "UpgradeToEdit").is_displayed()
        upgrade_to_edit_found = upgrade_to_edit is not None
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "'Upgrade To Edit' prompt appears",
            "The user should see an upgrade prompt if they try to edit a survey with >10 Q's",
            upgrade_to_edit_found,
            False,
            not upgrade_to_edit_found,
            self.driver)
        assert start_template_result
        assert select_template_result
        assert create_displayed
        assert page_found
        assert question_found
        assert actions_found
        assert upgrade_to_edit_found
        # assert walkme_displayed

    def test_cannot_copy_template(self):
        template_name = TEMPLATE_name
        self.report.add_report_record(
            ReportMessageTypes.TEST_CASE,
            "Cannot Copy >10q Survey",
            "Basic users can make surveys from templates with >10 questions, but should not "
            "be able to copy them.")

        survey = SurveyFromTemplate(self.driver)
        category_names = survey.get_category_names()
        category_name = survey.get_specific_category_name(
            category_names, CAT_name
        )
        survey.choose_category(category_name)
        survey.choose_template(template_name, category_name)
        # do a wait here
        common.id_wait(self.driver, CREATE_MAIN_CHECK_ID)
        self.driver.get(self.step_1_url)
        # do a wait here
        common.id_wait(self.driver, CREATE_STEP_1_ID)
        create_start.click_step_1_radio_button(self.driver, 2)
        survey = EditExistingSurvey(self.driver)
        survey_found = survey.choose_survey(template_name)
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Survey was found successfully",
            "If you want to copy a specific survey, then that survey had better exist.",
            survey_found)

        upgrade_prompt_appears = survey.verify_upgrade_prompt()
        self.report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Upgrade Prompt Appears",
            "Clicking the 'Upgrade' button should bring up an upgrade prompt.",
            upgrade_prompt_appears)

        assert survey_found
        assert upgrade_prompt_appears
