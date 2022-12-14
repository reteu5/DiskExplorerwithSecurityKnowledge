# -*- coding:utf-8 -*-
# Author: Kei Choi(hanul93@gmail.com)


import os
import re
import ctypes
import struct
import kernel
import kavutil
import cryptolib

BYTE = ctypes.c_ubyte
WORD = ctypes.c_ushort
DWORD = ctypes.c_uint
FLOAT = ctypes.c_float
LPBYTE = ctypes.POINTER(ctypes.c_ubyte)
LPTSTR = ctypes.POINTER(ctypes.c_char)
HANDLE = ctypes.c_void_p
PVOID = ctypes.c_void_p
LPVOID = ctypes.c_void_p
UINT_PTR = ctypes.c_uint
SIZE_T = ctypes.c_uint


class DOS_HEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('e_magic', WORD),
        ('e_cblp', WORD),
        ('e_cp', WORD),
        ('e_crlc', WORD),
        ('e_cparhdr', WORD),
        ('e_minalloc', WORD),
        ('e_maxalloc', WORD),
        ('e_ss', WORD),
        ('e_sp', WORD),
        ('e_csum', WORD),
        ('e_ip', WORD),
        ('e_cs', WORD),
        ('e_lfarlc', WORD),
        ('e_ovno', WORD),
        ('e_res', BYTE * 8),  # 8Byte
        ('e_oemid', WORD),
        ('e_oeminfo', WORD),
        ('e_res2', BYTE * 20),  # 20Byte
        ('e_lfanew', DWORD),
    ]


class FILE_HEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Machine', WORD),
        ('NumberOfSections', WORD),
        ('CreationYear', DWORD),
        ('PointerToSymbolTable', DWORD),
        ('NumberOfSymbols', DWORD),
        ('SizeOfOptionalHeader', WORD),
        ('Characteristics', WORD),
    ]


class OPTIONAL_HEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Magic', WORD),
        ('MajorLinkerVersion', BYTE),
        ('MinorLinkerVersion', BYTE),
        ('SizeOfCode', DWORD),
        ('SizeOfInitializedData', DWORD),
        ('SizeOfUninitializedData', DWORD),
        ('AddressOfEntryPoint', DWORD),
        ('BaseOfCode', DWORD),
        ('BaseOfData', DWORD),
        ('ImageBase', DWORD),
        ('SectionAlignment', DWORD),
        ('FileAlignment', DWORD),
        ('MajorOperatingSystemVersion', WORD),
        ('MinorOperatingSystemVersion', WORD),
        ('MajorImageVersion', WORD),
        ('MinorImageVersion', WORD),
        ('MajorSubsystemVersion', WORD),
        ('MinorSubsystemVersion', WORD),
        ('Reserved1', DWORD),
        ('SizeOfImage', DWORD),
        ('SizeOfHeaders', DWORD),
        ('CheckSum', DWORD),
        ('Subsystem', WORD),
        ('DllCharacteristics', WORD),
        ('SizeOfStackReserve', DWORD),
        ('SizeOfStackCommit', DWORD),
        ('SizeOfHeapReserve', DWORD),
        ('SizeOfHeapCommit', DWORD),
        ('LoaderFlags', DWORD),
        ('NumberOfRvaAndSizes', DWORD),
    ]


class DATA_DIRECTORY(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('VirtualAddress', DWORD),
        ('Size', DWORD),
    ]


class SECTION_HEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Name', BYTE * 8),
        ('Misc_VirtualSize', DWORD),
        ('VirtualAddress', DWORD),
        ('SizeOfRawData', DWORD),
        ('PointerToRawData', DWORD),
        ('PointerToRelocations', DWORD),
        ('PointerToLinenumbers', DWORD),
        ('NumberOfRelocations', WORD),
        ('NumberOfLinenumbers', WORD),
        ('Characteristics', DWORD),
    ]


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

