import win32com.client as win32

def extract_outlook_data_to_excel(mailbox_name):
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    recipient = outlook.CreateRecipient(mailbox_name)
    recipient.Resolve()

    if recipient.Resolved:
        inbox = outlook.GetSharedDefaultFolder(recipient, 6) 
        # 6 corresponds to the Inbox folder; check here for the other folder types:
        # https://learn.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders

        xlApp = win32.Dispatch("Excel.Application")
        xlWB = xlApp.Workbooks.Add()
        xlWS = xlWB.Worksheets(1)

        xlWS.Cells(1, 1).Value = "Subject"
        xlWS.Cells(1, 2).Value = "Sender"
        xlWS.Cells(1, 3).Value = "ReceivedTime"
        xlWS.Cells(1, 4).Value = "SentOn"
        xlWS.Cells(1, 5).Value = "Categories"
        xlWS.Cells(1, 6).Value = "ConversationTopic"
        xlWS.Cells(1, 7).Value = "To"
        xlWS.Cells(1, 8).Value = "CC"
        xlWS.Cells(1, 9).Value = "BCC"
        xlWS.Cells(1, 10).Value = "EntryID"
        xlWS.Cells(1, 11).Value = "Body"
        xlWS.Cells(1, 12).Value = "ConversationIndex"
        xlWS.Cells(1, 13).Value = "ReceivedByEntryID"
        xlWS.Cells(1, 14).Value = "Parent"

        row = 2
        for item in inbox.Items:
            if item.Class == 43: # 43 corresponds to MailItem class
                xlWS.Cells(row, 1).Value = item.Subject
                xlWS.Cells(row, 2).Value = item.SenderName
                xlWS.Cells(row, 3).Value = item.ReceivedTime
                xlWS.Cells(row, 4).Value = item.SentOn
                xlWS.Cells(row, 5).Value = item.Categories
                xlWS.Cells(row, 6).Value = item.ConversationTopic
                xlWS.Cells(row, 7).Value = item.To
                xlWS.Cells(row, 8).Value = item.CC
                xlWS.Cells(row, 9).Value = item.BCC
                xlWS.Cells(row, 10).Value = item.EntryID
                xlWS.Cells(row, 11).Value = item.Body
                xlWS.Cells(row, 12).Value = item.ConversationIndex
                xlWS.Cells(row, 13).Value = item.ReceivedByEntryID
                xlWS.Cells(row, 14).Value = item.Parent
                row += 1

        xlWS.Columns.AutoFit()
        xlApp.Visible = True

    else:
        print("Mailbox name not resolved.")

if __name__ == "__main__":
    mailbox_name = "MailboxName" # Replace with the desired mailbox name
    extract_outlook_data_to_excel(mailbox_name)
