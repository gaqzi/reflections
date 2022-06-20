---
title: Distil git logs attached to a single file
date: 2022-06-21
tags: shell, git
---

I run `git log --oneline` to list out the commit logs all the time. It prints out a
compact view of the git history. Running the command in this repo gives me this:

```
d9fad76 Publish blog on safer operator.itemgetter, closes #130
0570997 Merge pull request #129 from rednafi/dependabot/github_actions/...
6967f73 Bump actions/setup-python from 3 to 4
48c8634 Merge pull request #128 from rednafi/dependabot/pip/mypy-0.961
5b7a7b0 Bump mypy from 0.960 to 0.961
```

However, there are times when I need to list out the commit logs that only represent
the changes made to a particular file. Here's the command that does exactly that.

```
git logs --oneline --follow <file_path>
```

Running the command on the markdown file that you're reading gives this:

```
git log --oneline
```
