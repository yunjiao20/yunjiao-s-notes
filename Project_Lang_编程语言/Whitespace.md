---
tags:
  - 2026/9/9
  - Whitespace
  - 语法
---
官方wiki: [https://esolangs.org/wiki/Whitespace](https://esolangs.org/wiki/Whitespace)

做 CTF 杂项时遇到的编程语言。趁现在看得懂找得到资料赶紧记一下。wiki是公认的权威资料，社区以其为规范。下面复制wiki页面（竟然直接在网页复制粘贴下来就基本能兼容，我只需要注释\[]、添加复制不下的水平线、示例处使用\`\`\`引起示例即可，好方便 ~~流口水~~）


# Whitespace
---
**Whitespace**, designed in 2003 by [Edwin Brady](https://esolangs.org/wiki/Edwin_Brady "Edwin Brady") and Chris Morris, is an imperative, stack-based, [esoteric programming language](https://esolangs.org/wiki/Esoteric_programming_language "Esoteric programming language") that uses only whitespace characters—space, tab, and linefeed—as syntax. All other characters are ignored. Whitespace got a brief moment of fame when it was posted on [Slashdot](https://en.wikipedia.org/wiki/Slashdot "wikipedia:Slashdot") on April 1st, 2003. Most people took it as an April Fool's joke, while it wasn't.

This page uses \[Space], \[Tab], and \[LF] for Space (ASCII 32), Tab (ASCII 9), and Line Feed (ASCII 10) respectively.

## Contents

- [1 Commands](https://esolangs.org/wiki/Whitespace#Commands)
    - [1.1 IMP](https://esolangs.org/wiki/Whitespace#IMP)
    - [1.2 Numbers](https://esolangs.org/wiki/Whitespace#Numbers)
    - [1.3 I/O](https://esolangs.org/wiki/Whitespace#I/O)
    - [1.4 Stack manipulation](https://esolangs.org/wiki/Whitespace#Stack_manipulation)
    - [1.5 Arithmetic](https://esolangs.org/wiki/Whitespace#Arithmetic)
    - [1.6 Flow Control](https://esolangs.org/wiki/Whitespace#Flow_Control)
    - [1.7 Heap Access](https://esolangs.org/wiki/Whitespace#Heap_Access)
- [2 Examples](https://esolangs.org/wiki/Whitespace#Examples)
    - [2.1 Cat program](https://esolangs.org/wiki/Whitespace#Cat_program)
    - [2.2 Hello, world!](https://esolangs.org/wiki/Whitespace#Hello,_world!)
    - [2.3 Truth-machine](https://esolangs.org/wiki/Whitespace#Truth-machine)
- [3 See also](https://esolangs.org/wiki/Whitespace#See_also)
- [4 External resources](https://esolangs.org/wiki/Whitespace#External_resources)

_这上面是以wiki中的界面为标准的，但我不打算改。为了方便跳转，我在下面提供可用于 Obsidian 此界面的跳转表_
- 1 [[#Commands]]
    - 1.1 [[#IMP]]
    - 1.2 [[#Numbers]]
    - 1.3 [[#I/O]]
    - 1.4 [[#Stack manipulation]]
    - 1.5 [[#Arithmetic]]
    - 1.6 [[#Flow Control]]
    - 1.7 [[#Heap Access]]
- 2 [[#Examples]]
    - 2.1 [[#[Cat program](https //esolangs.org/wiki/Cat_program "Cat program")]]
    - 2.2 [[#[Hello, world!](https //esolangs.org/wiki/Hello,_world! "Hello, world!")]]
    - 2.3 [[#[Truth-machine](https //esolangs.org/wiki/Truth-machine "Truth-machine")]]
- 3 [[#See also]]
- 4 [[#External resources]]



## Commands
---
### IMP

There are different types of commands in Whitespace, and they all have different Instruction Modification Parameters (IMP), which can be thought of as the category a command falls in. Every command starts with an IMP, followed by the remainder of the command, and followed by parameters, if necessary.

| IMP          | Command            |
| ------------ | ------------------ |
| [Tab][LF]    | I/O                |
| [Space]      | Stack Manipulation |
| [Tab][Space] | Arithmetic         |
| [LF]         | Flow control       |
| [Tab][Tab]   | Heap access        |
### Numbers

Numbers start with a sign (\[Space] for positive or \[Tab] for negative), then have a sequence of \[Space] (0) and \[Tab] (1) representing the number in binary, and end with \[LF].

### I/O

| Commands       | Parameters | Meaning                                                                                                     |
| -------------- | ---------- | ----------------------------------------------------------------------------------------------------------- |
| [Tab][Space]   | -          | Pop a heap address from the stack, read a character as ASCII, and store that character to that heap address |
| [Tab][Tab]     | -          | Pop a heap address from the stack, read a number, and store that number to that heap address                |
| [Space][Space] | -          | Pop a number from the stack and output it as an ASCII character                                             |
| [Space][Tab]   | -          | Pop a number from the stack and output it                                                                   |

The general pattern for the IO instructions is that the first character is [Tab] when an instruction is for input, and [Space] when it's for output. The second character is then [Space] for a character, and [Tab] for a number.

### Stack manipulation

| Commands     | Parameters | Meaning                                                                                 |
| ------------ | ---------- | --------------------------------------------------------------------------------------- |
| [Space]      | Number     | Push a number to the stack                                                              |
| [LF][Space]  | -          | Duplicate the top item on the stack                                                     |
| [LF][Tab]    | -          | Swap the top two items on the stack                                                     |
| [LF][LF]     | -          | Discard the top item on the stack                                                       |
| [Tab][Space] | Number     | Copy the nth item on the stack (given by the argument) onto the top of the stack (v0.3) |
| [Tab][LF]    | Number     | Slide n items off the stack, keeping the top item (v0.3)                                |

### Arithmetic

Arithmetic commands operate on the top two items on the stack, and replace them with the result of the operation. The first element pushed is considered to be left of the operator.

| Command        | Parameters | Meaning          |
| -------------- | ---------- | ---------------- |
| [Space][Space] | -          | Addition         |
| [Space][Tab]   | -          | Subtraction      |
| [Space][LF]    | -          | Multiplication   |
| [Tab][Space]   | -          | Integer Division |
| [Tab][Tab]     | -          | Modulo           |

### Flow Control

| Commands       | Parameters | Meaning                                                  |
| -------------- | ---------- | -------------------------------------------------------- |
| [Space][Space] | Label      | Mark a location in the program                           |
| [Space][Tab]   | Label      | Call a subroutine                                        |
| [Space][LF]    | Label      | Jump unconditionally to a label                          |
| [Tab][Space]   | Label      | Jump to a label if the top of the stack is zero          |
| [Tab][Tab]     | Label      | Jump to a label if the top of the stack is negative      |
| [Tab][LF]      | -          | End a subroutine and transfer control back to the caller |
| [LF][LF]       | -          | Ends the program                                         |

Labels are a sequence of \[Space] and \[Tab], ended by \[LF].

### Heap Access

Heap access commands look at the stack to find the address of the items to be stored or retrieved. To store a number, the address and value must be pushed in that order, then the store command must be run. To retrieve a number, the address must be pushed and the retrieve command must be run after; this will push the value at the given address to the stack.

| Command | Parameters | Meaning  |
| ------- | ---------- | -------- |
| [Space] | -          | Store    |
| [Tab]   | -          | Retrieve |

## Examples
---
### [Cat program](https://esolangs.org/wiki/Cat_program "Cat program")
```
[LF][Space][Space][Space]
[LF][Space][Space][Space][Tab]
[LF][Tab]
[LF][Tab][Space][Space][Space][Space][Tab]
[LF][Tab][Tab][Tab][Tab]
[LF][Space][Space][Space][Space][Space][Tab]
[LF][Tab][Tab][Tab]
[LF][Tab][Space][Tab]
[LF]
[LF][Space]
[LF][Space]
[LF]
[LF][Space][Space][Tab]
[LF]
[LF]
[LF]
[LF]
```

### [Hello, world!](https://esolangs.org/wiki/Hello,_world! "Hello, world!")
```
Hello,[Space]world![Space][Space][Tab][Space][Space][Tab][Space][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Space][Tab][Space][Tab][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Tab][Tab][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Tab][Tab][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Tab][Tab][Tab][Tab][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Space][Tab][Tab][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Space][Space][Space][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Tab][Space][Tab][Tab][Tab][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Tab][Tab][Tab][Tab][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Tab][Space][Space][Tab][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Tab][Tab][Space][Space][LF]
[Tab][LF][Space][Space]
[Space][Space][Space][Tab][Tab][Space][Space][Tab][Space][Space][LF]
[Tab][LF][Space][Space]
[LF][LF][LF]
```

### [Truth-machine](https://esolangs.org/wiki/Truth-machine "Truth-machine")
```
[Space][Space][Space][LF]
[Space][LF][Space]
[Tab][LF][Tab][Tab]
[Tab][Tab][Tab]
[LF][Tab][Space][Space][LF]
[LF][Space][Space][Tab][LF]
[Space][Space][Space][Tab][LF]
[Tab][LF][Space][Tab]
[LF][Space][LF][Tab][LF]
[LF][Space][Space][Space][LF]
[Space][Space][Space][LF]
[Tab][LF][Space][Tab]
[LF][LF][LF]
```


## See also
---
- [Unispace](https://esolangs.org/wiki/Unispace "Unispace")
- [HaPyLi](https://esolangs.org/wiki/HaPyLi "HaPyLi")
- [Acme::Bleach](https://esolangs.org/wiki/Acme::Bleach "Acme::Bleach") (Circa 2001)
- [Visible Whitespace](https://esolangs.org/wiki/Visible_Whitespace "Visible Whitespace")

## External resources
---
- [Whitespace website](https://web.archive.org/web/20150623025348/http://compsoc.dur.ac.uk/whitespace/) _(from the [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine "wikipedia:Wayback Machine"); retrieved on 23 June 2015)_
- [The Whitespace Corpus](https://github.com/wspace/corpus) A collection of interpreters, compilers, and programs for Whitespace
- [Interpreter Collection for the Whitespace Language](https://github.com/hostilefork/whitespacers/) (GitHub)
- [whitespace-rs](https://github.com/CensoredUsername/whitespace-rs) A Whitespace JIT
- [Slashdot announcement](http://developers.slashdot.org/article.pl?sid=03/04/01/0332202)
- [Whitespace interpreter implemented in Haskell](https://github.com/helvm/helma#readme)
- [WSA (Whitespace assembler) implemented in Haskell](https://github.com/helvm/helpa#readme)