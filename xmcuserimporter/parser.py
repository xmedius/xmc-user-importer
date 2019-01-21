import csv
import json
from .portal import Client


class Parser:

    def __init__(self, config_filename, csv_filename):
        self.csv_filename = csv_filename
        self.config = self._load_config(config_filename)
        self.client = Client(self.config['access_token'], self.config['enterprise_account'], endpoint=self.config['endpoint'])

        self.groups = self.client.groups()
        self.fax_numbers = self.client.fax_numbers()

        self.default_group_id = self.client.default_group()

    def import_users(self):
        with open(self.csv_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = self._build_user(row)
                json = self.client.add_user(user)
                if json['result'] == True:
                    print ("%s... Success" % row['email'])
                else:
                    print ("%s... Failed: %s" % (row['email'], json['errors'] ))


    def _build_user(self, row):
        user = {
            'username':                 row["username"],
            'email':                    row['email'],
            'role':                     'user',
            'group_id':                 self._group_id(row.get('group', '')),
            'language':                 row.get('language'),
            'time_zone':                row.get('time_zone'),
            'selected_fax_number':      self._fax_number_id(row.get("fax_number")),
            'first_name':               row.get('first_name'),
            'last_name':                row.get('last_name'),
            'salutation':               row.get('salutation'),
            'job_title':                row.get('job_title'),
            'company_name':             row.get('company_name'),
            'address':                  row.get('address'),
            'city':                     row.get('city'),
            'state':                    row.get('state'),
            'country':                  row.get('country'),
            'zip_code':                 row.get('zip_code'),
            'phone_number':             row.get('phone_number'),
            'mobile_number':            row.get('mobile_number')
        }

        if self.config['password_setup_mode'] == "user_choice":
            user['password_setup_type'] = 'user'
        elif self.config['password_setup_mode'] == "random":
            user['password_setup_type'] = 'auto'
        else: # password_setup_mode == manual,
            user['password_setup_type'] = 'force'
            user['password'] = user['password_confirmation'] = row['password']

        if user['selected_fax_number'] is None:
            user['fax_number_type']  = 'enterprise'
        else:
            user['fax_number_type']  = 'selected'

        return user

    def _group_id(self, group_name):
        if group_name == '':
            return self.default_group_id

        try:
            return self.groups.keys()[list(self.groups.values()).index(group_name)]
        except ValueError:
            return self.default_group_id

    def _fax_number_id(self, fax_number):
        for key, value in self.fax_numbers.items():
            if value['number'] == fax_number:
                return key

        return None

    def _load_config(self, config_filename):
        with open(config_filename) as json_data_file:
            data = json.load(json_data_file)
        return data
