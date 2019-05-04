from src.Parsers.EmailParser import EmailParser
from src.services.db import db
import re


EmailParser('https://ksena.com.ua/contacts','ksena').run()
