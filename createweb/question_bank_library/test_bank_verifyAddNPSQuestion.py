from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyAddNPSQuestion/",  # report_relative_location
                               "test_bank_verifyAddNPSQuestion",  # report_file_name_prefix
                               "Verify add NPS question",  # test_suite_title
                               ("Test to verify add NPS question"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C281075
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifyAddNPSQuestion(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify add NPS question")

    open_category = "AllCategories"
    search_question = "How likely is it that you would recommend <this company> to a friend or colleague?"

    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                 "it opens with " + open_category + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + " Category closing the modal failed"

        ex = mySurvey.myQBank.typePartialQuestion(search_question)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text entry",
                                 "check to make sure that entered question to get an autocomplete list",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Verify Text Entry verification failure"
        mySurvey.myQBank.addModalSearchQuestionToPreview(1, 1)
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                 "Verify Added Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add question in preview box"
        ex = mySurvey.myQBank.check_modal_question_card_box_color()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question card in the modal turns gray ",
                                 "check to make sure that question card in the modal turns gray",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question card in the modal turns gray"
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question adds in preview ",
                                 "check to make sure that question added in preview",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added in preview"
        ex = mySurvey.myQBank.check_preview_question_box_color()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question adds in preview with light grey color",
                                 "check to make sure that question added in preview with light grey color",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added in preview with light grey color"
        ex = mySurvey.myQBank.check_modal_question_icon_visible()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question has check icon",
                                 "check to make sure that question having check icon",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question has check icon"
        ex = mySurvey.myQBank.clickAddQuestionOnPreview()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify click on add question",
                                 "check to make sure that clicked on add question btn",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify main survey questions"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify NPS question gets added",
                                 "check to make sure that NPS question gets added",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add NPS question"
        mySurvey.myQuestion.hover_on_question(1)
        ex = mySurvey.myQBank.verifyBechmarkCertifiedQuestion()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Benchmark certified question",
                                 "Adds a Benchmark certified question and verifies that the certification icon appears",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Benchmark certified question verification failure"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
