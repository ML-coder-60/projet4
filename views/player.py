"""Class Menu"""
# coding: utf-8


class Player:
    def __init__(self, data):
        self.Last_Name = data['Last Name']
        self.First_Name = data['First Name']
        self.Date_Birth = data['Date Birth']
        self.Gender = data['Gender']
        self.Ranking = data['Ranking']

    def __str__(self):
        s = "Last Name  : "+self.Last_Name+"\n"
        s += "First Name : "+self.First_Name+"\n"
        s += "Date Birth : "+self.Date_Birth+"\n"
        s += "Gender     : "+self.Gender+"\n"
        s += "Ranking    : "+self.Ranking+"\n"
        return s
