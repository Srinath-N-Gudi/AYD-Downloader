import cryptocode
import os
from EasyCode.EasyCode import ParseList
class _ED():
    @staticmethod
    def _encrypt(_data, _pswd):
        _new_data = []
        for _i in _data:
            _new_data.append(cryptocode.encrypt(_i, _pswd))
        return _new_data
    def _decrypt(_data, _pswd):
        _new_data = []
        for _i in _data:
            _new_data.append(cryptocode.decrypt(_i, _pswd))
        return _new_data
class DB():
    def __init__(self):
        self.pswd = "rockpython3.9"
    @property
    def settings(self):
        return Settings(self.pswd)
    @property
    def downloads_mp4(self):
        return Downloads_MP4(self.pswd)
    @property
    def downloads_mp3(self):
        return Downloads_MP3(self.pswd)
    @property
    def converting_data(self):
        return converter_data(self.pswd)
    @property
    def check_in(self):
        return check_in(self.pswd)
class Settings():
    def __init__(self, pswd):
        self.pswd = pswd
        self.file_save_name = "dbs.db"
    def save_data(self, data_list=[]):
        self.data = data_list
        self.encrypted_data = _ED._encrypt(self.data, self.pswd)
        self._sd(self.encrypted_data)
    def load_data(self):
        if os.path.exists("DBY"):
            if os.path.exists(f"DBY/{self.file_save_name}"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'r') as file:
                        self.saved_data = ParseList(file.readlines())
                        self.saved_confirmed_data = _ED._decrypt(self.saved_data, self.pswd)
                        return self.saved_confirmed_data
                except:
                    raise Exception("Failed to load data")
            else:
                open(f"DBY/{self.file_save_name}", 'x')
                return []
        else:
            os.mkdir("DBY")
            open(f"DBY/{self.file_save_name}", 'x')
            return []

        
    def _sd(self, _ed):
        _new_data = []
        for i in _ed:
            _new_data.append(i+"\n")
        status = self._wr(_new_data)
        if not status:
            raise Exception("Could not save data")
    def _wr(self, _data):
        _data_written = False
        if os.path.exists("DBY"):
            try:
                with open(f"DBY/{self.file_save_name}", 'w') as _file:
                    _file.writelines(_data)
                    _data_written = True
            except:
                _data_written = False
            if _data_written:
                return True
            else:
                return False
        else:
            os.mkdir("DBY")       
            if os.path.exists("DBY"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'w') as _file:
                        _file.writelines(_data)
                        _data_written = True
                except:
                    _data_written = False
                if _data_written:
                    return True
                else:
                    return False
        
class Downloads_MP4():
    def __init__(self, pswd):
        self.pswd = pswd
        self.file_save_name = "dbmp4.db"
    def save_data(self, data_list=[]):
        self.data = data_list
        self.encrypted_data = _ED._encrypt(self.data, self.pswd)
        self._sd(self.encrypted_data)
    def load_data(self):
        if os.path.exists("DBY"):
            if os.path.exists(f"DBY/{self.file_save_name}"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'r') as file:
                        self.saved_data = ParseList(file.readlines())
                        self.saved_confirmed_data = _ED._decrypt(self.saved_data, self.pswd)
                        return self.saved_confirmed_data
                except:
                    raise Exception("Failed to load data")
            else:
                open(f"DBY/{self.file_save_name}", 'x')
                return []
        else:
            os.mkdir("DBY")
            open(f"DBY/{self.file_save_name}", 'x')
            return []

        
    def _sd(self, _ed):
        _new_data = []
        for i in _ed:
            _new_data.append(i+"\n")
        status = self._wr(_new_data)
        if not status:
            raise Exception("Could not save data")
    def _wr(self, _data):
        _data_written = False
        if os.path.exists("DBY"):
            try:
                with open(f"DBY/{self.file_save_name}", 'w') as _file:
                    _file.writelines(_data)
                    _data_written = True
            except:
                _data_written = False
            if _data_written:
                return True
            else:
                return False
        else:
            os.mkdir("DBY")       
            if os.path.exists("DBY"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'w') as _file:
                        _file.writelines(_data)
                        _data_written = True
                except:
                    _data_written = False
                if _data_written:
                    return True
                else:
                    return False
