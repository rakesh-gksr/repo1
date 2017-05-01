from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
from smsdk.qafw.rpage import responses, endpage
from smsdk.qafw.create.svysvc_api_wrapper import get_question_responses
import traceback
import pytest

__author__ = 'rajat'

#testrail('C83914')
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicCustomOption/",  # report_relative_location
                               "test_logic_CustomOption_Redirect to Webpage",  # report_file_name_prefix
                               "Verify custom option and redirect to your own page option ",  # test_suite_title
                               ("This test verifies custom option and redirect to your own page option "
                                "To verify custom option and redirect to your own page option "),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.quota
@pytest.mark.C83914
@pytest.mark.Infobeans
@pytest.mark.IB
@pytest.mark.MT1
def test_logic_simpleQuota_verifyCustomOption_closingWindow(create_survey):
    driver, mySurvey, report = create_survey
    answer_rows = ["Regularly","Sometimes", "Occasionally"]

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify custom option and redirect to your own page option window.")
    try:
        survey_id = mySurvey.survey_id
        user_id = mySurvey.user_id
        survey_json = mySurvey.mySvc_holder.svysvc.get_survey(survey_id, user_id)
        survey_title = survey_json["title"]["text"]
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How often you travel?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How often you travel?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1], "1")
        mySurvey.myLogic.click_QuotaOptions()
        mySurvey.myLogic.click_selectingOption_redirectToWebpage("http://www.google.com")
        mySurvey.myLogic.click_QuotaDone()
        ex = mySurvey.myLogic.verifyQuotaStatus("On")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify quota status is on",
                                 "Verify quota status is on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quota status"

        # parameters for creating collector via API
        params = {
            'survey_id': int(mySurvey.survey_id),
            'name': "New collector's name",
            'type': "weblink",
        }
        # create collector via api
        collector = mySurvey.mySvc_holder.collectsvc.create(int(mySurvey.user_id), params)
        collector_url = collector["weblink"]["url"]
        collector_id = collector["metadata"]["collector_id"]

        # turn on multiple response for collector
        update_options = {
            "allow_multiple_responses": True
        }
        update_result = mySurvey.mySvc_holder.collectsvc.update(int(collector_id), int(mySurvey.user_id), update_options)
        check_update_result = True if update_result["survey_id"] == int(survey_id) else False
        report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify collector option is updated or not",
            "Verify collector option is updated or not",
            check_update_result,
            False,
            not check_update_result,
            driver)
        assert check_update_result, "Failed to update collector option"

        for attempt in range(0, 2):

            opened, total_load_time = Spage.open_survey(
                driver, collector_url, survey_title)
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Open survey url " + collector_url,
                                     "Driver goes to the survey and it took " + str(total_load_time) +
                                     " to open page.",
                                     opened, False, not opened, driver)
            assert opened, "cannot open survey"

            if attempt == 0:
                answers = {
                    1: {
                        1: {"choices_list": [1]}
                    }
                }

                expected_answers_dict, expected_response_dict = get_question_responses(
                    collector_url, answers, collector_id)

                previous_count = responses.get_responses_count(survey_id)

                take = Spage.take_survey(driver, expected_answers_dict[1])
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Attempting question",
                                         "Attempting question",
                                         take, False, not take, driver)
                assert take, "cannot take survey"

                submit_result = Spage.submit_survey(driver)
                report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Click Done",
                    "Driver clicks done button",
                    submit_result,
                    False,
                    not submit_result,
                    driver)
                assert submit_result, "Submit survey failed"

                check_thank_you = "survey-thanks" in driver.current_url
                assert check_thank_you, "Failed to load thank you page"

                response_result = responses.poll_response_generated(
                    3,
                    10,
                    5,
                    5,
                    survey_id,
                    mySurvey.user_id,
                    previous_count,
                    expected_response_dict)

                report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "Verify Response",
                    "Verifies survey response is sent and correctly received by AnSvc.",
                    response_result,
                    False,
                    not response_result,
                    driver)
                assert response_result, "Survey response verification failed."

            elif attempt == 1:

                check_closed = "survey-closed" in driver.current_url
                assert check_closed, "Failed to check survey closure"

                expected_text = "This survey is currently closed. " \
                                "Please contact the author of this survey for further assistance."
                ex = endpage.is_closed_collector_displayed(driver, expected_text)
                report.add_report_record(
                    ReportMessageTypes.TEST_STEP,
                    "verify survey closed page",
                    "verify survey closed page",
                    ex,
                    False,
                    not ex,
                    driver)
                assert ex, "Survey response verification failed."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

