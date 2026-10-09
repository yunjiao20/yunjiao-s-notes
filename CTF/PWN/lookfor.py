#!/bin/sh


'''
lookfor.py

快速功能查询：
    --file [file_name]  > 强制认为后面一个参数是文件，无论此文件名的开头是不是'-'

    --auto              > 认为传入的文件是待pwn的文件而非你已处理的包含gadgets的
                        文本文件，由lookfor.py自动调用ROPgadget在本目录下创建文
                        件gadgets_from_[file_name].txt，然后在此文件中寻找信息。
                        这个被创建的文件gadgets_from_[file_name].txt默认保存
    --nokeep            > 不保留--auto生成的文件gadgets_from_[file_name].txt，将
                        在处理完后删除
    -i                  > 忽略大小写，所有大写字符都会被处理成小写字符，处理输出
                        全小写句子

    --help  -h          > 查看此文档
    --version  -v       > 输出lookfor.py的版本信息（其实是我编写此脚本的日期）
    --my-msg            > 输出一些我保留的信息，如syscall的样板代码，可以通过修
                        改函数print_something_msg()来更改它

用于在ROPgadget中获取特定字符串的行的python脚本，用于快速批量获取特定gadget，
用于处理grep查找的字符串中不能有换行而返回过多结果的情况。此脚本允许传入多个
文件顺序处理

使用：
打开此脚本修改列表gadgetIneed，将自己需要查找的字符串加入此列表中。你可以在字
符串末尾加上\\n以表明此字符串应该在此行的末尾，否则此脚本的功能将与grep一样
如 gadgetIneed = [
      ': pop rax ; ret\\n',
      ': pop rdi ; ret',
]
gadgetIneed的元素只能是非空字符串
保存

你可以手动使用ROPgadget创建包含gadgets的文件，交由lookfor.py处理
    ROPgadget --binary pwnfile > gadgets.txt
    python3 lookfor.py gadgets.txt
处理多个文件：
    python3 lookfor.py gadgets.txt ropmsg1 ropmsg2

使用ROPgadget创建包含gadgets的文件可能需要不少时间，特别是处理如libc这样的文
件时，你可能会在手动创建gadgets文件时花费较多时间，然后还要交给lookfor.py。
所以lookfor.py提供了参数--auto以自动化这个流程，--auto会将你给的文件看作需要
pwn的文件而非你以处理好的gadgets文本文件，调用ROPgadget自动创建文件并处理它
    python3 lookfor.py --auto pwnfile
    python3 lookfor.py --auto /usr/lib/x86_64-linux-gnu/libc.so.6

--auto创建的文件名为gadgets_from_[file_name].txt，file_name是你提供的文件名，
文件中的路径符'/'将被处理成'---'以便于放在当前目录。此文件默认保存，以免于你
需要更高级的手动查询时重复创建gadgets文件。如果你不希望保存--auto创建的gadgets
文件，你可以使用--nokeep以使lookfor.py在处理完后自动删除它
    python3 lookfor.py --auto --nokeep pwnfile

-i使lookfor.py忽略文件中数据和需要查询的gadgets的大小写，统一转成小写，然后处
理。输出的也为纯小写
    python3 lookfor.py gadgets.txt -i
    python3 lookfor.py --auto -i pwnfile

所有第一个字符为'-'的都被lookfor.py视作参数，如果你的文件名的第一位带'-'，会导
致文件无法被处理。你可以在此带-的文件前带上参数--file，它会强制下一个参数为文件
名，无论此文件名前面是否有'-'
    python3 lookfor.py --file -some-gadgets.txt

--version -v输出版本
    python3 lookfor.py --version

--help -h使用help()展示此帮助信息
    python3 lookfor.py --help

--my-msg输出我保留可能经常需要的信息，请提供修改函数print_something_msg()来修改
并保持它
    python3 lookfor.py --my-msg
'''
from os  import system, remove
from sys import argv, exit, stderr



gadgetsIneed = [
    ': pop rax ; ret\n',
    ': pop rdi ; ret\n',
    ': pop rsi ; ret\n',
    ': pop rdx ; pop rbx ; ret\n',
    ': syscall',

    ': leave ; ret',
    ': ret\n',
]