class Downloads_MP3():
    def __init__(self, pswd):
        self.pswd = pswd
        self.file_save_name = "dbmp3.db"
    def save_data(self, data_list=[]):
        self.data = data_list
        self.encrypted_data = _ED._encrypt(self.data, self.pswd)
        self._sd(self.encrypted_data)
    def load_data(self):
        if os.path.exists("DBY"):
            if os.path.exists(f"DBY/{self.file_save_name}"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'r') as file:
                        self.saved_data = ParseList(file.readlines())
                        self.saved_confirmed_data = _ED._decrypt(self.saved_data, self.pswd)
                        return self.saved_confirmed_data
                except:
                    raise Exception("Failed to load data")
            else:
                open(f"DBY/{self.file_save_name}", 'x')
                return []
        else:
            os.mkdir("DBY")
            open(f"DBY/{self.file_save_name}", 'x')
            return []

        
    def _sd(self, _ed):
        _new_data = []
        for i in _ed:
            _new_data.append(i+"\n")
        status = self._wr(_new_data)
        if not status:
            raise Exception("Could not save data")
    def _wr(self, _data):
        _data_written = False
        if os.path.exists("DBY"):
            try:
                with open(f"DBY/{self.file_save_name}", 'w') as _file:
                    _file.writelines(_data)
                    _data_written = True
            except:
                _data_written = False
            if _data_written:
                return True
            else:
                return False
        else:
            os.mkdir("DBY")       
            if os.path.exists("DBY"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'w') as _file:
                        _file.writelines(_data)
                        _data_written = True
                except:
                    _data_written = False
                if _data_written:
                    return True
                else:
                    return False

class converter_data():
    def __init__(self, pswd):
        self.pswd = pswd
        self.file_save_name = "dbc.db"
    def save_data(self, data_list=[]):
        self.data = data_list
        self.encrypted_data = _ED._encrypt(self.data, self.pswd)
        self._sd(self.encrypted_data)
    def load_data(self):
        if os.path.exists("DBY"):
            if os.path.exists(f"DBY/{self.file_save_name}"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'r') as file:
                        self.saved_data = ParseList(file.readlines())
                        self.saved_confirmed_data = _ED._decrypt(self.saved_data, self.pswd)
                        return self.saved_confirmed_data
                except:
                    raise Exception("Failed to load data")
            else:
                open(f"DBY/{self.file_save_name}", 'x')
                return []
        else:
            os.mkdir("DBY")
            open(f"DBY/{self.file_save_name}", 'x')
            return []

        
    def _sd(self, _ed):
        _new_data = []
        for i in _ed:
            _new_data.append(i+"\n")
        status = self._wr(_new_data)
        if not status:
            raise Exception("Could not save data")
    def _wr(self, _data):
        _data_written = False
        if os.path.exists("DBY"):
            try:
                with open(f"DBY/{self.file_save_name}", 'w') as _file:
                    _file.writelines(_data)
                    _data_written = True
            except:
                _data_written = False
            if _data_written:
                return True
            else:
                return False
        else:
            os.mkdir("DBY")       
            if os.path.exists("DBY"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'w') as _file:
                        _file.writelines(_data)
                        _data_written = True
                except:
                    _data_written = False
                if _data_written:
                    return True
                else:
                    return False
class check_in():
    def __init__(self, pswd):
        self.pswd = pswd
        self.file_save_name = "dbcc.db"
    def save_data(self, data_list=[]):
        self.data = data_list
        self.encrypted_data = _ED._encrypt(self.data, self.pswd)
        self._sd(self.encrypted_data)
    def check(self):
        if os.path.exists("DBY"):
            if os.path.exists(f"DBY/{self.file_save_name}"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'r') as file:
                        self.saved_data = ParseList(file.readlines())
                        self.saved_confirmed_data = _ED._decrypt(self.saved_data, self.pswd)
                        return self.saved_confirmed_data
                except:
                    raise Exception("Failed to load data")
            else:
                open(f"DBY/{self.file_save_name}", 'x')
                return []
        else:
            os.mkdir("DBY")
            open(f"DBY/{self.file_save_name}", 'x')
            return []

        
    def _sd(self, _ed):
        _new_data = []
        for i in _ed:
            _new_data.append(i+"\n")
        status = self._wr(_new_data)
        if not status:
            raise Exception("Could not save data")
    def _wr(self, _data):
        _data_written = False
        if os.path.exists("DBY"):
            try:
                with open(f"DBY/{self.file_save_name}", 'w') as _file:
                    _file.writelines(_data)
                    _data_written = True
            except:
                _data_written = False
            if _data_written:
                return True
            else:
                return False
        else:
            os.mkdir("DBY")       
            if os.path.exists("DBY"):
                try:
                    with open(f"DBY/{self.file_save_name}", 'w') as _file:
                        _file.writelines(_data)
                        _data_written = True
                except:
                    _data_written = False
                if _data_written:
                    return True
                else:
                    return False
