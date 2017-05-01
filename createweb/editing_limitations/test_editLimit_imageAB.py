from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitImageAB/",  # report_relative_location
                               "test_editLimit_imageAB",  # report_file_name_prefix
                               "verify editing limitations on image AB test question type",  # test_suite_title
                               ("Adds an image type question. Survey answers are collected"
                                " and verifies that limited editability is enabled, and nickname can be changed."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_editLimit_imageAB(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify editing limitations on image AB test question type.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_ImageABTestAddButton()
        mySurvey.myQuestion.enter_imageAB_label(1, "poi?")
        mySurvey.myQuestion.enter_imageAB_url(
            1,
            "https://secure.surveymonkey.com/smassets/smlib.globaltemplates/1.4.7/assets/logo/surveymonkey_logo.svg")
        mySurvey.myQuestion.enter_imageAB_label(2, "tacos!")
        mySurvey.myQuestion.enter_imageAB_url(
            2,
            "https://resources.monkeytest1.com/smassets/createweb/smlib.globaltemplates/1.4.4/assets/logo/surveymonkey_logo_dark.svg")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.process_surveyCollection(mySurvey.myCreate.get_survey_title(), [{2: {'choices_list': ['Kongou']}}])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability ."
        ex = mySurvey.myQuestion.enter_nickname_label("test nickname")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify nickname added after collection",
                                 "checks that question can still have nickname added after collection",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify nickname addition."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
