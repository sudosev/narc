import requests
import os
import time

start = time.time()
url_pastebin_scraping = 'https://scrape.pastebin.com/api_scraping.php'
limit = 250
pastes_dir = '/home/ubuntu/pastes/'  # Trailing slash is important here!
originals_dir = '/home/ubuntu/pastes/origraw/'  # Trailing slash is important here!
logfile = pastes_dir + 'pastes.log'


def posh_find(text):
    if "[System.Convert]::" in text:
        return True
    if "FromBase64String(" in text:
        return True
    if "New-Object System.IO." in text:
        return True
    if "[System.Net." in text:
        return True
    if "System.Reflection.AssemblyName" in text:
        return True
    if 'powershell -' in text:
        return True
    if 'powershell.exe -' in text:
        return True
    if '\1.0\powershell.exe' in text:
        return True
    if 'PowerShell -' in text:
        return True
    if 'PowerShell.exe -' in text:
        return True
    if 'cG93ZXJzaGVsbC' in text:
        return True
    if 'UG93ZXJTaGVsbC' in text:
        return True
    if "<PCSettings>" in text:
        return True
    if "<DeepLink>" in text:
        return True
    if "So MAny scrapers hahahaha" in text:
        return True
    # Added a "double-check" for camel-casing by lowering text.
    # Probably lots more to do to counter PowerShell obfuscation.
    if "[system.convert]::" in text.lower():
        return True
    if "frombase64string(" in text.lower():
        return True
    if "new-object system.io." in text.lower():
        return True
    if "[system.net." in text.lower():
        return True
    if "system.reflection.assemblyname" in text.lower():
        return True


def dec_find(text):
    if '77 90 144 0 3 0 4 0' in text:
        return True
    if '77 90 232 0 0 0 0 91' in text:
        return True
    if '77 90 144 0 3 0 0 0' in text:
        return True
    if '77 90 80 0 2 0 0 0' in text:
        return True
    if '77 90 0 0 0 0 0 0' in text:
        return True
    if '77 90 65 82 85 72 137 229' in text:
        return True
    if '77 90 128 0 1 0 0 0' in text:
        return True
    if '77,90,144,0,3,0,4,0,' in text:
        return True
    if '77,90,232,0,0,0,0,91,' in text:
        return True
    if '77,90,144,0,3,0,0,0,' in text:
        return True
    if '77,90,80,0,2,0,0,0,' in text:
        return True
    if '77,90,0,0,0,0,0,0,' in text:
        return True
    if '77,90,65,82,85,72,137,229,' in text:
        return True
    if '77,90,128,0,1,0,0,0,' in text:
        return True
    if '77, 90, 144, 0, 3, 0, 4, 0,' in text:
        return True
    if '77, 90, 232, 0, 0, 0, 0, 91,' in text:
        return True
    if '77, 90, 144, 0, 3, 0, 0, 0,' in text:
        return True
    if '77, 90, 80, 0, 2, 0, 0, 0,' in text:
        return True
    if '77, 90, 0, 0, 0, 0, 0, 0,' in text:
        return True
    if '77, 90, 65, 82, 85, 72, 137, 229,' in text:
        return True
    if '77, 90, 128, 0, 1, 0, 0, 0,' in text:
        return True


