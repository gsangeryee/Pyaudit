<h1 align=center><code>Pyaudit</code></h1>

## Introduction

`Pyaudit` is a static programming language analyzer, specially for solidity contracts. Its main ideas come from [c4udit](https://github.com/byterocket/c4udit) and [Rustol](https://github.com/Jansen-C-Moreira/Rustol)

![Pyaudit Design](/images/design.png)

run

```
python pyaudit.py -c=2023-01-canto-identity -u=https://github.com/code-423n4/2023-01-canto-identity/blob/main
```

### Auto
1. Close all of chrome and check activity
2. Open remote debug chrome
   start remote debug chrome
    ```
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
    ```
    check, open another terminal 
    ```
    lsof -i :9222
    ```
3. Run pyaudit with auto mode
    ```
    python python contest.py
    ```

### Single contest mode
Some contests url in view repo link  is not the real code repo. You need manually get the real link.

1. run pyaudit with single mode
    ```
    python contest.py -u=https://github.com/code-423n4/2023-03-polynomial
    ``` 

### Manual mode

1. donwload the contest repo in audit folder
2. Add scope in `scope.txt`, scope comes from contest's README.md
3. run pyaudit with
    ```
    python pyaudit.py -c=contest -u=contest_real_url
    ```
    example:
    ```
    python pyaudit.py -c=2023-01-canto-identity -u=https://github.com/code-423n4/2023-01-canto-identity/blob/main
    ```

### TODO

- Verify the reliability of the rules Using the latest [Reoprts](https://code4rena.com/reports)

### Create Path file

- copy scope lines in VSCode,
- `command+F` and trun `Use Regular Expression(option+command+R)
- input `.*\[(.*.sol)\].*`
- input `$1` in replace dialog, and `replace all`
- check the result

### Log
- Tue Apr4 2023: Update gasop.json. Every week renew it. The rule that has been updated, it will add a plus sign in the end of the rule name.