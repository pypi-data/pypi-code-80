import threading
import asyncio
import json
import traceback
import re
import os
import sys

from .. import objects
from .. import exceptions
from ..enums import events, action


class thread(threading.Thread):
    processing = False

    def __init__(self, library, handler_id, cache):
        threading.Thread.__init__(self)
        self.daemon = True
        self.handler_id = handler_id
        self.cache = cache

        self.library = library
        self.packages = []


    def run(self):
        self.setName(f"{self.cache}_{self.handler_id}")
        self.library.tools.system_message(
            module = "package_handler", 
            level = "debug",
            write = f"{self.getName()} is started")

        self.all_messages = self.library.tools.values.ALL_MESSAGES.value
        self.add_mentions = self.library.tools.values.ADD_MENTIONS.value
        self.mentions = self.library.tools.getBotMentions()

        self.thread_loop = asyncio.new_event_loop()
        self.thread_loop.set_exception_handler(self.exception_handler)
        asyncio.set_event_loop(self.thread_loop)
        self.library.tools.http.create_session(self)

        self.thread_loop.run_forever()

    def exception_handler(self, loop, context):
        try:
            raise context['exception']

        except exceptions.Quit as message:
            self.library.tools.system_message(
                module = "framework",
                level = "debug",
                write = "Attached message: " + message
            )
            
            os._exit(1)

        except exceptions.LibraryReload as message:
            self.library.tools.system_message(
                module = "framework",
                level = "debug",
                write = "Attached message: " + message
            )

            self.library.upload()

        except exceptions.CallVoid as e:
            if e[0] == "$" and e.count("_") == 1:
                peer_id, from_id = str(e)[1:].split("_")
                handler = self.library.handlers['void']
                module = self.library.modules[handler.__module__]

                package = objects.package({
                    'peer_id': int(peer_id), 
                    'from_id': int(from_id), 
                    'items': [self.library.tools.values.NOREPLY]
                    })
                self.thread_loop.create_task(handler(module, self.library.tools, package))

            else:
                self.library.tools.system_message(
                    module = "framework",
                    level = "debug",
                    write = "Attempted to call void with incorrect task: " + e
                )


        except Exception as e:
            print(traceback.format_exc())
            
            self.library.tools.system_message(
                module = "traceback",
                level = "debug",
                write = traceback.format_exc())

            self.library.tools.system_message(
                module = self.name,
                level = "error", 
                write = "Appeared exception: " + e)

    def create_task(self, package):
        if isinstance(package, objects.package):
            if package.type in [events.message_new, *self.library.handlers['events']]:
                asyncio.run_coroutine_threadsafe(self.resolver(package), self.thread_loop)

        else:
            asyncio.run_coroutine_threadsafe(self.__start_module(package), self.thread_loop)

    async def __start_module(self, package):
        self.thread_loop.create_task(package(self.library.tools))

    async def resolver(self, package):
        if package.type == events.message_new:
            package.params.action = False
            package.params.payload = False

            if hasattr(package, 'action'): 
                package.params.action = True
                package.action.type = getattr(action, package.action.type)

            elif hasattr(package, 'payload'): 
                package.params.payload = True
                package.payload = json.loads(package.payload)
            
            elif package.text != '':
                message = package.text.split()
                package.params.command = False
                if len(message) > 1 and ((message[0].lower() in self.mentions) or (message[0][:-1].lower() in self.mentions)):
                    package.params.gment = message.pop(0)
                    package.params.command = True

                package.items = message
                package.params.mentions = [self.parse_mention(i) for i in re.findall(r'\[(.*?)\]', package.text)]

                if self.add_mentions:
                    package.params.mentions.extend(list(set(message) & set(self.mentions)))
                
            elif len(package.attachments) > 0: 
                package.params.attachments = True

            await self.handler(package)
            
        else:
            await self.handler(package)
            

    async def handler(self, package: objects.package):
        self.library.handlers['void']
        try:
            package.items.append(self.library.tools.values.ENDLINE)
            if self.library.tools.wait_check(package):
                self.library.tools._tools__waiting_replies[f"${package.peer_id}_{package.from_id}"] = package

            elif package.type == events.message_new:
                if package.params.action:
                    handler = self.library.action_handlers[package.action.type]
                    module = self.library.modules[handler.__module__]
                    
                    self.thread_loop.create_task(handler(module, self.library.tools, package))

                elif package.params.command and len(package.items) > 0 and package.items[0] in self.library.handlers['priority'].keys():
                    handler = self.library.handlers['priority'][package.items[0]]
                    module = self.library.modules[handler.__module__]
                    
                    self.thread_loop.create_task(handler(module, self.library.tools, package))

                elif self.library.void_react:
                    if self.all_messages or package.params.command:
                        handler = self.library.handlers['void']
                        module = self.library.modules[handler.__module__]

                        self.thread_loop.create_task(handler(module, self.library.tools, package))

            elif package.type in self.library.handlers['events'].keys():
                handler = self.library.handlers['events'][package.type]
                module = self.library.modules[handler.__module__]

                self.thread_loop.create_task(handler(module, self.library.tools, package))

        except Exception as e:
            print(e)

    
    def parse_mention(self, ment) -> objects.mention:
        page_id, call = ment[0: ment.find('|')], ment[ment.find('|') + 1:]

        page_id = page_id.replace('id', '')
        page_id = page_id.replace('club', '-')
        page_id = page_id.replace('public', '-')
            
        return objects.mention(int(page_id), call)