# -*- coding: utf-8 -*-
from apiclient import discovery, errors
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from oauth2client import tools
import mimetypes
import oauth2client
import json
import httplib2
import os
import base64
import argparse


class GmailCommunication:
    STANDARD_SUBJECT = "Reporte de tests"

    def __init__(self, flags):
        #self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        self.flags = flags
        self.scopes = 'https://mail.google.com/'
        self.client_secret_file = 'client_secret.json'
        self.application_name = 'Auxiliar CC1002'
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)
        self.studentsMails = self.getStudentsMAils()
        self.sender = self.getSender()
        self.query = self.buildQuery()

    def getSender(self):
        with open('config.json') as data_file:
            data = json.load(data_file)
            return data["myMail"]

    def getStudentsMAils(self):
        """ getStudentsMAils: none -> Dict
            Retorna un diccionario con los mails (llaves) y nombres (valores) de los estudiantes,
            almacenados en el archivo config.json
        """
        d = {}
        with open('config.json') as data_file:
            data = json.load(data_file)
            for email in data["emails"]:
                d[email['mail']] = email['alumno']
        return d

    def buildQuery(self):
        """ buildQuery : none -> string
            retorna un string con la query que se ejecutará para buscar correos en gmail
            con los mails de todos los alumnos y que hayan sido enviados dentro del último día
        """

        s = "("
        for email in self.studentsMails.keys():
            s += "from:" + email + " OR "
        s = s[:-4] + ")"
        s += " AND newer_than:1d"
        return s


    def getCredentials(self):
        """ getCredentials : none -> Credentials
            obtiene las credenciales para acceder a la cuenta de gmail
            si las credenciales están almacenadas, procede con esas credenciales
            en caso contrario abre gmail en un navegador para loggearse
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_name
            credentials = oauth2client.tools.run_flow(flow, store, self.flags)
            print 'Storing credentials to ' + credential_path
        return credentials

    def getMessages(self):
        """ getMessages: none -> list[Messages]
        retorna la lista de mensajes que coinciden con self.query
        """

        try:
            response = self.service.users().messages().list(userId = "me",
                                                       q = self.query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId="me", q=self.query,
                                                 pageToken=page_token).execute()
                messages.extend(response['messages'])

            # for m in messages:
            #     self.getMessage(m['id'])
            return messages
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def getStudentByMail(self, mail):
        """ getStudentByMail: string -> string
            Dado un mail, retorna el nombre de usuario asociado a ese mail. None en caso de no existir
        """
        if mail in self.studentsMails:
            return self.studentsMails[mail]
        return None


    def getMessage(self,id):
        """ getMessage: string -> Message
        Retorna el mensaje que coincide con la id entregada
        """

        try:
            message = self.service.users().messages().get(userId="me", id=id).execute()
            return message

        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def getHeaderFrom(self, message):
        """ getHeaderFrom: Message -> String
            Retorna el mail del que fue enviado el mensaje
        """
        for header in message['payload']['headers']:
            if header['name'] == "From":
                partsOfTheHeader = header['value'].split(" ")
                for s in partsOfTheHeader:
                    if s[0] == "<" and s[-1] == ">": return s[1:-1]

                return False # no se encontró el mail

        return False # idem

    def getAttachments(self, message, storeDir, msgStudentName):
        """ getAttachments: Message -> string
            Obtiene y descarga el primer archivo adjunto asociado a un mensaje. Retorna la ruta del archivo
            descargado (con la extensión .py)
        """
        msgId = message['id']

        if msgStudentName == "":
            msgFrom = self.getHeaderFrom(message)
            msgStudentName = self.studentsMails[msgFrom]

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    attId = part['body']['attachmentId']
                    att = self.service.users().messages().attachments().get(userId="me", messageId=msgId,id=attId).execute()
                    data = att['data']

                fileData = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = os.path.join(storeDir, msgStudentName + ".py")

                with open(path, 'w') as f:
                    f.write(fileData)

                return path
        return "" # no se encontró ningún archivo adjunto

    def createMessageWithAttachment(self, to, fileDir, fileName):
        """Create a message for an email.

            Args:
                sender: Email address of the sender.
                to: Email address of the receiver.
                subject: The subject of the email message.
                message_text: The text of the email message.
                file_dir: The directory containing the file to be attached.
                filename: The name of the file to be attached.

            Returns:
                An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = self.sender
        message['subject'] = GmailCommunication.STANDARD_SUBJECT

        # msg = MIMEText(messageText)
        # message.attach(msg)

        filePath = os.path.join(fileDir, fileName)

        content_type, encoding = mimetypes.guess_type(filePath)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filePath, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filePath, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filePath, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filePath, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=fileName)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def sendMessage(self, message):
        """Send an email message.

            Args:
                service: Authorized Gmail API service instance.
                user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
                message: Message to be sent.

            Returns:
                Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId="me", body=message)
                    .execute())
            print 'Message Id: %s' % message['id']
            return message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def createAndSendMessage(self, to, fileDir, fileName):
        message = self.createMessageWithAttachment(to, fileDir, fileName)
        sentMessage = self.sendMessage(message)
        return sentMessage

if __name__ == '__main__':
    g = GmailCommunication()
