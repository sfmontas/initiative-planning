from typing import Dict, List, Callable

from common.events.events import Event

streams: Dict[str, List[Event]] = {}

streams_handlers: Dict[str, List[Callable]] = {}


def publish(stream_name: str, event: Event):
    stream = streams.get(stream_name)

    if stream is None:
        stream = [event]
        streams[stream_name] = stream

    stream.append(event)

    stream_handlers = streams_handlers.get(stream_name)

    if stream_handlers is not None:
        for stream_handler in stream_handlers:
            stream_handler(event)


def register_stream_handler(stream_name: str, stream_handler: Callable):
    stream_handlers = streams_handlers.get(stream_name)

    if stream_handlers is None:
        streams_handlers[stream_name] = [stream_handler]
    else:
        stream_handlers.append(stream_handler)