image_directory_entry = enum('EXPORT', 'IMPORT', 'RESOURCE', 'EXCEPTION', 'SECURITY',
                             'BASERELOC', 'DEBUG',
                             'COPYRIGHT',  # Architecture on non-x86 platforms
                             'GLOBALPTR', 'TLS', 'LOAD_CONFIG', 'BOUND_IMPORT',
                             'IAT', 'DELAY_IMPORT', 'COM_DESCRIPTOR', 'RESERVED')


p_str = re.compile(rb'[^\x00]*')  # NULL ?????? ???????????? ??????


class PE:
    def __init__(self, mm, verbose, filename):
        self.filename = filename
        self.filesize = os.path.getsize(filename)
        self.verbose = verbose
        self.mm = mm
        self.sections = []  # ?????? ?????? ?????? ?????? ?????????
        self.data_directories = []  # ?????? ????????? ???????????? ????????? ?????? ?????????
        self.pe_file_align = 0

    # -------------------------------------------------------------------------
    # pe_parse(mm)
    # PE ????????? ???????????? ?????? ????????? ????????????.
    # ????????? : mm - ?????? ??????
    # ????????? : {PE ?????? ?????? ??????} or None
    # -------------------------------------------------------------------------
    def parse(self):
        mm = self.mm

        pe_format = {'PE_Position': 0, 'EntryPoint': 0, 'SectionNumber': 0,
                     'Sections': None, 'EntryPointRaw': 0, 'FileAlignment': 0}

        try:
            if mm[0:2] != 'MZ':  # MZ??? ?????????????
                raise ValueError

            dos_header = DOS_HEADER()
            ctypes.memmove(ctypes.addressof(dos_header), mm[0:], ctypes.sizeof(dos_header))

            # PE ????????? ?????? ????????????
            pe_pos = dos_header.e_lfanew

            # PE ???????
            if mm[pe_pos:pe_pos + 4] != 'PE\x00\x00':
                raise ValueError

            pe_format['PE_Position'] = pe_pos

            # File Header ??????
            file_header = FILE_HEADER()
            file_header_size = ctypes.sizeof(file_header)  # file_header_size : 0x14
            ctypes.memmove(ctypes.addressof(file_header), mm[pe_pos + 4:], file_header_size)

            # Optional Header ??????
            optional_header = OPTIONAL_HEADER()
            optional_header_size = ctypes.sizeof(optional_header)
            ctypes.memmove(ctypes.addressof(optional_header), mm[pe_pos + 4 + file_header_size:], optional_header_size)

            # Optional Header??? Magic ID?
            if optional_header.Magic != 0x10b:
                raise ValueError

            # Entry Point ?????????
            pe_ep = optional_header.AddressOfEntryPoint
            pe_format['EntryPoint'] = pe_ep

            # Image Base ?????????
            pe_img = optional_header.ImageBase
            pe_format['ImageBase'] = pe_img

            # File Alignment ?????????
            self.pe_file_align = optional_header.FileAlignment
            pe_format['FileAlignment'] = self.pe_file_align

            # Section ?????? ?????????
            section_num = file_header.NumberOfSections
            pe_format['SectionNumber'] = section_num

            # Optional Header ?????? ?????????
            opthdr_size = file_header.SizeOfOptionalHeader
            pe_format['OptionalHederSize'] = opthdr_size

            # Data Directory ??????
            data_directory_size = ctypes.sizeof(DATA_DIRECTORY())  # data_directory_size : 8
            num_data_directory = (opthdr_size - optional_header_size) / data_directory_size
            off_data_directory = pe_pos + 4 + file_header_size + optional_header_size

            for i in range(num_data_directory):
                dx = DATA_DIRECTORY()
                ctypes.memmove(ctypes.addressof(dx),
                               mm[off_data_directory + (i * data_directory_size):],
                               data_directory_size)

                self.data_directories.append(dx)

            # ?????? ?????? ??????
            section_pos = pe_pos + 4 + file_header_size + opthdr_size

            # ?????? ?????? ?????? ??????
            for i in range(section_num):
                section = {}

                section_header = SECTION_HEADER()
                section_header_size = ctypes.sizeof(section_header)  # section_header_size : 0x28

                s = section_pos + (section_header_size * i)
                ctypes.memmove(ctypes.addressof(section_header), mm[s:], section_header_size)

                sec_name = ctypes.cast(section_header.Name, ctypes.c_char_p)
                section['Name'] = sec_name.value.replace('\x00', '')
                section['VirtualSize'] = section_header.Misc_VirtualSize
                section['RVA'] = section_header.VirtualAddress
                section['SizeRawData'] = section_header.SizeOfRawData
                section['PointerRawData'] = section_header.PointerToRawData
                section['Characteristics'] = section_header.Characteristics

                self.sections.append(section)

            pe_format['Sections'] = self.sections

            # EntryPoint??? ??????????????? ?????? ?????????
            ep_raw, sec_idx = self.rva_to_off(pe_ep)
            pe_format['EntryPointRaw'] = ep_raw  # EP??? Raw ??????
            pe_format['EntryPoint_in_Section'] = sec_idx  # EP??? ????????? ??????

            # ????????? ??????
            try:
                rsrc_rva = self.data_directories[image_directory_entry.RESOURCE].VirtualAddress  # ????????? ??????(RVA)
                rsrc_size = self.data_directories[image_directory_entry.RESOURCE].Size  # ????????? ??????
            except IndexError:
                rsrc_rva = 0
                rsrc_size = 0

            if rsrc_rva:  # ???????????? ?????????????
                try:
                    rsrc_off, rsrc_idx = self.rva_to_off(rsrc_rva)  # ????????? ?????? ??????

                    if rsrc_off > self.filesize:
                        raise ValueError

                    t_size = self.sections[rsrc_idx]['SizeRawData']
                    if not (len(mm[rsrc_off:rsrc_off + rsrc_size]) == rsrc_size or \
                        len(mm[rsrc_off:rsrc_off + t_size]) == t_size):  # ????????? ???????????? ???????????? ??????
                        raise ValueError

                    # Type ??????
                    num_type_name = kavutil.get_uint16(mm, rsrc_off+0xC)
                    num_type_id = kavutil.get_uint16(mm, rsrc_off + 0xE)

                    for i in range(num_type_name + num_type_id):
                        type_id = kavutil.get_uint32(mm, rsrc_off + 0x10 + (i*8))
                        name_id_off = kavutil.get_uint32(mm, rsrc_off + 0x14 + (i * 8))

                        # Type??? ???????????? ????????? ?????? or RCDATA?
                        if type_id & 0x80000000 == 0x80000000 or type_id == 0xA or type_id == 0:
                            if type_id & 0x80000000 == 0x80000000:
                                # ???????????? ????????? ?????? ??????
                                string_off = (type_id & 0x7FFFFFFF) + rsrc_off
                                len_name = kavutil.get_uint16(mm, string_off)
                                rsrc_type_name = mm[string_off + 2:string_off + 2 + (len_name * 2):2]
                            elif type_id == 0xA:
                                rsrc_type_name = 'RCDATA'
                            else:
                                rsrc_type_name = '%d' % type_id

                            # Name ID
                            name_id_off = (name_id_off & 0x7FFFFFFF) + rsrc_off
                            if name_id_off > self.filesize:
                                raise ValueError

                            num_name_id_name = kavutil.get_uint16(mm, name_id_off + 0xC)
                            num_name_id_id = kavutil.get_uint16(mm, name_id_off + 0xE)

                            for j in range(num_name_id_name + num_name_id_id):
                                name_id_id = kavutil.get_uint32(mm, name_id_off + 0x10 + (j * 8))
                                language_off = kavutil.get_uint32(mm, name_id_off + 0x14 + (j * 8))

                                # ????????? ????????? ?????? ?????? ??????
                                if name_id_id & 0x80000000 == 0x80000000:
                                    string_off = (name_id_id & 0x7FFFFFFF) + rsrc_off
                                    if string_off > self.filesize:
                                        raise ValueError

                                    len_name = kavutil.get_uint16(mm, string_off)
                                    rsrc_name_id_name = mm[string_off + 2:string_off + 2 + (len_name * 2):2]
                                    string_name = rsrc_type_name + '/' + rsrc_name_id_name
                                else:
                                    string_name = rsrc_type_name + '/' + hex(name_id_id).upper()[2:]

                                # Language
                                language_off = (language_off & 0x7FFFFFFF) + rsrc_off
                                if language_off > self.filesize:
                                    raise ValueError

                                num_language_name = kavutil.get_uint16(mm, language_off + 0xC)
                                num_language_id = kavutil.get_uint16(mm, language_off + 0xE)

                                for k in range(num_language_name + num_language_id):
                                    # language_id = kavutil.get_uint32(mm, language_off + 0x10 + (k * 8))
                                    data_entry_off = kavutil.get_uint32(mm, language_off + 0x14 + (k * 8))

                                    data_entry_off = (data_entry_off & 0x7FFFFFFF) + rsrc_off

                                    data_rva = kavutil.get_uint32(mm, data_entry_off)
                                    data_off, _ = self.rva_to_off(data_rva)
                                    if data_off > self.filesize:
                                        continue

                                    data_size = kavutil.get_uint32(mm, data_entry_off + 4)
                                    if data_size > self.filesize:
                                        continue

                                    if data_size > 8192:  # ?????? 8K ????????? ???????????? ???????????? ??????
                                        if 'Resource_UserData' in pe_format:
                                            pe_format['Resource_UserData'][string_name] = (data_off, data_size)
                                        else:
                                            pe_format['Resource_UserData'] = {string_name: (data_off, data_size)}
                except (struct.error, ValueError) as e:
                    pass

                # if 'Resource_UserData' in pe_format:
                #     print (pe_format['Resource_UserData'])

            # Import API ??????
            try:
                imp_rva = self.data_directories[image_directory_entry.IMPORT].VirtualAddress  # Import API ??????(RVA)
                imp_size = self.data_directories[image_directory_entry.IMPORT].Size  # Import API ??????
            except IndexError:
                imp_rva = 0
                imp_size = 0

            if imp_rva:  # Import API ??????
                imp_api = {}

                # print ('IMP : %08X' % imp_rva)
                imp_off = self.rva_to_off(imp_rva)[0]
                # print (hex(imp_off), imp_size)
                imp_data = mm[imp_off:imp_off+imp_size]
                if len(imp_data) == imp_size:
                    for i in range(imp_size / 0x14):  # DLL ?????? ????????? 0x14
                        try:
                            dll_rva = kavutil.get_uint32(imp_data, (i*0x14)+0xC)
                            api_rva = kavutil.get_uint32(imp_data, (i * 0x14))
                            bo = 2
                            if api_rva == 0:
                                api_rva = kavutil.get_uint32(imp_data, (i*0x14)+0x10)
                                bo = 0

                            # print (hex(api_rva))
                            if dll_rva == 0:  # DLL ????????? ??????
                                break

                            t_off = self.rva_to_off(dll_rva)[0]
                            dll_name = p_str.search(mm[t_off:t_off+0x20]).group()
                            # print ('[+]', dll_name)
                            imp_api[dll_name] = []

                            t_off = self.rva_to_off(api_rva)[0]
                            while True:
                                try:
                                    api_name_rva = kavutil.get_uint32(mm, t_off)
                                except struct.error:
                                    break

                                if api_name_rva & 0x80000000 == 0x80000000:  # Odinal API
                                        t_off += 4
                                        continue

                                if api_name_rva == 0:
                                    break

                                t = self.rva_to_off(api_name_rva)[0]
                                # print (hex(t_off), hex(t))
                                api_name = p_str.search(mm[t+bo:t+bo+0x20]).group()
                                # print ('   ', api_name)
                                imp_api[dll_name].append(api_name)
                                t_off += 4
                        except struct.error:
                            pass
                # end if

                pe_format['Import_API'] = imp_api

            # ????????? ????????? ??????
            try:
                cert_off = self.data_directories[image_directory_entry.SECURITY].VirtualAddress  # ???????????? RVA??? ?????? ?????????
                cert_size = self.data_directories[image_directory_entry.SECURITY].Size  # ????????? ????????? ??????
            except IndexError:
                cert_off = 0
                cert_size = 0

            if cert_off:  # ????????? ????????? ??????
                if cert_off + cert_size <= len(mm[:]):  # UPack??? ?????? ????????? ?????? ?????? ???
                    pe_format['CERTIFICATE_Offset'] = cert_off
                    pe_format['CERTIFICATE_Size'] = cert_size

            # Debug ?????? ??????
            try:
                debug_rva = self.data_directories[image_directory_entry.DEBUG].VirtualAddress  # RVA
                debug_size = self.data_directories[image_directory_entry.DEBUG].Size  # ??????
                if debug_size < 0x1C:
                    raise ValueError
            except (IndexError, ValueError) as e:
                debug_rva = 0
                debug_size = 0

            if debug_rva:  # Debug ?????? ??????
                t = self.rva_to_off(debug_rva)[0]
                debug_off = kavutil.get_uint32(mm, t + 0x18)
                debug_size = kavutil.get_uint32(mm, t + 0x10)

                debug_data = mm[debug_off:debug_off + debug_size]

                if debug_data[:4] == 'RSDS':
                    pe_format['PDB_Name'] = debug_data[0x18:]
                else:
                    pe_format['PDB_Name'] = 'Not support Type : %s' % debug_data[:4]

            if self.verbose:
                print ('-' * 79)
                kavutil.vprint('Engine')
                kavutil.vprint(None, 'Engine', 'pe.kmd')
                kavutil.vprint(None, 'File name', os.path.split(self.filename)[-1])
                kavutil.vprint(None, 'MD5', cryptolib.md5(mm[:]))

                print ()
                kavutil.vprint('PE')
                kavutil.vprint(None, 'EntryPoint', '%08X' % pe_format['EntryPoint'])
                kavutil.vprint(None, 'EntryPoint (Section)', '%d' % pe_format['EntryPoint_in_Section'])

                # ?????? ??????
                if section_num:
                    print ()
                    kavutil.vprint('Section Header')
                    print ('    %-8s %-8s %-8s %-8s %-8s %-8s' % ('Name', 'VOFF', 'VSIZE', 'FOFF', 'FSIZE', 'EXEC'))
                    print ('    ' + ('-' * (9*6 - 1)))

                    for s in self.sections:
                        print ('    %-8s %08X %08X %08X %08X %-05s' % (s['Name'], s['RVA'], s['VirtualSize'],
                                                                     s['PointerRawData'], s['SizeRawData'],
                                                                     s['Characteristics'] & 0x20000000 == 0x20000000))

                if section_num:
                    print ()
                    kavutil.vprint('Section MD5')
                    print ('    %-8s %-8s %-32s' % ('Name', 'FSIZE', 'MD5'))
                    print ('    ' + ('-' * ((9 * 2 - 1)+32)))

                    for s in self.sections:
                        # if s['Characteristics'] & 0x20000000 == 0x20000000:
                        off = s['PointerRawData']
                        size = s['SizeRawData']
                        fmd5 = cryptolib.md5(mm[off:off+size]) if size else '-'
                        print ('    %-8s %8d %s' % (s['Name'], size, fmd5))

                print ()
                kavutil.vprint('Entry Point (Raw)')
                print ()
                kavutil.HexDump().Buffer(mm[:], pe_format['EntryPointRaw'], 0x80)
                print ()
                if 'PDB_Name' in pe_format:
                    kavutil.vprint('PDB Information')
                    kavutil.vprint(None, 'Name', '%s' % repr(pe_format['PDB_Name']))
                    print (repr(pe_format['PDB_Name']))
                    print ()

        except (ValueError, struct.error) as e:
            return None

        return pe_format

    def rva_to_off(self, t_rva):
        for section in self.sections:
            size = section['SizeRawData']
            rva = section['RVA']

            if rva <= t_rva < rva + size:
                if self.pe_file_align:
                    foff = (section['PointerRawData'] / self.pe_file_align) * self.pe_file_align
                else:
                    foff = section['PointerRawData']
                t_off = t_rva - rva + foff

                return t_off, self.sections.index(section)

        return t_rva, -1  # ?????? ???????????? ???????????? ????????????.. ?????? RVA ??????