def bin_find(text):
    if '010011010101101000000000000000000000000000000000' in text:
        return True
    if '010011010101101001000001010100100101010101001000' in text:
        return True
    if '010011010101101001010000000000000000001000000000' in text:
        return True
    if '010011010101101010000000000000000000000100000000' in text:
        return True
    if '010011010101101010010000000000000000001100000000' in text:
        return True
    if '010011010101101011101000000000000000000000000000' in text:
        return True
    if '0100 1101 0101 1010 0000 0000 0000 0000 0000 0000 0000 0000' in text:
        return True
    if '0100 1101 0101 1010 0100 0001 0101 0010 0101 0101 0100 1000' in text:
        return True
    if '0100 1101 0101 1010 0101 0000 0000 0000 0000 0010 0000 0000' in text:
        return True
    if '0100 1101 0101 1010 1000 0000 0000 0000 0000 0001 0000 0000' in text:
        return True
    if '0100 1101 0101 1010 1001 0000 0000 0000 0000 0011 0000 0000' in text:
        return True
    if '0100 1101 0101 1010 1110 1000 0000 0000 0000 0000 0000 0000' in text:
        return True
    if '01 00 11 01 01 01 10 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' in text:
        return True
    if '01 00 11 01 01 01 10 10 01 00 00 01 01 01 00 10 01 01 01 01 01 00 10 00' in text:
        return True
    if '01 00 11 01 01 01 10 10 01 01 00 00 00 00 00 00 00 00 00 10 00 00 00 00' in text:
        return True
    if '01 00 11 01 01 01 10 10 10 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00' in text:
        return True
    if '01 00 11 01 01 01 10 10 10 01 00 00 00 00 00 00 00 00 00 11 00 00 00 00' in text:
        return True
    if '01 00 11 01 01 01 10 10 11 10 10 00 00 00 00 00 00 00 00 00 00 00 00 00' in text:
        return True


def b64_find(text):
    if 'TVqQAAMAAAAEAAAA' in text:
        return True
    if 'TVpQAAIAAAAEAA8A' in text:
        return True
    if 'TVoAAAAAAAAAAAAA' in text:
        return True
    if 'TVpBUlVIieVIgewg' in text:
        return True
    if 'TVqAAAEAAAAEABAA' in text:
        return True
    if 'TVroAAAAAFtSRVWJ' in text:
        return True
    if 'TVqQAAMABAAAAAAA' in text:
        return True
    if 'TVpBUlVIieVIgewgAAAA' in text:
        return True
    if 'kJCQkE1aQVJVSInlSIHsIAAAA' in text:
        return True


def doublebase_find(text):
    if 'VFZxUUFBTUFBQUFFQUFBQ' in text:
        return True
    if 'VFZwUUFBSUFBQUFFQUE4Q' in text:
        return True
    if 'VFZvQUFBQUFBQUFBQUFBQ' in text:
        return True
    if 'VFZwQlVsVklpZVZJZ2V3Z' in text:
        return True
    if 'VFZxQUFBRUFBQUFFQUJBQ' in text:
        return True
    if 'VFZyb0FBQUFBRnRTUlZXS' in text:
        return True
    if 'VFZxUUFBTUFCQUFBQUFBQ' in text:
        return True


def exe_find(text):
    if '\x4d\x5a\x90\x00\x03\x00\x00\x00' in text:
        return True
    if '\x4d\x5a\x50\x00\x02\x00\x00\x00' in text:
        return True
    if '\x4d\x5a\x00\x00\x00\x00\x00\x00' in text:
        return True
    if '\x4d\x5a\x41\x52\x55\x48\x89\xe5' in text:
        return True
    if '\x4d\x5a\x80\x00\x01\x00\x00\x00' in text:
        return True
    if '\x4d\x5a\x90\x00\x03\x00\x04\x00' in text:
        return True
    if '\x4d\x5a\xe8\x00\x00\x00\x00\x5b' in text:
        return True


