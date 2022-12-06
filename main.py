from classes import address_book, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'No user with given name, try again!'
        except ValueError:
            return 'This user can not be added!'
        except IndexError:
            return 'Unknown command or parameters, please try again!'
    return inner


def greeting():
    return 'How can I help you?'


def good_bye():
    return 'Good bye!'


@input_error
def add_contact(data):
    name, *phones = data.strip().split()
    if name in address_book:
        raise ValueError('This contact already exist.')
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    address_book.add_record(record)
    return f'The user with name {name} and phone {phone} was added!'
    

@input_error
def change_phone(data):
    name, *phones = data.strip().split()
    record = address_book[name]
    record.change_phone(phones)
    return f'The phone number for name {name} was changed!'


@input_error
def show_phone(value):
    return address_book.search(value.strip()).get_info()


def show_all():
    contacts = ''
    page_number = 1
    for page in address_book.iterator():
        contacts += f'Page #{page_number}\n'
        for record in page:
            contacts += f'{record.get_info()}\n'
        page_number += 1
    return contacts


@input_error
def add_birthday(data):
    name, birthday = data.strip().split()
    record = address_book[name]
    record.add_birthday(birthday)
    return f'The birthday {birthday} added to {name}.'


@input_error
def birthday(name):
    name = name.strip()
    record = address_book[name]
    return f'{name}\'s birthday will be in {record.days_to_birthday()} day(s).'
        

def change_input(user_input):
    new_input = user_input
    data = ''
    for key in COMMANDS:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()
        

def reaction_func(reaction):
    return COMMANDS.get(reaction, break_func)


def break_func():
    return 'Wrong enter.'    
    

COMMANDS = {
    'hello': greeting,
    'add': add_contact,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'birthday': add_birthday,
    'days to birthday': birthday, 
    'good bye': good_bye,
    'exit': good_bye,
    'close': good_bye
    }


def main():
    while True:
        user_input = input('>>> ')
        if user_input == '.':
            break
        result = change_input(user_input)
        print(result)
        if result == good_bye:
            break

               
if __name__ == '__main__':
    main()