"""Class Menu"""
# coding: utf-8


class Tournament:
    def __init__(self, data):
        self.Name = data['Name']
        self.Location = data['Location']
        self.Date = data['Date']
        self.Nbr_of_turn = data['Nbr_of_turn']
        self.Time_controls = data['Time_controls']
        self.Description = data['Description']

class Turn:
    