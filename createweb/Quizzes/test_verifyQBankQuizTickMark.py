from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQBankQuizTickMark/",  # report_relative_location
                               "test_verifyQBankQuizTickMark",  # report_file_name_prefix
                               # test_suite_title
                               "Verify that the scoring can also be enabled for the QB questions",
                               "Test to verify that the scoring can also be enabled for the QB questions",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809405
def test_verify_qbank_quiz_tick_mark(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify that the scoring can also be enabled for the QB questions")
    try:
        # add question to survey via api

        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myBank.add_questionBankQuestion_via_qbsvc(
            "What is your child's gender?", mySurvey.survey_id, page_num, 1)
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myBank.editQBQAnswers()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Mark",
                                 "Verifies that all the answer choices showing are tick mark",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices showing are tick marks."

        for i in range(1, 3):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
            ex = mySurvey.myQuestion.increase_quiz_points(i, 6)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Up Arrow for Increasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on up arrow increased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on up arrow increased the points for answer choice - " + str(i)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
