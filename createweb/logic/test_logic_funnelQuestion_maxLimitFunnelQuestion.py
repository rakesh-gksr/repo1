from smsdk.qafw.create import create_utils
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.survey_util.create_survey import Survey as CreateSurvey
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes

import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionMaxLimitFunnelQuestion",  # report_relative_location
                               "test_logic_funnelQuestion_maxLimitFunnelQuestion",  # report_file_name_prefix
                               "funneling edge case automation for max limit, important for every svysvc release",
                               # test_suite_title
                               "Test to verify funneling edge case automation for max limit, important for "
                               "every svysvc release",  # test_suite_description
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


@pytest.mark.IB
@pytest.mark.C1076587
@pytest.mark.SVYSVC_1234
def test_logic_funnel_question_max_limit_funnel_question(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "funneling edge case automation for max limit, important"
                                                           " for every svysvc release.")
    try:

        page_one_index = 0
        page_two_index = 1
        user_id = mySurvey.user_id
        survey_id = mySurvey.survey_id
        survey = CreateSurvey()
        svysvc = mySurvey.mySvc_holder.svysvc
        answer_rows = []
        for i in range(1, 191):
            answer_rows.append('row ' + str(i))
        # Code to add multi choice question type
        question_q1 = survey.add_multichoice_question_raw(
            svysvc, user_id, survey_id, page_one_index,
            'Test Q1 multi choice question', answer_rows, 1)

        answer_rows = []
        for i in range(1, 491):
            answer_rows.append('row ' + str(i))

        # Code to add dropdown question type
        question_q2 = survey.add_dropdown_question(
            svysvc, user_id, survey_id, page_one_index,
            'Test Q2 dropdown question', 2, answer_rows)

        survey.create_new_page(svysvc, user_id, str(survey_id), 2, "This is second Page")

        answer_rows = ['row one', 'row two']
        answer_cols = ['col one', 'col two']

        # Code to add multiple choice question type
        question_q3 = survey.add_multichoice_question_raw(
            svysvc, user_id, survey_id, page_two_index,
            'Test Q3 multi choice question', answer_rows, 1)

        # Code to add dropdown question type
        question_q4 = survey.add_dropdown_question(
            svysvc, user_id, survey_id, page_two_index,
            'Test Q4 dropdown question', 2, answer_rows)

        # Code to add matrix rating scale question type
        question_q5 = survey.add_matrix_scale_question(
            svysvc, user_id, survey_id, page_two_index,
            'Test Q5 matrix rating scale question', 3, answer_rows, answer_cols)

        # Code to add multi textbox question type
        question_q6 = survey.add_multi_textbox_question(
            svysvc, user_id, survey_id, page_two_index,
            'Test Q6 multi textbox question', 4, answer_rows)

        # Code to add ranking question type
        question_q7 = survey.add_ranking_question(
            svysvc, user_id, survey_id, page_two_index,
            'Test Q7 Ranking question', 5)

        result = create_utils.funnels_question(survey_id, question_q1[0]['question_id'], question_q3[0]['question_id'])
        ex = (len(result['receiver_options_map']) == 190)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows from Q1 to Q3",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows from Q1 to Q3."

        result = create_utils.funnels_question(survey_id, question_q2[0]['question_id'], question_q4[0]['question_id'])
        ex = (len(result['receiver_options_map']) == 490)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows from Q2 to Q4",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows from Q2 to Q4."

        result = create_utils.funnels_question(survey_id, question_q1[0]['question_id'], question_q5[0]['question_id'])
        ex = (len(result['receiver_options_map']) == 190)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows from Q1 to Q5",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows from Q1 to Q5."

        result = create_utils.funnels_question(survey_id, question_q1[0]['question_id'], question_q6[0]['question_id'])
        ex = (len(result['receiver_options_map']) == 190)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows from Q1 to Q6",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows from Q1 to Q6."

        result = create_utils.funnels_question(survey_id, question_q1[0]['question_id'], question_q7[0]['question_id'])
        ex = (len(result['receiver_options_map']) == 190)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows from Q1 to Q7",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows from Q1 to Q7."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
