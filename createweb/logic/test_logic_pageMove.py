from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageMove/",  # report_relative_location
                               "test_logic_pageMove",  # report_file_name_prefix
                               "Test copying a page followed by moving a page",  # test_suite_title
                               ("This test copies page 1 to page 2 "
                                " and then attempts to move page 1 to after page 2."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_pageMove(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test copying a page followed by moving a page.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.copy_existing_page(1, 1)
        mySurvey.myCreate.single_page_goto(1)
        mySurvey.myBuilder.unfold_BuilderRegion()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myLogic.pushQuestionToStack(title)
        mySurvey.myQuestion.create_question_with_svysvc(mySurvey.survey_id,
                                                        mySurvey.myDesign.getPageID(1),
                                                        [{u'type': {u'subtype': u'vertical',
                                                                    u'name': None,
                                                                    u'family': u'single_choice'},
                                                          u'answers': {u'rows': [{u'text': mySurvey.myLogic.RNG(10),
                                                                                  u'visible': True,
                                                                                  u'position': 1,
                                                                                  u'type': u'row'}]},
                                                            u'visible': True,
                                                            u'has_piping': False,
                                                            u'position': 1,
                                                            u'question_bank': {u'logical_bank_id': None,
                                                                               u'is_banked': False,
                                                                               u'partner_id': None,
                                                                               u'name': None,
                                                                               u'lang_bank_id': None},
                                                            u'heading': title}])
        driver.refresh()
        mySurvey.myLogic.movePage(1, 2)
        ex = True if mySurvey.myCreate.num_questions_in_page(2) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Page Mode",
                                 "checks to make sure that we scroll at the top and are not on page 1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify single page mode."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
