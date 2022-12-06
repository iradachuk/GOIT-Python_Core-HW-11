from  collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value 


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) != 10:
            raise ValueError('Phone number must contain of 10 symbols')
        if not value.isnumeric():
            raise ValueError('Wrong number!')
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y-%m-%d').date()
        if birth_date > today:
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False
    
    def change_phone(self, phones):
        for phone in phones:
            if not self.remove_phone(phone):
                self.add_phone(phone)

    def get_info(self):
        phones_info = ''
        birthday = ''
        for phone in self.phones:
            phones_info += f'{phone.value}, '
        if self.birthday:
            birthday += f'Birthday: {self.birthday.value}'
        return f'{self.name.value} - {phones_info[:-2]} {birthday}'

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError('This contact doesn\'t have attribute birthday')
        current_date = datetime.now().date()
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        next_year = current_date.year
        if current_date.month > birthday.month and current_date.day > birthday.day:
            next_year += 1
        next_birthday = datetime(year=next_year, month=birthday.month, day=birthday.day)
        return (current_date - next_birthday.date()).days
         

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, value):
        if self.data.get(value):
            return self.data.get(value)
        for record in self.data.values():
            for phone in record.phones:
                if phone.value == value:
                    return record
        raise ValueError("Contact with this value does not exist.")


    def iterator(self, count = 5):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page


address_book = AddressBook()