# -------------------------------------------------------------------------
# KavMain ?????????
# -------------------------------------------------------------------------
class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # ???????????? ????????? ????????? ??????.
    # ????????? : plugins_path - ???????????? ????????? ??????
    #         verbose      - ????????? ?????? (True or False)
    # ????????? : 0 - ??????, 0 ????????? ??? - ??????
    # ---------------------------------------------------------------------
    def init(self, plugins_path, verbose=False):  # ???????????? ?????? ?????????
        self.verbose = verbose

        # NSIS ?????? ??????
        '''
        81 7D DC EF BE AD DE                          cmp     [ebp+var_24], 0DEADBEEFh
        75 69                                         jnz     short loc_402D79
        81 7D E8 49 6E 73 74                          cmp     [ebp+var_18], 'tsnI'
        75 60                                         jnz     short loc_402D79
        81 7D E4 73 6F 66 74                          cmp     [ebp+var_1C], 'tfos'
        75 57                                         jnz     short loc_402D79
        81 7D E0 4E 75 6C 6C                          cmp     [ebp+var_20], 'lluN'
        '''

        self.p_nsis = '817DDCEFBEADDE7569817DE8496E7374'.decode('hex')

        return 0  # ???????????? ?????? ????????? ??????

    # ---------------------------------------------------------------------
    # uninit(self)
    # ???????????? ????????? ????????????.
    # ????????? : 0 - ??????, 0 ????????? ??? - ??????
    # ---------------------------------------------------------------------
    def uninit(self):  # ???????????? ?????? ??????
        return 0  # ???????????? ?????? ?????? ??????

    # ---------------------------------------------------------------------
    # getinfo(self)
    # ???????????? ????????? ?????? ????????? ????????????. (?????????, ??????, ...)
    # ????????? : ???????????? ?????? ??????
    # ---------------------------------------------------------------------
    def getinfo(self):  # ???????????? ????????? ?????? ??????
        info = dict()  # ????????? ?????? ??????

        info['author'] = 'Kei Choi'  # ?????????
        info['version'] = '1.2'  # ??????
        info['title'] = 'PE Engine'  # ?????? ??????
        info['kmd_name'] = 'pe'  # ?????? ?????? ??????

        # ????????? ????????? ??????????????? ???????????? ????????? ????????? ????????? ????????????.
        info['make_arc_type'] = kernel.MASTER_DELETE  # ???????????? ?????? ??? ????????? ??????
        return info

    # ---------------------------------------------------------------------
    # format(self, filehandle, filename, filename_ex)
    # ?????? ????????? ????????????.
    # ????????? : filehandle - ?????? ??????
    #          filename   - ?????? ??????
    #          filename_ex - ?????? ?????? ?????? ?????? ??????
    # ????????? : {?????? ?????? ?????? ??????} or None
    # ---------------------------------------------------------------------
    def format(self, filehandle, filename, filename_ex):
        fileformat = {}  # ?????? ????????? ?????? ??????
        ret = {}

        pe = PE(filehandle, self.verbose, filename)
        try:
            pe_format = pe.parse()  # PE ?????? ??????
        except MemoryError:
            pe_format = None

        if pe_format is None:
            return None

        fileformat['pe'] = pe_format
        ret = {'ff_pe': fileformat}

        # PE ?????? ????????? ?????? ????????? ????????? ????????????.
        pe_size = 0

        pe_file_align = pe_format['FileAlignment']

        for sec in pe_format['Sections']:
            if pe_file_align:
                off = (sec['PointerRawData'] / pe_file_align) * pe_file_align
            else:
                off = sec['PointerRawData']
            size = sec['SizeRawData']
            if pe_size < off + size:
                pe_size = off + size

        file_size = len(filehandle)

        if 'CERTIFICATE_Offset' in pe_format:  # ?????? ?????? ???????????? ????????????????
            if pe_format['CERTIFICATE_Offset'] == pe_size:  # PE ????????? ????????? ???????????? ????????? ????????? ???????????? ?????? ??????
                t_pe_size = pe_format['CERTIFICATE_Offset'] + pe_format['CERTIFICATE_Size']
                if pe_size < t_pe_size:
                    pe_size = t_pe_size
                attach_size = file_size - pe_size
            else:
                attach_size = file_size - pe_size - pe_format['CERTIFICATE_Size']
        else:
            attach_size = file_size - pe_size

        if pe_size < file_size and pe_size != 0:
            mm = filehandle

            # NSIS ????????? .text ????????? ??????????????? ????????????.
            text_sec = pe_format['Sections'][0]
            if pe_file_align:
                off = (text_sec['PointerRawData'] / pe_file_align) * pe_file_align
            else:
                off = text_sec['PointerRawData']
            size = text_sec['SizeRawData']

            if size:
                if mm[off:off + size].find(self.p_nsis) != -1:
                    # PE ????????? ????????? ???????????? ????????? NSIS ???????????? ????????????
                    i = 1
                    while True:
                        t = mm[i * 0x200 + 4:i * 0x200 + 20]
                        if len(t) != 16:
                            break

                        if t == '\xEF\xBE\xAD\xDENullsoftInst':
                            ret['ff_nsis'] = {'Offset': i * 0x200}
                            break

                        i += 1

            # Attach ???????????? (??? NSIS??? ???????????? ???????????? ??????)
            if not('ff_nsis' in ret):
                fileformat = {  # ?????? ????????? ?????? ??????
                    'Attached_Pos': pe_size,
                    'Attached_Size': attach_size
                }
                ret['ff_attach'] = fileformat

        return ret

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # ?????? ?????? ????????? ?????? ????????? ?????????.
    # ????????? : filename   - ?????? ??????
    #          fileformat - ?????? ?????? ?????? ??????
    # ????????? : [[?????? ?????? ID, ????????? ?????? ??????]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = []  # ?????? ?????? ????????? ?????? ??????

        # ?????? ????????? ?????? ???????????? ?????? ?????? ????????? ??????????
        if 'ff_pe' in fileformat:
            if 'Resource_UserData' in fileformat['ff_pe']['pe']:
                for key in fileformat['ff_pe']['pe']['Resource_UserData'].keys():
                    off, size = fileformat['ff_pe']['pe']['Resource_UserData'][key]
                    file_scan_list.append(['arc_pe_rcdata:%d:%d' % (off, size), key])

        return file_scan_list

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # ????????? : arc_engine_id - ?????? ?????? ID
    #          arc_name      - ?????? ??????
    #          fname_in_arc   - ?????? ????????? ?????? ??????
    # ????????? : ?????? ????????? ?????? or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id.find('arc_pe_rcdata:') != -1:
            t = arc_engine_id.split(':')
            off = int(t[1])
            size = int(t[2])

            try:
                with open(arc_name, 'rb') as fp:
                    fp.seek(off)
                    data = fp.read(size)
            except IOError:
                return None

            return data

        return None

    # ---------------------------------------------------------------------
    # arcclose(self)
    # ?????? ?????? ????????? ?????????.
    # ---------------------------------------------------------------------
    def arcclose(self):
        pass

    # ---------------------------------------------------------------------
    # feature(self, filehandle, filename, fileformat, malware_id)
    # ????????? Feature??? ????????????.
    # ????????? : filehandle  - ?????? ??????
    #         filename    - ?????? ??????
    #         fileformat  - ?????? ??????
    #         filename_ex - ?????? ?????? (?????? ?????? ?????? ??????)
    #         malware_id  - ???????????? ID
    # ????????? : Feature ?????? ?????? ??????
    # ---------------------------------------------------------------------
    def feature(self, filehandle, filename, fileformat, filename_ex, malware_id):  # Feature ??????
        try:
            mm = filehandle

            # ?????? ????????? ?????? ???????????? PE ????????? ??????????
            if 'ff_pe' in fileformat:
                buf = mm[:]
                fmd5 = cryptolib.md5(buf).decode('hex')  # ?????? ?????? MD5 ??????
                header = 'PE\x00\x00' + struct.pack('<L', malware_id) + fmd5

                pe = PE(mm, False, filename)
                pe_format = pe.parse()
                if not pe_format:
                    return None

                pe_off = pe_format['PE_Position']  # pe.DOS_HEADER.e_lfanew
                ep = pe_format['EntryPoint']  # pe.OPTIONAL_HEADER.AddressOfEntryPoint

                text_off = 0
                text_size = 0

                for sec in pe_format['Sections']:  # pe.sections:
                    rva = sec['RVA']  # sec.VirtualAddress
                    vsize = sec['VirtualSize']  # sec.Misc_VirtualSize
                    if rva <= ep <= rva + vsize:
                        text_off = sec['PointerRawData']  # sec.PointerToRawData
                        text_size = sec['SizeRawData']  # sec.SizeOfRawData
                        break

                # Feature ??????
                f = kavutil.Feature()

                data = ''
                # 1. text ????????? ????????? ??????????????? ????????????.
                data += f.entropy(mm[text_off:text_off + text_size])

                # 2. PE ?????? ????????? ????????????.
                data += mm[pe_off + 6:pe_off + 6 + 256]

                # 3. DATA ?????? 2-gram ????????????
                data_off = 0
                data_size = 0

                for sec in pe_format['Sections']:  # pe.sections:
                    if sec['Characteristics'] & 0x40000040 == 0x40000040:  # if DATA and Read
                        data_off = sec['PointerRawData']  # sec.PointerToRawData
                        data_size = sec['SizeRawData']  # sec.SizeOfRawData
                        break

                data += f.k_gram(mm[data_off:data_off + data_size], 2)

                # 4. Import API ?????? ????????????
                def import_api(l_pe_format):
                    api_hash = set()

                    l_data = ''

                    if 'Import_API' in l_pe_format:
                        imp_api = pe_format['Import_API']
                        # print (imp_api)

                        for dll in imp_api.keys():
                            for api in dll:
                                api_name = ('%s:%s' % (dll, api)).lower()
                                api_hash.add(struct.pack('<H', cryptolib.CRC16().calculate(api_name)))

                        t = list(api_hash)
                        l_data = ''.join(t)

                    if len(l_data) < 256:
                        l_data += '\x00' * (256 - len(l_data))

                    return l_data[:256]

                data += import_api(pe_format)

                open('pe.bin', 'ab').write(header + data)  # Feature ?????? ??????

                return True
        except IOError:
            pass

        # Feature ?????? ??????????????? ????????????.
        return False
