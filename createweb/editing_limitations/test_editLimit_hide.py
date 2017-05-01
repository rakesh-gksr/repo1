from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitHide/",  # report_relative_location
                               "test_editLimit_hide",  # report_file_name_prefix
                               "verify hiding/unhiding all answer options leaving minimum required choice for each question type",  # test_suite_title
                               ("Adds affected question types and options, collects answers"
                                " and verifies that limited editability is enabled."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_editLimit_hide(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify hiding/unhiding all answer options leaving minimum required choice for each question type.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("How silly is this Survey?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "poi?")
        mySurvey.myQuestion.enter_matrix_answerText(1, "1")
        mySurvey.myQuestion.enter_matrix_answerText(2, "2")
        mySurvey.myQuestion.enter_matrix_answerText(3, "3")
        mySurvey.myQuestion.enter_matrix_answerText(4, "4")
        mySurvey.myQuestion.enter_matrix_answerText(5, "5")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_RankingAddButton()
        mySurvey.myQuestion.enter_question_title("Rank you favorite DD")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Yuudachi")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Shigure")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MultipleTextboxesAddButton()
        mySurvey.myQuestion.enter_question_title("Please explain the meaning of life.")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Wall of Text goes here")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_DateTimeAddButton()
        mySurvey.myQuestion.enter_question_title("When is my birthday?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "07/15/1988")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        mySurvey.myQuestion.enter_question_title("The silliness in this survey has reached critical levels!")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "poipoipoi?!")
        mySurvey.myQuestion.enter_matrix_answerText(1, "much poi")
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, "such poi")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.process_surveyCollection(mySurvey.myCreate.get_survey_title(),
                                                  [{1: {'choices_list': ['Kongou']},
                                                    2:{'choices_list': ['Miku']},
                                                      3:{'choices_list': ['poi? 5']},
                                                      4:{'ranking_list': ['Yuudachi', 'Shigure']},
                                                      5:{'input_text': '42'},
                                                      6: {'time_input_text': ['08', '16', 'PM'],
                                                          'date_input_text': ['07', '15', '1988']},
                                                      7:{'answer_choices_tuple': [('poipoipoi?', 'such poi')]}
                                                    }])
        for x in xrange(1, 7):
            mySurvey.myQuestion.click_on_question_to_edit(x)
            ex = mySurvey.myQuestion.verify_responsesCollected()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                     "checks for limited editability notice multiple choice",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify limited editability multiple choice."
            ex = mySurvey.myQuestion.disabled_delete_multipleChoice_answerRow(1)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled delete answer row",
                                     "checks for answer row deletion to be disabled",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify disabled answer row delete."
            ex = mySurvey.myQuestion.disabled_answerRow_hide(1)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled hide answer row",
                                     "checks for answer row hiding button to be disabled",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify disabled answer row hide."
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled hide answer column",
                                     "checks for answer column hiding button to be disabled",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify disabled answer row column."
            ex = mySurvey.myLogic.disabled_toggleQuestionFunneling()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled question funneling",
                                     "checks for disabled question funneling",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify disabled question funneling."
            if x == 1 or x == 2 or x == 3 or x == 7:
                mySurvey.myQuestion.turn_on_multichoice_otheroption()
            mySurvey.myQuestion.click_question_save_from_edit_tab()
            if x == 1 or x == 2 or x == 3 or x == 7:
                ex = mySurvey.myQuestion.verify_otherAnswer_textBox(x)
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify other answer option",
                                         "checks that we can still turn on other answer option",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to verify other option."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
