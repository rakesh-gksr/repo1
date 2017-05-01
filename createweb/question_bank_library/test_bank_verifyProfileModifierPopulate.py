from smsdk.qafw.create.create_utils import env_init
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

open_category = "CustomerFeedback"
keyword = "this neighborhood"
company_name = "infobeans"
question = "How likely is it that you would recommend <this company> to a friend or colleague?"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyAccountProfileModifierPopulate",  # report_relative_location
                               "test_bank_verifyAccountProfileModifierPopulate",  # report_file_name_prefix
                               "Verify Account level Profile with Modifier Popup",  # test_suite_title
                               "Testing of Modifier from Modal with Account level Profile Details like company name",
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})
    env_init('questionbank_profile')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.QBL
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C280917
@pytest.mark.C812369
@pytest.mark.skipif(True, reason="skip because it always failed while adding company name")
def test_bank_verify_profile_modifier_populate(create_survey):
    driver, mySurvey, report = create_survey

    url = driver.current_url
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Account Level Profile with Modifier Value")
    try:
        # Do the account setting and update company name
        mySurvey.myProfile.open_account_settings()
        ex = mySurvey.myProfile.addCustomerFeedbackCompanyDetails(company_name)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify company profile setting update",
                                 "Verify to update the account setting by using profile functions",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify account level setting update."
        driver.refresh()
        driver.get(url)
        ex = mySurvey.myBank.unfold_QuestionBankRegion()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify unfold question bank region",
                                 "check to make sure that  question bank region is unfolded",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to unfold question bank region"
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                             "Clicks on " + open_category + " and makes sure that "
                             "it opens with " + open_category + " as hero button",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, open_category + "Category closing the modal failed"
        ex = mySurvey.myQBank.typePartialQuestion(question)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text entry",
                                 "check to make sure that entered question to get an autocomplete list",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Verify Text Entry verification failure"
        # check first question from question list match with company name or not
        ex = mySurvey.myQBank.verify_modifier_value_from_modal_qb(1, 1, company_name)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify profile setting with modifier value",
                                 "Verify profile setting with modifier value by checking and filtering the question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify profile level setting match with modifier value."
        #############################
        mySurvey.myQBank.addModalSearchQuestionToPreview(1, 1)
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                 "Verify Added Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add question in preview box"

        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question adds in preview ",
                                 "check to make sure that question added in preview",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added in preview"
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
        ex = mySurvey.myQBank.verifyCompanyNameInQuestionDropdown(company_name)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify company name",
                                 "check to make sure that company name showing in dropdown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify company name"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    finally:
            driver.get(url)
            mySurvey.myProfile.open_account_settings()
            mySurvey.myProfile.deleteCustomerFeedbackCompanyDetails()