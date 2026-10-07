"""Optional GitHub token storage in the current Windows user's Credential Manager."""

import ctypes
import re
import sys
import uuid
from ctypes import wintypes

GENERIC = 1
LOCAL_MACHINE = 2  # Same user/computer across logins; does not roam to another PC.
NOT_FOUND = 1168
MAX_BLOB = 2560


class Credential(ctypes.Structure):
    # https://learn.microsoft.com/windows/win32/api/wincred/ns-wincred-credentialw
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


def credential_target(project, repository):
    if not isinstance(repository, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ):
        raise ValueError("Enter owner/repository before saving or using a token")
    return f"LazuriAdmin/GitHub/{uuid.UUID(project)}/{repository.lower()}"


def validate_token(token):
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Enter a GitHub token")
    token = token.strip()
    if any(ord(char) < 33 or ord(char) > 126 for char in token):
        raise ValueError(
            "A GitHub token must contain ASCII characters without spaces or line breaks"
        )
    return token


class WindowsCredentials:
    available = sys.platform == "win32"

    def __init__(self):
        self._api = None

    def api(self):
        if not self.available:
            raise ValueError(
                "Remembering tokens is supported only on Windows; enter a token to publish"
            )
        if self._api is None:
            try:
                api = ctypes.WinDLL("Advapi32.dll", use_last_error=True)
            except OSError:
                raise ValueError("Windows Credential Manager is unavailable") from None
            pointer = ctypes.POINTER(Credential)
            api.CredReadW.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                ctypes.POINTER(pointer),
            ]
            api.CredReadW.restype = wintypes.BOOL
            api.CredWriteW.argtypes = [pointer, wintypes.DWORD]
            api.CredWriteW.restype = wintypes.BOOL
            api.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
            api.CredDeleteW.restype = wintypes.BOOL
            api.CredFree.argtypes = [ctypes.c_void_p]
            api.CredFree.restype = None
            self._api = api
        return self._api

    @staticmethod
    def error():
        # Do not include secret blobs, request bodies or native exception reprs.
        return ValueError(f"Windows Credential Manager failed (code {ctypes.get_last_error()})")

    def get(self, target):
        if not self.available:
            return None
        api = self.api()
        pointer = ctypes.POINTER(Credential)()
        if not api.CredReadW(target, GENERIC, 0, ctypes.byref(pointer)):
            if ctypes.get_last_error() == NOT_FOUND:
                return None
            raise self.error()
        try:
            record = pointer.contents
            if not 0 < record.CredentialBlobSize <= MAX_BLOB:
                raise ValueError("Saved token is invalid; forget it and enter it again")
            try:
                return ctypes.string_at(record.CredentialBlob, record.CredentialBlobSize).decode(
                    "utf-8"
                )
            except UnicodeDecodeError:
                raise ValueError("Saved token is invalid; forget it and enter it again") from None
        finally:
            api.CredFree(pointer)

    def save(self, target, token):
        encoded = validate_token(token).encode("utf-8")
        if len(encoded) > MAX_BLOB:
            raise ValueError("Token exceeds the Windows credential size limit")
        blob = (ctypes.c_ubyte * len(encoded)).from_buffer_copy(encoded)
        record = Credential(
            Type=GENERIC,
            TargetName=target,
            Comment="Lazuri Admin GitHub publication token",
            CredentialBlobSize=len(encoded),
            CredentialBlob=blob,
            Persist=LOCAL_MACHINE,
            UserName="GitHub token",
        )
        if not self.api().CredWriteW(ctypes.byref(record), 0):
            raise self.error()

    def delete(self, target):
        if not self.api().CredDeleteW(target, GENERIC, 0):
            if ctypes.get_last_error() != NOT_FOUND:
                raise self.error()