def hex_find(text):
    if '4d5a900003000000' in text:
        return True
    if '4D5A900003000000' in text:
        return True
    if '4d5a500002000000' in text:
        return True
    if '4D5A500002000000' in text:
        return True
    if '4d5a000000000000' in text:
        return True
    if '4D5A000000000000' in text:
        return True
    if '4d5a4152554889e5' in text:
        return True
    if '4D5A4152554889E5' in text:
        return True
    if '4d5a800001000000' in text:
        return True
    if '4D5A800001000000' in text:
        return True
    if '4d5a900003000400' in text:
        return True
    if '4D5A900003000400' in text:
        return True
    if '4d5ae8000000005b' in text:
        return True
    if '4D5AE8000000005B' in text:
        return True
    if '4d 5a 90 00 03 00 04 00' in text:
        return True
    if '4D 5A 90 00 03 00 04 00' in text:
        return True
    if '4d 5a e8 00 00 00 00 5b' in text:
        return True
    if '4D 5A E8 00 00 00 00 5B' in text:
        return True
    if '4d 5a 90 00 03 00 00 00' in text:
        return True
    if '4D 5A 90 00 03 00 00 00' in text:
        return True
    if '4d 5a 50 00 02 00 00 00' in text:
        return True
    if '4D 5A 50 00 02 00 00 00' in text:
        return True
    if '4d 5a 00 00 00 00 00 00' in text:
        return True
    if '4D 5A 00 00 00 00 00 00' in text:
        return True
    if '4d 5a 41 52 55 48 89 e5' in text:
        return True
    if '4D 5A 41 52 55 48 89 E5' in text:
        return True
    if '4d 5a 80 00 01 00 00 00' in text:
        return True
    if '4D 5A 80 00 01 00 00 00' in text:
        return True
    if '4d 5a 90 00 03 00 04 00' in text:
        return True
    if '4D 5A 90 00 03 00 04 00' in text:
        return True
    if '4d 5a e8 00 00 00 00 5b' in text:
        return True
    if '4D 5A E8 00 00 00 00 5B' in text:
        return True
    if '0x4d,0x5a,0x90,0x00,0x03,0x00,0x04,0x00' in text:
        return True
    if '0x4D,0x5A,0x90,0x00,0x03,0x00,0x04,0x00' in text:
        return True
    if '0x4d,0x5a,0xe8,0x00,0x00,0x00,0x00,0x5b' in text:
        return True
    if '0x4D,0x5A,0xE8,0x00,0x00,0x00,0x00,0x5B' in text:
        return True
    if '0x4d,0x5a,0x90,0x00,0x03,0x00,0x00,0x00' in text:
        return True
    if '0x4D,0x5A,0x90,0x00,0x03,0x00,0x00,0x00' in text:
        return True
    if '0x4d,0x5a,0x50,0x00,0x02,0x00,0x00,0x00' in text:
        return True
    if '0x4D,0x5A,0x50,0x00,0x02,0x00,0x00,0x00' in text:
        return True
    if '0x4d,0x5a,0x00,0x00,0x00,0x00,0x00,0x00' in text:
        return True
    if '0x4D,0x5A,0x00,0x00,0x00,0x00,0x00,0x00' in text:
        return True
    if '0x4d,0x5a,0x41,0x52,0x55,0x48,0x89,0xe5' in text:
        return True
    if '0x4D,0x5A,0x41,0x52,0x55,0x48,0x89,0xE5' in text:
        return True
    if '0x4d,0x5a,0x80,0x00,0x01,0x00,0x00,0x00' in text:
        return True
    if '0x4D,0x5A,0x80,0x00,0x01,0x00,0x00,0x00' in text:
        return True
    if '0x4d,0x5a,0x90,0x00,0x03,0x00,0x04,0x00' in text:
        return True
    if '0x4D,0x5A,0x90,0x00,0x03,0x00,0x04,0x00' in text:
        return True
    if '0x4d,0x5a,0xe8,0x00,0x00,0x00,0x00,0x5b' in text:
        return True
    if '0x4D,0x5A,0xE8,0x00,0x00,0x00,0x00,0x5B' in text:
        return True


