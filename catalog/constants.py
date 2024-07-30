from enum import Enum

# loan status of bookinstance
LOAN_STATUS = (
  ('m', 'Maintenance'),
  ('o', 'On loan'),
  ('a', 'Available'),
  ('r', 'Reserved'),
)

def get_loan_status(name):
    status_dict = {name: code for code, name in LOAN_STATUS}
    return status_dict.get(name)

PAGINATE_BY = 3

DEFAULT_DATE = '03/11/2003'
