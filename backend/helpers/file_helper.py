import uuid

from py3crdt.gset import GSet


def merge_file_content(file_path: str, content_to_merge: str):
    with open(file_path, 'w+') as file:
        file_content = GSet(id=str(uuid.uuid1()))
        user_additions = GSet(id=str(uuid.uuid1()))
        file_content.add(file.read())
        user_additions.add(content_to_merge)

        file_content.merge(user_additions)

        content = ''.join(file_content.payload)
        file.write(content)
        return content