def hexbase_find(text):
    if '5456715141414d414141414541414141' in text:
        return True
    if '5456715141414D414141414541414141' in text:
        return True
    if '54 56 71 51 41 41 4d 41 41 41 41 45 41 41 41 41' in text:
        return True
    if '54 56 71 51 41 41 4D 41 41 41 41 45 41 41 41 41' in text:
        return True
    if '54567051414149414141414541413841' in text:
        return True
    if '54 56 70 51 41 41 49 41 41 41 41 45 41 41 38 41' in text:
        return True
    if '54566f41414141414141414141414141' in text:
        return True
    if '54566F41414141414141414141414141' in text:
        return True
    if '54 56 6f 41 41 41 41 41 41 41 41 41 41 41 41 41' in text:
        return True
    if '54 56 6F 41 41 41 41 41 41 41 41 41 41 41 41 41' in text:
        return True
    if '54567042556c56496965564967657767' in text:
        return True
    if '54567042556C56496965564967657767' in text:
        return True
    if '54 56 70 42 55 6c 56 49 69 65 56 49 67 65 77 67' in text:
        return True
    if '54 56 70 42 55 6C 56 49 69 65 56 49 67 65 77 67' in text:
        return True
    if '54567141414145414141414541424141' in text:
        return True
    if '54 56 71 41 41 41 45 41 41 41 41 45 41 42 41 41' in text:
        return True
    if '5456726f41414141414674535256574a' in text:
        return True
    if '5456726F41414141414674535256574A' in text:
        return True
    if '54 56 72 6f 41 41 41 41 41 46 74 53 52 56 57 4a' in text:
        return True
    if '54 56 72 6F 41 41 41 41 41 46 74 53 52 56 57 4A' in text:
        return True
    if '5456715141414d414241414141414141' in text:
        return True
    if '5456715141414D414241414141414141' in text:
        return True
    if '54 56 71 51 41 41 4d 41 42 41 41 41 41 41 41 41' in text:
        return True
    if '54 56 71 51 41 41 4D 41 42 41 41 41 41 41 41 41' in text:
        return True


def basehex_find(text):
    if 'NGQ1YTkwMDAwMzAwMDAwMA' in text:
        return True
    if 'NEQ1QTkwMDAwMzAwMDAwMA' in text:
        return True
    if 'NGQ1YTUwMDAwMjAwMDAwMA' in text:
        return True
    if 'NEQ1QTUwMDAwMjAwMDAwMA' in text:
        return True
    if 'NGQ1YTAwMDAwMDAwMDAwMA' in text:
        return True
    if 'NEQ1QTAwMDAwMDAwMDAwMA' in text:
        return True
    if 'NGQ1YTQxNTI1NTQ4ODllNQ' in text:
        return True
    if 'NEQ1QTQxNTI1NTQ4ODlFNQ' in text:
        return True
    if 'NGQ1YTgwMDAwMTAwMDAwMA' in text:
        return True
    if 'NEQ1QTgwMDAwMTAwMDAwMA' in text:
        return True
    if 'NGQ1YTkwMDAwMzAwMDQwMA' in text:
        return True
    if 'NEQ1QTkwMDAwMzAwMDQwMA' in text:
        return True
    if 'NGQ1YWU4MDAwMDAwMDA1Yg' in text:
        return True
    if 'NEQ1QUU4MDAwMDAwMDA1Qg' in text:
        return True
    if 'NGQgNWEgOTAgMDAgMDMgMDAgMDQgMDA' in text:
        return True
    if 'NEQgNUEgOTAgMDAgMDMgMDAgMDQgMDA' in text:
        return True
    if 'NGQgNWEgZTggMDAgMDAgMDAgMDAgNWI' in text:
        return True
    if 'NEQgNUEgRTggMDAgMDAgMDAgMDAgNUI' in text:
        return True
    if 'NGQgNWEgOTAgMDAgMDMgMDAgMDAgMDA' in text:
        return True
    if 'NEQgNUEgOTAgMDAgMDMgMDAgMDAgMDA' in text:
        return True
    if 'NGQgNWEgNTAgMDAgMDIgMDAgMDAgMDA' in text:
        return True
    if 'NEQgNUEgNTAgMDAgMDIgMDAgMDAgMDA' in text:
        return True
    if 'NGQgNWEgMDAgMDAgMDAgMDAgMDAgMDA' in text:
        return True
    if 'NEQgNUEgMDAgMDAgMDAgMDAgMDAgMDA' in text:
        return True
    if 'NGQgNWEgNDEgNTIgNTUgNDggODkgZTU' in text:
        return True
    if 'NEQgNUEgNDEgNTIgNTUgNDggODkgRTU' in text:
        return True
    if 'NGQgNWEgODAgMDAgMDEgMDAgMDAgMDA' in text:
        return True
    if 'NEQgNUEgODAgMDAgMDEgMDAgMDAgMDA' in text:
        return True
    if 'NGQgNWEgOTAgMDAgMDMgMDAgMDQgMDA' in text:
        return True
    if 'NEQgNUEgOTAgMDAgMDMgMDAgMDQgMDA' in text:
        return True
    if 'NGQgNWEgZTggMDAgMDAgMDAgMDAgNWI' in text:
        return True
    if 'NEQgNUEgRTggMDAgMDAgMDAgMDAgNUI' in text:
        return True
    if 'MHg0ZCwweDVhLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwNCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwNCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4ZTgsMHgwMCwweDAwLDB4MDAsMHgwMCwweDViCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4RTgsMHgwMCwweDAwLDB4MDAsMHgwMCwweDVCCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4NTAsMHgwMCwweDAyLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4NTAsMHgwMCwweDAyLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4NDEsMHg1MiwweDU1LDB4NDgsMHg4OSwweGU1Cg' in text:
        return True
    if 'MHg0RCwweDVBLDB4NDEsMHg1MiwweDU1LDB4NDgsMHg4OSwweEU1Cg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4ODAsMHgwMCwweDAxLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4ODAsMHgwMCwweDAxLDB4MDAsMHgwMCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwNCwweDAwCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4OTAsMHgwMCwweDAzLDB4MDAsMHgwNCwweDAwCg' in text:
        return True
    if 'MHg0ZCwweDVhLDB4ZTgsMHgwMCwweDAwLDB4MDAsMHgwMCwweDViCg' in text:
        return True
    if 'MHg0RCwweDVBLDB4RTgsMHgwMCwweDAwLDB4MDAsMHgwMCwweDVCCg' in text:
        return True