def main(argv: list  = argv,
         gadgetsIneed: list[str] = gadgetsIneed) -> int:
    '''lookfor.py的主函数，检查参数并调用各功能'''
    check_gadgetsIneed()

    files: tuple = ()
    argv : dir = argv_handler(argv)  # 识别处理参数，返回一个包含三个键的字典，类似于
                # {'files': ('file1', 'file2'),   '--auto': True,   '--nokeep': Flase}

    if argv['--version']:
        print('lookfor.py writed in 2026/3/29')

    if argv['--my-msg']:
        print_something_msg()

    if argv['--help']:
        from sys import modules
        help(modules[__name__])    # sys.modules[__name__]返回此文件的引用，以供help查看此文件文档字符串

    if argv['--auto']:
        # argv['--auto'] == True, 传入了参数 --auto
        # 认为用户传入的是需要pwn的文件，由lookfor.py自动创建包含gadgets的文件并处理
        print(f'gadgetsIneed: {gadgetsIneed}')
        files: tuple = gadgets_file_creativer(pwnfiles = argv['files'])  # 创建包含待pwn文件gadgets的文件
        for file in files:                               # 返回一个元组，包含创建文件的文件名，以便查找处理
            lookfor_in_file_and_print(file, gadgetsIneed, ignore_uppercase=argv['-i'])  # 参数-i决定是否忽略
                                                                                        # 大小写
    else :
        # argv['--auto'] == False, 没有传入参数 --auto
        # 认为传入的文件是用户制作好的包含gadgets的文件
        print(f'gadgetsIneed: {gadgetsIneed}')
        for file in argv['files']:
            lookfor_in_file_and_print(file, gadgetsIneed, ignore_uppercase=argv['-i'])

    if argv['--nokeep'] and files:
        # 传入了参数 --nokeep 且lookfor.py自动创建了gadgets文件，删除文件
        for file in files:
            try:    # 防止因没有此文件而崩溃
                remove(file)  # os.remove()删除文件
            except FileNotFoundError:
                stderr.write(f'\033[31m[lookfor.py Error]:\033[0m 删除文件{file}时出错')

def check_gadgetsIneed(gadgetsIneed: list[str] = gadgetsIneed) -> None:
    '''检查全局变量gadgetsIneed，确保用户的修改可以使用。如gadgetsIneed为不是列表、
    列表为空、列表中存在非字符串或空
    ---------------...（   -_-）...---------------
    程序退出代码（检查失败时）
    255     gadgetsIneed为空列表
    254     gadgetsIneed不是列表
    253     gadgetsIneed中存在非字符串
    252     gadgetsIneed中存在空字符串'' '''
    if not gadgetsIneed:
        # 列表为空，默认为空，为第一次使用的用户提供详细的信息
        stderr.write(
'''\033[31m!!!lookfor.py Error!!!
查询列表gadgetIneed为空，你应该打开lookfor.py添加非空字符串以供lookfor.py查询
请使用\033[32m python3 lookfor.py --help \033[31m以查看帮助信息\033[0m''')
        ask_to_open_help()
        exit(255)

    if not isinstance(gadgetsIneed, list):
        # gadgetsIneed不是列表
        stderr.write(
'''\033[31m!!!lookfor.py Error!!!
全局变量gadgetsIneed只能是包含非空字符串的列表，请打开lookfor.py将其改为列表\033[0m''')
        ask_to_open_help()
        exit(254)

    if not all([isinstance(gadget_str, str) for gadget_str in gadgetsIneed]):
        # gadgetsIneed中存在非字符串
        stderr.write(
'\033[31m!!!lookfor.py Error!!!\n全局变量gadgetsIneed中的元素只能是字符串\033[0m')
        ask_to_open_help()
        exit(253)

    if not all(gadgetsIneed):
        # gadgets中存在空字符 ''
        stderr.write(
'''\033[31m!!!lookfor.py Error!!!
全局变量gadgetsIneed中不能存在空字符\033[0m''')
        ask_to_open_help()
        exit(252)

def ask_to_open_help() -> None:
    '''询问用户是否需要打开lookfor的帮助信息，是调用help查看本文件的文档字符串'''
    ask = 'Want you watch help messge of lookfor.py[\'y\' to watch]?: '
    if input(ask) == 'y':
        from sys import modules
        help(modules[__name__])

def argv_handler(argv: list) -> dir:
    '''
    处理程序参数，返回一个字典，同时检查用户是否提供了文件名，没有提供文件名
    同时没有提供数据查看参数--version(-v)、--msg、--help(-h)，终止程序并提供
    信息(错误代码250)。此函数也兼职处理没有提供参数时的报错终止(错误代码251)
    --------------= o<  ^ ^>o =--------------
    返回字典格式：
    {
        'files' :    tuple[str],
        '--auto':    bool,
        '--nokeep':  bool,
        '-i'    :    bool,
        '--version': bool,
        '--help':    bool,
        '--my-msg':  bool,
    }

    ['files']的值为一个元组，包含参数中的文件名
    --auto、--nokeep、--version、--help、--msg、-i的值为bool，
        True表示传入参数中存在此参数，Flase为不存在此参数

    lookfor.py也存在--file参数，但其强制标识下一个为文件，以使首字符为'-'的
    文件名可以被强制识别。其识别的文件名将被加入['files']元组中，不被特殊
    处理，故没有在返回字典中提供
    '''
    if len(argv) == 1:    # 没有提供参数
        stderr.write(
'''\033[31m!!!lookfor.py Error!!!
你没有为lookfor.py提供可用参数，请使用\033[32m python3 lookfor.py --help \033[31m查看帮助信息\033[0m''')
        ask_to_open_help()
        exit(251)

    files: list = []
    _file :  bool  = False    # 标识上一位是否为参数--file

    _auto :  bool  = False    # 标识是否存在此参数
    _nokeep: bool  = False
    _i    :  bool  = False
    _help :  bool  = False
    _my_msg: bool  = False
    _version:bool  = False

    for a in argv[1:]:

        if _file:    # 上一个参数为--file，强制作为文件名加入files
            files.append(a)
            _file = False
        elif a == '--file':  # 参数为--file，设置_file=True对下一个触发_file逻辑
            _file = True

        elif a == '--auto':
            _auto = True
        elif a == '--nokeep':
            _nokeep = True
        elif a == '-i':
            _i = True
        elif a == '--help' or a == '-h':
            _help = True
        elif a == '--my-msg':
            _my_msg = True
        elif a == '--version' or a == '-v':
            _version = True

        elif a[0] == '-':
            stderr.write(f'\033[33m\033[1m[Warning]\033[21m: \'{a}\'不是有效参数\n')

        else :
            files.append(a)

    if not files and not (_help or _my_msg or _version):
    # 没提供文件 and 没有提供--help(-h)、--msg、--version(-v)参数
    # 即：存在有输出信息的参数时，不一定要处理文件，不必报错
        stderr.write(
'''\033[31m!!!lookfor.py Error!!!
你没有为lookfor.py提供可供处理的文件名，如果你的文件名因首位为'-'而被lookfor.py视作功能参数，请\
在文件名前添加参数'--file'\033[0m''')
        ask_to_open_help()
        exit(250)

    return     {
        'files' :    tuple(files),
        '--auto':    _auto,
        '--nokeep':  _nokeep,
        '-i'    :    _i,
        '--version': _version,
        '--help':    _help,
        '--my-msg':  _my_msg,
    }

