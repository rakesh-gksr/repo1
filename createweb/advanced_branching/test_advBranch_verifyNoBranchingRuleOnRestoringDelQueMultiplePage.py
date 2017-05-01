#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It verifies that the advance branching logic is removed on restoring the deleted question on multiple pages.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchVerifyNoBranchRuleOnRestoringDelQueOnMultiplePage/",
                               # report_relative_location
                               "test_advBranch_verifyNoBranchingRuleOnRestoringDelQueMultiplePage",
                               # report_file_name_prefix
                               "To check that Branching rule does not exists after restoring a deleted Matrix type"
                               " question on Multiple page survey",  # test_suite_title
                               ("verify deleting source question and restoring it back shouldn't restore branching "
                                "rule with multiple page survey"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C249902
def test_advBranch_verifyNoBranchingRuleOnRestoringDelQueMultiplePage(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify deleting source question and restoring it back"
                                                           "shouldn't restore branching rule with multiple page survey")

    try:
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")

        for x in xrange(2):
            driver.refresh()
            page_num = mySurvey.myDesign.getPageID(x+1)
            mySurvey.myDesign.click_addPageTitle("Page "+ str(x+1), "This is test page "+ str(x+1), (x+1))
            mySurvey.myQuestion.generate_unweighted_matrix_question(mySurvey.survey_id, page_num,
                                                                    "Please classify the following Ships",
                                                                    ["Haruna", "Yuudachi", "Naka"],
                                                                    ["Destroyer(DD)", "Light Cruiser(CL)",
                                                                     "Battleship(BB)", "Aircraft Carrier(CV)",
                                                                     "Submarine(SS)"], (x+1))
            mySurvey.myLogic.unfold_LogicRegion()
            mySurvey.myLogic.click_PageSkipLogicButton()
            mySurvey.myLogic.select_PageSkipSelectPage("P"+str(x+1) + ":" + " Page " + str(x+1))
            mySurvey.myLogic.click_PageSkipSelectNextButton()
            ex = mySurvey.myLogic.addNewBranchingRule([
                ("matrix", [(x + 1), (x + 1), 1], "equals", ["Destroyer(DD)"], "finish", "default", None)])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                     "Verifies advanced logic window closed and logic saved.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to save advanced logic"
            ex = mySurvey.myQuestion.hover_on_question_to_delete_it(x+1)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Q"+str(x+1)+" Question",
                                     "Verifies Q"+str(x+1)+" deleted successfully.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to delete Q"+str(x+1)+" question"
            # Restore the deleted question
            mySurvey.myCreate.restoreDeletedQuestion(1)
            # Verify advance branching does not apply
            ex = mySurvey.myLogic.verify_num_advanced_branching(0)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching deleted",
                                     "verifies that Page Skip Logic is off and that the Advanced Branching "
                                     "rule is deleted.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify Page Skip Logic Off/Advanced Branching deleted"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
