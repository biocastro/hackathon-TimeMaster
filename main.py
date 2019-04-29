# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 09:46:26 2019

@author: cacec
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import dfgui
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import  MIMEText
from email.mime.multipart import MIMEMultipart


# variables para la hoja de calculo de Gdrive
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('hackaton-c6d5224e7723.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Hacks2019').sheet1

class CustomPopup(Popup):
    pass

class CustomPopup2(Popup):
    pass

class MainWindow(Screen):
    pass

class MedicoWindow(Screen):
    def cleartext(self):
         self.passw1.text = ''
    def open_popup(self):
        the_popup = CustomPopup2()
        the_popup.open()

class ClinicaWindow(Screen):
    def cleartext(self):
         self.passw2.text = ''
    def open_popup(self):
        the_popup = CustomPopup2()
        the_popup.open()

class DesarrolladorWindow(Screen):
    def cleartext(self):
         self.passw3.text = ''
    def open_popup(self):
        the_popup = CustomPopup2()
        the_popup.open()

class PacientesWindow(Screen):
    def graph(self):
        df = pd.DataFrame(sheet.get_all_records())
        dfgui.show(df)

class PacientesDesWindow(Screen):
    def graph(self):
        df = pd.DataFrame(sheet.get_all_records())
        dfgui.show(df)

class RegistroWindow(Screen):
    def write(self):
        Id = self.id_data.text
        Age = self.age_data.text
        BMI = self.bmi_data.text
        Insulin = self.ins_data.text
        K = self.k_data.text
        Neutro = self.neu_data.text
        row = [Id, Age, BMI, Insulin, K, Neutro]
        sheet.insert_row(row, 2)
    def cleartext(self):
         self.id_data.text = ''
         self.age_data.text = ''
         self.bmi_data.text = ''
         self.ins_data.text = ''
         self.k_data.text = ''
         self.neu_data.text = ''
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()

class DiagnosticoWindow(Screen):
    def diagnosis(self):
        paciente = self.pac_data.text
        diagnostico = self.diag_data.text
        paciente = int(paciente)
        
        data = pd.DataFrame(sheet.get_all_records())
        r = data[data['1. NSS'] == paciente].index.item()
        sheet.update_cell(r+2, 7, diagnostico)
        
    def cleartext(self):
         self.pac_data.text = ''
         self.diag_data.text = ''
         
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()
      
class Email(Screen):
    def mail(self):
        df = pd.DataFrame(sheet.get_all_records())
        df_csv = df.to_csv()
        dfpart = MIMEText(df_csv, 'csv')

        email_user = 'biohackers.ens@gmail.com'
        email_send = self.mail_data.text
        subject = 'Base de datos de pacientes'

        msg = MIMEMultipart()
        msg ['From'] = email_user
        msg ['To'] = email_send
        msg ['Subject'] = subject
        msg.attach(dfpart)

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, 'Biohacks2019')

        server.sendmail(email_user, email_send, text)
        server.quit()
        
    def cleartext(self):
         self.mail_data.text = ''
         
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

        
class MyMainApp(App):
    def build(self):
        
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1280, 720)
        return kv

if __name__ == "__main__":
    MyMainApp().run()