import asyncio
from distutils.command.upload import upload
import time
from threading import Thread

from pypresence import InvalidPipe, Presence, DiscordNotFound

from .functions import path

class Discord:

    APP_ID = 957279570854301726

    @classmethod
    def init(cls):
        
        cls.connected = False
        cls.payload = {
            'start': time.time(),
            'details': None,
            'state': 'Climbing the mountain',
            }
        
        cls.thread = Thread(
            name='DiscordMainThread',
            target=cls.__init,
            daemon=True
        )
        cls.thread.start()

    @classmethod
    def __init(cls):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            cls.rpc = Presence(cls.APP_ID)
            cls.rpc.connect()
        except (InvalidPipe, ConnectionRefusedError):
            pass
        except DiscordNotFound:
            pass
        else:
            try:
                cls.rpc.update(**cls.payload)  
                
            except:
                pass
            else:
                cls.connected = True

    @classmethod
    def update(cls, details: str = None, state: str = None):
        Thread(
            name='DiscordUpdateThread',
            target=cls.__update,
            args=(details, state),
            daemon=True
        ).start()

    @classmethod
    def __update(cls, details: str, state: str):
        
        cls.payload = {
            'start': cls.payload['start'],
            'details': details or cls.payload['details'],
            'state': state or cls.payload['state']
        }
        
        if cls.thread is not None:
            cls.thread.join()
        if cls.connected:
            cls.rpc.update(**cls.payload)
            cls.rpc.update(large_image="logo", state = "Climbing the mountain")
