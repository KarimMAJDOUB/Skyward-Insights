#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
##############################################################################
This module is designed to manage and validate JSON files,
specifically for airport data.
##############################################################################
"""
import os

class JsonAirport:
    FORMAT = "json"
    
    def __init__(self, json_path):
        assert isinstance(json_path, str)
        self.json_path = json_path
        self.validateJson()

    def validateJson(self):
        if not self.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")
        elif not self.isCorrectFormat():
            raise ValueError(f"File format must be {JsonAirport.FORMAT}")
        
    def __repr__(self):  
        return (f"Filename = {self.basename()}\n"
                f"Format = {JsonAirport.FORMAT}\n"
                f"Directory = {self.dirname()}\n"
                f"File exists = {self.exists()}\n")
    
    def exists(self):
        return os.path.isfile(self.json_path)

    def basename(self):
        return os.path.basename(self.json_path)

    def dirname(self):
        return os.path.dirname(os.path.abspath(self.json_path))

    def extension(self):
        _, ext = os.path.splitext(self.json_path)
        return ext.lstrip('.')

    def isCorrectFormat(self):
        return self.extension().lower() == JsonAirport.FORMAT