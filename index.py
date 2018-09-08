import requests
import lxml.html

from parsers.act import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser


if __name__ == '__main__':

  arc2AgeParser = Arc2AgeParser()
  arc2AgeParser.analize()
  # for staff in arc2AgeParser.staff:
    # arc2AgeParser.get_club_data(staff['name'], staff['url'])
    # arc2AgeParser.get_rowers_data(staff['name'])

