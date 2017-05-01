from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeAutosavingQtnFromAddAnotherQtnBtn/",  # report_relative_location
                               "test_starQType_autosavingQtnFromAddAnotherQtnBtn",
                               # report_file_name_prefix
                               ("Verify autosaving star rating question from clicking on 'add next question' button " +
                                "on edit mode"),  # test_suite_title
                               ("This test verifies star rating question should autosave and multiple choice question "
                                "should be in open edit mode"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812365
def test_starQType_autosavingQtnFromAddAnotherQtnBtn(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify autosaving star rating question from clicking on "
                                                           "'add next question' button on edit mode")
    try:
        mySurvey.myBuilder.click_star_rating_add_button()
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-emoji-rating")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add star rating question type to survey",
                                 "Verified that star rating question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star rating question to survey."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verifyReqiredFieldErrorMessage()
        "check question shouldn't add at this point due to star rating question required fields are missing"
        report.add_report_record(ReportMessageTypes.TEST_STEP, ("Verify star rating question is not Saved due to "
                                                                "required field missing"),
                                 "Verified that star rating question is not saved due to required field missing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question not saved due to required field missing."
        # code to enter the title into star rating question title text box
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # code to verify that star rating question type automatically saved
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star rating question auto save",
                                 "Verified that star rating question type automatically saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question type automatically saved."
        ex = mySurvey.myQuestion.verify_question_in_edit_mode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice Question Open In Edit Mode",
                                 "Verified that multiple choice question opened in edit mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple choice question opened in edit mode."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
