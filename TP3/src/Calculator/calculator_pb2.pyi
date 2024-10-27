from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddRequest(_message.Message):
    __slots__ = ("first_number", "second_number")
    FIRST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECOND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    first_number: int
    second_number: int
    def __init__(self, first_number: _Optional[int] = ..., second_number: _Optional[int] = ...) -> None: ...

class SubtractRequest(_message.Message):
    __slots__ = ("first_number", "second_number")
    FIRST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECOND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    first_number: int
    second_number: int
    def __init__(self, first_number: _Optional[int] = ..., second_number: _Optional[int] = ...) -> None: ...

class MultiplyRequest(_message.Message):
    __slots__ = ("first_number", "second_number")
    FIRST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECOND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    first_number: int
    second_number: int
    def __init__(self, first_number: _Optional[int] = ..., second_number: _Optional[int] = ...) -> None: ...

class DivideRequest(_message.Message):
    __slots__ = ("first_number", "second_number")
    FIRST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECOND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    first_number: int
    second_number: int
    def __init__(self, first_number: _Optional[int] = ..., second_number: _Optional[int] = ...) -> None: ...

class AddResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class SubtractResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class MultiplyResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class DivideResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: float
    def __init__(self, result: _Optional[float] = ...) -> None: ...
