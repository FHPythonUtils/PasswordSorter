Module passwordsorter.sort
==========================
PASSWORD SORTER

Sort dumps into Email, hash, password, source

Functions
---------

    
`getSrc(filename: str) ‑> Optional[str]`
:   Grab the source/ domain from the filename
    
    Args:
            filename (str): the relative file path/ filename
    
    Returns:
            string|None: return the domain name or None

    
`hasPwdComplexity(password: str) ‑> bool`
:   Does the password have sufficient complexity?
    
    Args:
            password (string): password to check
    
    Returns:
            bool: true if the string looks like a complex password

    
`idEmailCol(data: list, threshhold: float = 0.85) ‑> int`
:   Do some heuristics on the data and return the column index that is
    likely to be the email column
    
    Args:
            data (list[list[str]]): the 2d array of data to analyse
            threshhold (float, optional): The confidence that the column actually
            contains email addresses. Defaults to 0.85.
    
    Returns:
            int: the column index for emails

    
`idHashCol(data: list, threshhold: float = 0.85) ‑> int`
:   Do some heuristics on the data and return the column index that is
    likely to be the hash column
    
    Args:
            data (list[list[str]]): the 2d array of data to analyse
            threshhold (float, optional): The confidence that the column actually
            contains hashes. Defaults to 0.85.
    
    Returns:
            int: the column index for the hashes

    
`idPwdCol(data: list, threshhold: float = 0.7) ‑> int`
:   Do some heuristics on the data and return the column index that is
    likely to be the password column
    
    Args:
            data (list[list[str]]): the 2d array of data to analyse
            threshhold (float, optional): The confidence that the column actually
            contains passwords. Defaults to 0.7.
    
    Returns:
            int: the column index for the passwords

    
`isKnownPwd(password: str) ‑> bool`
:   Is the password known? As in does it show up in the top 10,000 list?
    
    Args:
            password (str): password to check
    
    Returns:
            bool: true if known

    
`process(lines: list, filename: str)`
:   Process a file
    
    Args:
            lines (list[str]): list of lines from the file
            filename (str): path to the file

    
`processFile(filename: str)`
:   Open a massive file and call process() for each 1gb chunk
    
    Args:
            filename (str): relative file path of dump

    
`returnArr(lines: list, delim: Optional[str] = None) ‑> list`
:   Convert the array of raw data (lines) to a 2d array representing a table
    
    Args:
            lines (string[]): array of plaintext lines (raw data)

    
`returnDelim(lines: list)`
:   Return the most likely delimeter from some input data
    
    Args:
            lines (list[str]): array of plaintext lines (raw data)