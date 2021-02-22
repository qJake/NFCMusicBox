import os
import json
import utils

class TagStorage:
    def __init__(self, storage_path, dbname='nfc.json'):
        self.storage_path = storage_path
        self.dbname = dbname
        
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
    
    def get_tags(self):
        data = self._read()
        if 'tags' in data:
            return data['tags']
        return []
    
    def add_tag(self, tag):
        if not 'name' in tag or not 'uid' in tag:
            raise 'Tag is missing name or uid.'

        data = self._read()

        if data['tags'] is None:
            data['tags'] = []

        data['tags'].append(tag)

        self._write(data)

    def remove_tag(self, tag_uid):
        data = self._read()

        if data['tags'] is not None:
            tag = utils.select_tag_index(data['tags'], tag_uid)

            if tag is not None:
                del data['tags'][tag]
                os.remove(self.to_full_path(data['tags']['name']))

        self._write(data)
    
    def add_song(self, songfile, secure_name):
        path = self.to_full_path(secure_name)
        songfile.save(path)

    def to_full_path(self, name):
        return os.path.join((self.storage_path[:-1] if self.storage_path.endswith(os.sep) else self.storage_path) + os.sep, name)

    def _read(self):
        path = self.to_full_path(self.dbname)
        if not os.path.exists(path):
            with open(path, 'w+') as f:
                f.write('{}')

        with open(path) as f:
            j = json.load(f)
        
        return j
    
    def _write(self, json_data):
        path = self.to_full_path(self.dbname)
        with open(path, 'w+') as f:
            json.dump(json_data, f)
    