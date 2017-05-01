from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeCoypQuestion/",  # report_relative_location
                               "test_starQType_copyQuestion",  # report_file_name_prefix
                               "Copy star on another page ",  # test_suite_title
                               "This test copy the star question on another page",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812388
def test_starQType_copyQuestion(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(ReportMessageTypes.TEST_CASE, "This test copy the star question on another page.")
    try:
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add star question type to survey ",
                                 "Verified that star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star question to survey."

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star question Add to Live Preview",
                                 "Verifies that star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question added to live preview."

        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")
        driver.refresh()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_copy_tab()
        mySurvey.myLogic.copyQuestion(2, 1, 'After')

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star Question Copied",
                                 "verifies that star question is copied after question 2 on page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question is copied after question 2 on page 2"
        # Code to edit star question on page no 3
        mySurvey.myQuestion.click_on_question_to_edit(3)
        # Code to verify that star rating question
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-emoji-rating")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star rating question type",
                                 "verifies that second question type on page 2 is star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify second question type on page 2 is star rating question."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
