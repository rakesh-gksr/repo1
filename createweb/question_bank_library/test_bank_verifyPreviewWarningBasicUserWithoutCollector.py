from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyPreviewWarningBasicUserWithoutCollector/",  # report_relative_location
                               "test_bank_verifyPreviewWarningBasicUserWithoutCollector",  # report_file_name_prefix
                               "Verify TBYB:Basic User without a Collector tries to "
                               "add more than 10 questions via the modal",  # test_suite_title
                               ("Test to verify TBYB: Basic User without a Collector tries to "
                                "add more than 10 questions via the modal"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    env_init("basic_with_tbyb")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280960
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifyPreviewWarningBasicUserWithoutCollector(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "TBYB : Basic User without a Collector tries to "
                                                           "add more than 10 questions via the modal")

    open_category = "AllCategories"

    try:
        # add question to survey via api
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")
        driver.refresh()

        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open " + open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                                                "it opens with " + open_category + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + " Category closing the modal failed"

        initial_question_count = mySurvey.myQBank.totalCategoryQuestions()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify default question box",
                                 "Verify default question box loaded or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert initial_question_count > 0, "Failed to load question box"

        ul_item = 1
        li_item = 1
        for i in xrange(9):
            ex = mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(ul_item, li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Modal Question From List",
                                     "Verify question added on click of card or question box.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add question"
            # check question added into preview box or not
            ex = mySurvey.myQBank.check_modal_question_added_in_preview_box(i+2)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                     "Verify Added Question is added into preview box or not.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add  question in preview box"

            #  check card / li box color after question add. It should be grey after question add
            ex = mySurvey.myQBank.check_preview_question_box_color(i+2)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Modal Box Color",
                                     "Verify Modal Box Color of added question.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to change question card color to grey"

        # add 11th question to preview window
        mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(ul_item, li_item)
        # verify message while adding 11th question to preview
        ex = mySurvey.myQBank.verifyUpgradeInPreviewQuestionBox("Enabled")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify yellow upgrade treatment appears over the "
                                                               "Preview section with upgrade button",
                                 "check to make sure that yellow upgrade treatment appears over the Preview section",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify yellow upgrade treatment appears over the Preview section"
        ex = mySurvey.myQBank.closeUpgradeButton()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Able to dismiss the Hard Stop",
                                 "check to make sure that upgrade window close",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to close upgrade window"
        ex = mySurvey.myQBank.verifyTotalQuestionAddedInPreview(11)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify able to add more than 10 questions",
                                 "check to make sure that added more than 10 questions in preview",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add more than 10 questions added in preview"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