def hexbin_find(text):
    if '303130303131303130313031313031303030303030303030303030303030303030303030303030303030303030303030' in text:
        return True
    if '303130303131303130313031313031303031303030303031303130313030313030313031303130313031303031303030' in text:
        return True
    if '303130303131303130313031313031303031303130303030303030303030303030303030303031303030303030303030' in text:
        return True
    if '303130303131303130313031313031303130303030303030303030303030303030303030303030313030303030303030' in text:
        return True
    if '303130303131303130313031313031303130303130303030303030303030303030303030303031313030303030303030' in text:
        return True
    if '303130303131303130313031313031303131313031303030303030303030303030303030303030303030303030303030' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 30 31 30 30 30 30 30 31 30 31 30 31 30 30 31 30 30 31 30 31 30 31 30 31 30 31 30 30 31 30 30 30' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 30 31 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 31 30 30 30 30 30 30 30 30 30' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 31 30 30 30 30 30 30 30 30' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 31 30 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 31 31 30 30 30 30 30 30 30 30' in text:
        return True
    if '30 31 30 30 31 31 30 31 30 31 30 31 31 30 31 30 31 31 31 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30' in text:
        return True


def basebin_find(text):
    if 'MDEwMDExMDEwMTAxMTAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw' in text:
        return True
    if 'MDEwMDExMDEwMTAxMTAxMDAxMDAwMDAxMDEwMTAwMTAwMTAxMDEwMTAxMDAxMDAw' in text:
        return True
    if 'MDEwMDExMDEwMTAxMTAxMDAxMDEwMDAwMDAwMDAwMDAwMDAwMDAxMDAwMDAwMDAw' in text:
        return True
    if 'MDEwMDExMDEwMTAxMTAxMDEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTAwMDAwMDAw' in text:
        return True
    if 'MDEwMDExMDEwMTAxMTAxMDEwMDEwMDAwMDAwMDAwMDAwMDAwMDAxMTAwMDAwMDAw' in text:
        return True
    if 'MDEwMDExMDEwMTAxMTAxMDExMTAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAwMDAwIDAwMDAgMDAwMCAwMDAwIDAwMDAgMDAwMCAwMDAwIDAw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAwMTAwIDAwMDEgMDEwMSAwMDEwIDAxMDEgMDEwMSAwMTAwIDEw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAwMTAxIDAwMDAgMDAwMCAwMDAwIDAwMDAgMDAxMCAwMDAwIDAw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAxMDAwIDAwMDAgMDAwMCAwMDAwIDAwMDAgMDAwMSAwMDAwIDAw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAxMDAxIDAwMDAgMDAwMCAwMDAwIDAwMDAgMDAxMSAwMDAwIDAw' in text:
        return True
    if 'MDEwMCAxMTAxIDAxMDEgMTAxMCAxMTEwIDEwMDAgMDAwMCAwMDAwIDAwMDAgMDAwMCAwMDAwIDAw' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMD' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMDEgMDAgMDAgMDEgMDEgMDEgMDAgMTAgMDEgMDEgMDEgMDEgMDEgMDAgMTAgMD' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMDEgMDEgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMTAgMDAgMDAgMDAgMD' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMTAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDEgMDAgMDAgMDAgMD' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMTAgMDEgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMTEgMDAgMDAgMDAgMD' in text:
        return True
    if 'MDEgMDAgMTEgMDEgMDEgMDEgMTAgMTAgMTEgMTAgMTAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMD' in text:
        return True


