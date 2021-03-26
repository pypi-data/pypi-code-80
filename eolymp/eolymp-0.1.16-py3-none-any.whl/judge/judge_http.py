# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class JudgeClient:
    def __init__(self, transport):
        self.transport = transport

    def CreateContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CreateContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CreateContestOutput"),
            **kwargs,
        )

    def DeleteContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DeleteContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DeleteContestOutput"),
            **kwargs,
        )

    def UpdateContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/UpdateContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.UpdateContestOutput"),
            **kwargs,
        )

    def LookupContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/LookupContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.LookupContestOutput"),
            **kwargs,
        )

    def DescribeContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeContestOutput"),
            **kwargs,
        )

    def ListContests(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListContests",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListContestsOutput"),
            **kwargs,
        )

    def OpenContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/OpenContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.OpenContestOutput"),
            **kwargs,
        )

    def CloseContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CloseContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CloseContestOutput"),
            **kwargs,
        )

    def ConfigureRegistrationForm(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ConfigureRegistrationForm",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ConfigureRegistrationFormOutput"),
            **kwargs,
        )

    def DescribeRegistrationForm(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeRegistrationForm",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeRegistrationFormOutput"),
            **kwargs,
        )

    def ConfigureRuntime(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ConfigureRuntime",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ConfigureRuntimeOutput"),
            **kwargs,
        )

    def DescribeRuntime(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeRuntime",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeRuntimeOutput"),
            **kwargs,
        )

    def SubmitRegistration(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/SubmitRegistration",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.SubmitRegistrationOutput"),
            **kwargs,
        )

    def DescribeRegistration(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeRegistration",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeRegistrationOutput"),
            **kwargs,
        )

    def ImportProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ImportProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ImportProblemOutput"),
            **kwargs,
        )

    def SyncProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/SyncProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.SyncProblemOutput"),
            **kwargs,
        )

    def UpdateProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/UpdateProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.UpdateProblemOutput"),
            **kwargs,
        )

    def ListProblems(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListProblems",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListProblemsOutput"),
            **kwargs,
        )

    def DescribeProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeProblemOutput"),
            **kwargs,
        )

    def ListStatements(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListStatements",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListStatementsOutput"),
            **kwargs,
        )

    def ListExamples(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListExamples",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListExamplesOutput"),
            **kwargs,
        )

    def DeleteProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DeleteProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DeleteProblemOutput"),
            **kwargs,
        )

    def RetestProblem(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/RetestProblem",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.RetestProblemOutput"),
            **kwargs,
        )

    def AddParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/AddParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.AddParticipantOutput"),
            **kwargs,
        )

    def EnableParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/EnableParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.EnableParticipantOutput"),
            **kwargs,
        )

    def DisableParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DisableParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DisableParticipantOutput"),
            **kwargs,
        )

    def VerifyPasscode(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/VerifyPasscode",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.VerifyPasscodeOutput"),
            **kwargs,
        )

    def EnterPasscode(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/EnterPasscode",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.EnterPasscodeOutput"),
            **kwargs,
        )

    def ResetPasscode(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ResetPasscode",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ResetPasscodeOutput"),
            **kwargs,
        )

    def RemovePasscode(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/RemovePasscode",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.RemovePasscodeOutput"),
            **kwargs,
        )

    def RemoveParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/RemoveParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.RemoveParticipantOutput"),
            **kwargs,
        )

    def ListParticipants(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListParticipants",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListParticipantsOutput"),
            **kwargs,
        )

    def DescribeParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeParticipantOutput"),
            **kwargs,
        )

    def IntrospectParticipant(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/IntrospectParticipant",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.IntrospectParticipantOutput"),
            **kwargs,
        )

    def JoinContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/JoinContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.JoinContestOutput"),
            **kwargs,
        )

    def StartContest(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/StartContest",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.StartContestOutput"),
            **kwargs,
        )

    def CreateSubmission(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CreateSubmission",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CreateSubmissionOutput"),
            **kwargs,
        )

    def ListSubmissions(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListSubmissions",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListSubmissionsOutput"),
            **kwargs,
        )

    def DescribeSubmission(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeSubmission",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeSubmissionOutput"),
            **kwargs,
        )

    def RetestSubmission(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/RetestSubmission",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.RetestSubmissionOutput"),
            **kwargs,
        )

    def CreateTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CreateTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CreateTicketOutput"),
            **kwargs,
        )

    def CloseTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CloseTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CloseTicketOutput"),
            **kwargs,
        )

    def OpenTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/OpenTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.OpenTicketOutput"),
            **kwargs,
        )

    def ReadTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ReadTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ReadTicketOutput"),
            **kwargs,
        )

    def DeleteTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DeleteTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DeleteTicketOutput"),
            **kwargs,
        )

    def DescribeTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeTicketOutput"),
            **kwargs,
        )

    def ListTickets(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListTickets",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListTicketsOutput"),
            **kwargs,
        )

    def ReplyTicket(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ReplyTicket",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ReplyTicketOutput"),
            **kwargs,
        )

    def ListReplies(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListReplies",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListRepliesOutput"),
            **kwargs,
        )

    def DeleteReply(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DeleteReply",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DeleteReplyOutput"),
            **kwargs,
        )

    def UpdateReply(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/UpdateReply",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.UpdateReplyOutput"),
            **kwargs,
        )

    def CreateAnnouncement(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/CreateAnnouncement",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.CreateAnnouncementOutput"),
            **kwargs,
        )

    def UpdateAnnouncement(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/UpdateAnnouncement",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.UpdateAnnouncementOutput"),
            **kwargs,
        )

    def DeleteAnnouncement(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DeleteAnnouncement",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DeleteAnnouncementOutput"),
            **kwargs,
        )

    def ReadAnnouncement(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ReadAnnouncement",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ReadAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncement(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeAnnouncement",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncementStatus(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeAnnouncementStatus",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementStatusOutput"),
            **kwargs,
        )

    def ListAnnouncements(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/ListAnnouncements",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.ListAnnouncementsOutput"),
            **kwargs,
        )

    def DescribeCodeTemplate(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.judge.Judge/DescribeCodeTemplate",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.judge.DescribeCodeTemplateOutput"),
            **kwargs,
        )

