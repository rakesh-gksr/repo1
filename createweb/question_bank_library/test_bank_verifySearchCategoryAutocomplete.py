from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create import create_utils
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyAutoCompleteSearchCategory",  # report_relative_location
                               "test_bank_verifySearchCategoryAutocomplete",  # report_file_name_prefix
                               "Verify Search Category Autocomplete Functionality",  # test_suite_title
                               "Testing of search category Autocomplete functionality by entering search value",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

search_keyword = "What"


@pytest.mark.MT1
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verify_search_category_autocomplete(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Search Category Autocomplete Functionality")
    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        # time.sleep(1)
        ex = mySurvey.myQBank.type_autocomplete_search_input_question(search_keyword)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Autocomplete Text Box",
                                 "Check able to enter the autocomplete text in text box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add autocomplete text in text box"

        ex = mySurvey.myQBank.get_search_autocomplete_question_list()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify All Subparts Of Autocomplete Box",
                                 "Check all sections like Question, Templates & Tags are present or not in Box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to load all sections in Autocomplete Box"
        ex = create_utils.get_basic_autocomplete_result()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify search keyword is present in autocomplete result",
                                 "check the getmatch returns meaningful data",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify search keyword is present in autocomplete result"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