def basegzip_find(text):
    if 'H4sIAAAAAAAEAO18' in text:
        return True
    if 'H4sIAAAAAAAEAO19' in text:
        return True
    if 'H4sIAAAAAAAEAOy9' in text:
        return True
    if 'H4sIAAAAAAAEAO29' in text:
        return True
    if 'H4sIAAAAAAAEAOS9' in text:
        return True
    if 'H4sIAAAAAAAEAOy8' in text:
        return True
    if 'H4sIAAAAAAAEAOx9' in text:
        return True
    if 'H4sIAAAAAAAEAO17' in text:
        return True
    if 'H4sIAAAAAAAEAMy9' in text:
        return True


def baserot_find(text):
    if 'GIdDNNZNNNNRNNNN' in text:
        return True
    if 'GIcDNNVNNNNRNN8N' in text:
        return True
    if 'GIbNNNNNNNNNNNNN' in text:
        return True
    if 'GIcOHyIVvrIVtrjt' in text:
        return True
    if 'GIdNNNRNNNNRNONN' in text:
        return True
    if 'GIebNNNNNSgFEIJW' in text:
        return True
    if 'GIdDNNZNONNNNNNN' in text:
        return True
    if 'GIcOHyIVvrIVtrjtNNNN' in text:
        return True


def base64_doc(text):
    # application/msword or application/vnd.ms-excel
    if '0M8R4KGxGuEAAAAAAAAAAAAAAAAAAAAA' in text:
        return True
    # application/vnd.openxmlformats-officedocument.*
    if 'UEsDBBQABgAIAAAAIQ' in text:
        return True
    if 'UEsDBBQACAAIAAAAAA' in text:
        return True
    # text/rtf
    if 'e1xydGYxXGFkZWZsYW5nMTAy' in text:
        return True
    if 'e1xydGYxXGFuc2lcYW5zaWNw' in text:
        return True
    if 'e1xydGYxB25zaQduc2ljcGcx' in text:
        return True
    if 'e1xydGYxDQogSGVyZSBhcmUg' in text:
        return True
    if 'e1xydGYxe1xvYmplY3Rcb2Jq' in text:
        return True
    if 'e1xydGZ7XG9iamVjdFxvYmpo' in text:
        return True


def gzencode_find(text):
    if 'eJy0' in text:
        return True
    if 'eJy8' in text:
        return True
    if 'eJyc' in text:
        return True
    if 'eJyM' in text:
        return True
    if 'eJys' in text:
        return True
    if 'eJyU' in text:
        return True
    if 'eJzc' in text:
        return True
    if 'eJzE' in text:
        return True
    if 'eJzk' in text:
        return True
    if 'eJzM' in text:
        return True
    if 'eJzs' in text:
        return True
    if 'eJzt' in text:
        return True
    if 'eJzU' in text:
        return True
    if 'cG93ZXJzaGVsbC' in text:
        return True
    if 'UG93ZXJTaGVsbC' in text:
        return True