def lookfor_in_file_and_print(file: str,    gadgetsIneed: list[str],
                              color: dir = {'start': '\033[31m\033[1m',
                                            'end'  : '\033[0m'},
                              ignore_uppercase: bool = False        ) -> None:
    '''逐行读取文件中的内容，对照是否有gadgetsIneed的字符串，有，则将此字符串
    在句子中标上颜色并输出
    参数：
        file: str  --待处理的文件名
        gadgetsIneed: list  --所需检查的gadgets的列表
        coler: dir  --标上的颜色的ANSI标识，应有两个key：'start', 'end'
                      默认为{'start': '\\033[31m\\0331m',  'end'  : '\\033[0m'}
                      start为颜色起始，默认为红色(31)加亮加粗(1)
        ignore_uppercase: bool  --是否忽略大小写，True则将gadget和句子都变成
                                  小写然后处理输出'''
    print(f'\n\033[35m{file}: \033[0m')

    line_num: int = 0
    try :
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                line = f.readline()

                if not line:  # 读取完毕
                    print(f'\033[32m[Tip]:\033[0m 共处理了\033[32m\033[1m{line_num}\033[0m行')
                    break

                for gadget_I_need in gadgetsIneed:  # 逐个gadget检查
                    if ignore_uppercase:  # 忽略大小写功能为True，行和gadget都变成小写
                        line = line.lower()       # 同样，此时输出也变成小写
                        gadget_I_need = gadget_I_need.lower()
                    if gadget_I_need in line:
                        print(line.replace(gadget_I_need,
                                           f'{color["start"]}{gadget_I_need}{color["end"]}'),
                              end = '')
                line_num += 1
    except FileNotFoundError:    # 文件未发现，提供的文件名不正确
        print(f'\033[31m\033[1m[FileNotFoundError]:\033[21m 文件\033[1m{file}\033[21m不存在\033[0m')

def gadgets_file_creativer(pwnfiles: tuple[str]) -> tuple[str]:
    '''在当前目录下调用ROPgadget --binary创建包含有gadgets信息的文件，并将所有
    制作出来的文件的文件名封装在一个元组中返回，以便交由lookfor_in_file_and_print
    寻找gadgets文件并处理'''
    keep_files_l: list = []
    for file in pwnfiles:
        keep_file = f'gadgets_from_{file}.txt'.replace('/', '---')
        system(f'ROPgadget --binary \'{file}\' > {keep_file}')
        keep_files_l.append(keep_file)

    return tuple(keep_files_l)

def print_something_msg() -> None:
    '''输出一些我保存的可能需要的信息（如pwn的一些利用样板代码），请通过修改这
    个函数来改变你所需要的信息'''
    print('''
   ###### syscall ######

pop_rax = libc_base + 0x0
pop_rdi = libc_base + 0x0
pop_rsi = libc_base + 0x0
pop_rdx = libc_base + 0x0
syscall = libc_base + 0x0
binsh   = libc_base + next(libc.search('/bin/sh'))
# search str'/bin/sh' addr in libc

payload = b'A' * 120     + \\
          p64(pop_rax)   + \\
          p64(59)        + \\
          p64(pop_rdi)   + \\
          p64(binsh)     + \\
          p64(pop_rsi)   + \\
          p64(0)         + \\
          p64(pop_rdx)   + \\
          p64(0)         + \\
          p64(syscall)
          # 'A'的数量应改成实际所需的距离数量
          # execve("/bin/sh", 0, 0)
          # execve的系统调用号为59
''')



if __name__ == '__main__':
    main()
