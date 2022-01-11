Title: Use 'command -v' Over 'which' to Find a Program's Executable
Date: 2021-11-16


One thing that came to me as news is that the command `which`—which is the de-facto tool to find the path of an executable—is not POSIX compliant. The recent Debian [debacle](https://lwn.net/Articles/874049/) around `which` brought it to my attention. The POSIX-compliant way of finding an executable program is `command -v`, which is usually built into most of the shells.

So, instead of doing this:

```
which python3.10
```

Do this:

```
command -v which python3.10
```


## References

* [Debian's Which Hunt](https://lwn.net/Articles/874049/)
* [TIL: which is not POSIX](https://hynek.me/til/which-not-posix/)