def basethreetwelve_find(text):
    if '396 398 425 393 377 377 389 377 377 377 377 381 377 377 377 377' in text:
        return True
    if '396 398 424 393 377 377 385 377 377 377 377 381 377 377 368 377' in text:
        return True
    if '396 398 423 377 377 377 377 377 377 377 377 377 377 377 377 377' in text:
        return True
    if '396 398 424 378 397 420 398 385 417 413 398 385 415 413 431 415' in text:
        return True
    if '396 398 425 377 377 377 381 377 377 377 377 381 377 378 377 377' in text:
        return True
    if '396 398 426 423 377 377 377 377 377 382 428 395 394 398 399 386' in text:
        return True
    if '396 398 425 393 377 377 389 377 378 377 377 377 377 377 377 377' in text:
        return True
    if '396 398 424 378 397 420 398 385 417 413 398 385 415 413 431 415 377 377 377 377' in text:
        return True
    if '419 386 379 393 419 381 361 409 393 398 386 398 395 385 422 420 395 385 384 427 385 377 377 377 377' in text:
        return True


def save_file(text, type, key):
    print('%s: %s' % (type, key))
    outfile = pastes_dir + key + "." + type
    if not os.path.exists(outfile):
        file = open(outfile, 'w')
        file.write(text)
        file.close()
        return
    else:
        print("paste already exists: " + outfile)
        return


def save_raw(text, key):
    rawfile = originals_dir + key
    if not os.path.exists(rawfile):
        file = open(rawfile, 'w')
        file.write(text)
        file.close()
        return
    else:
        print("paste already exists: " + rawfile)
        return


params = {'limit': limit}
r = requests.get(url_pastebin_scraping, params)
response = r.json()

logfile = open(logfile, 'a+')
counter = 0
bytes = 0
for paste in response:
    title = paste["title"]
    type = paste["syntax"]
    expire = paste["expire"]
    user = paste["user"]
    key = paste["key"]
    date = paste["date"]
    size = int(paste["size"])
    if (size > 3000 and not os.path.exists(originals_dir + key)):
        counter += 1
        bytes += size
        url = paste["scrape_url"]
        r = requests.get(url)
        if exe_find(r.content):
            type = "exe"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if b64_find(r.content):
            type = "base64"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if hex_find(r.content):
            type = "hex"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if bin_find(r.content):
            type = "bin"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if hexbase_find(r.content):
            type = "hexbase"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if dec_find(r.content):
            type = "dec"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if posh_find(r.content):
            type = "posh"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if doublebase_find(r.content):
            type = "2xbase64"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if b64_find(r.content[::-1]):
            type = "base64"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if hex_find(r.content[::-1]):
            type = "hex"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if bin_find(r.content[::-1]):
            type = "bin"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if hexbase_find(r.content[::-1]):
            type = "hexbase"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if dec_find(r.content[::-1]):
            type = "dec"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if doublebase_find(r.content[::-1]):
            type = "2xbase64"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basegzip_find(r.content):
            type = "basegzip"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basegzip_find(r.content[::-1]):
            type = "basegzip"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break

# EXPERIMENTAL DETECTION BELOW THIS LINE

        if basethreetwelve_find(r.content):
            type = "basethreetwelve"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basethreetwelve_find(r.content[::-1]):
            type = "basethreetwelve"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if base64_doc(r.content):
            type = "base64_doc"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if base64_doc(r.content[::-1]):
            type = "base64_doc"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if baserot_find(r.content):
            type = "baserot"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
        if baserot_find(r.content[::-1]):
            type = "baserot"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
        if hexbin_find(r.content):
            type = "hexbin"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if hexbin_find(r.content[::-1]):
            type = "hexbin"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basebin_find(r.content):
            type = "basebin"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basebin_find(r.content[::-1]):
            type = "basebin"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basehex_find(r.content):
            type = "basehex"
            save_file(r.content, type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break
        if basehex_find(r.content[::-1]):
            type = "basehex"
            save_file(r.content[::-1], type, key)
            save_raw(r.content, key)
            logfile.write('%s,%s,%s,%s,%s,%s\n' % (type, key, title, user, date, expire))
            break

end = time.time()
print("documents read: " + str(counter))
print("bytes read: " + str(bytes))
print("run time: " + str(end - start))
