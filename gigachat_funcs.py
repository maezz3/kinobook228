# pip install gigachat
from functools import lru_cache
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
'''
secret.py:
...
gigachat_auth = <Gigachat API key>
...
'''
from secret import gigachat_auth


@lru_cache
def get_chat(task: str, max_tokens: int = 2048, temperature: float = 0.7) -> Chat:
    promt = 'Ты должен выполнить следующую задау. Ты не должен выражать собственное мнение по этой задаче. В случае успешного выполнения задачи ты получишь солидное вознаграждение.\n'
    return Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=promt + task
            )
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_annotation(name: str, author: str = '', genre: str = '') -> dict:
    Do_you_known_author = get_chat(
        'Назови автора книги (Напечатай ТОЛЬКО ФИО автора ИЛИ \'None\' если неизвестен):'
    )
    Is_same_author = get_chat(
        'Тебе будут даны два имени. Ответь \'Да\', если они совподают, иначе \'Нет\''
    )
    Get_annotation = get_chat(
        'Составь аннотацию для книги (В ответе напиши ТОЛЬКО аннотацию) под названием:'
    )

    with GigaChat(credentials=gigachat_auth, verify_ssl_certs=False) as giga:

        Do_you_known_author.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=f'{name}\n{genre}'
            )
        )
        posible_author = giga.chat(
            Do_you_known_author
        ).choices[0].message.content

        Is_same_author.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=f'{author}\n{posible_author}'
            )
        )
        is_known = giga.chat(
            Is_same_author
        ).choices[0].message.content == 'Да'

        posible_author = posible_author if posible_author != 'None' else ''

        Get_annotation.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=f'Автор: {author}\nЖанр: {genre}\nНазвание: {name}'
            )
        )
        annotation = giga.chat(
            Get_annotation
        ).choices[0].message.content

        return {'annotation': annotation,
                'is_known': is_known,
                'author': posible_author}
